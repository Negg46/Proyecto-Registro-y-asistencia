import mysql.connector
import os
from datetime import date, datetime, timedelta


def _cargar_env_local():
    """Carga variables desde un archivo .env en la raiz del proyecto.
    No sobreescribe variables ya definidas en el sistema.
    """
    ruta_env = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(ruta_env):
        return

    with open(ruta_env, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or linea.startswith('#') or '=' not in linea:
                continue

            clave, valor = linea.split('=', 1)
            clave = clave.strip()
            valor = valor.strip().strip('"').strip("'")

            if clave and clave not in os.environ:
                os.environ[clave] = valor


class Registro_datos:
    def __init__(self):
        _cargar_env_local()

        # En local toma los valores de entorno si existen, si no usa los defaults de desarrollo
        host     = os.environ.get('DB_HOST', 'localhost')
        user     = os.environ.get('DB_USER', 'root')
        password = os.environ.get('DB_PASS', '')
        dbname   = os.environ.get('DB_NAME', 'registro_casino')
        port_txt = os.environ.get('DB_PORT', '3306')
        try:
            port = int(port_txt)
        except ValueError:
            port = 3306

        self.server_config = {'host': host, 'user': user, 'password': password, 'port': port}
        self.database_name = dbname
        self.config = {**self.server_config, 'database': self.database_name}
        self.asegurar_base_datos()
        self.crear_tablas()
        self.normalizar_esquema()
        self.insertar_datos_demo_si_vacio()
        self.recalcular_asistencias_y_niveles()

    def asegurar_base_datos(self):
        # En servicios remotos (Render) la BD ya existe; CREATE DATABASE puede no tener permisos
        try:
            con = mysql.connector.connect(**self.server_config)
            cursor = con.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            con.commit()
            cursor.close()
            con.close()
        except Exception:
            # Si ya existe o no hay permisos para crearla, continua con la conexion directa
            pass

    def conectar(self):
        return mysql.connector.connect(**self.config)

    def _tabla_existe(self, cursor, nombre_tabla):
        cursor.execute('SHOW TABLES LIKE %s', (nombre_tabla,))
        return cursor.fetchone() is not None

    def _obtener_columnas(self, cursor, nombre_tabla):
        if not self._tabla_existe(cursor, nombre_tabla):
            return set()
        cursor.execute(f'SHOW COLUMNS FROM {nombre_tabla}')
        return {fila[0] for fila in cursor.fetchall()}

    def _crear_tabla_clientes(self, cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                dni VARCHAR(20) NOT NULL UNIQUE,
                telefono VARCHAR(20),
                email VARCHAR(100),
                fecha_nacimiento DATE,
                nivel VARCHAR(20) NOT NULL DEFAULT 'Clasica',
                tarjeta VARCHAR(50) NOT NULL,
                asistencias_dias INT DEFAULT 0
            ) ENGINE=InnoDB
            """
        )

    def _crear_tabla_asistencias(self, cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS asistencias(
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_id INT NOT NULL,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                CONSTRAINT fk_asistencias_clientes
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                    ON DELETE CASCADE,
                INDEX idx_asistencias_fecha (fecha),
                INDEX idx_asistencias_cliente (cliente_id)
            ) ENGINE=InnoDB
            """
        )

    def _crear_tabla_actividad_operador(self, cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS actividad_operador(
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(60) NOT NULL,
                rol VARCHAR(30) NOT NULL,
                accion VARCHAR(80) NOT NULL,
                cliente_id INT NULL,
                detalle VARCHAR(255) NULL,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                INDEX idx_actividad_usuario_fecha (usuario, fecha),
                INDEX idx_actividad_rol_fecha (rol, fecha),
                INDEX idx_actividad_cliente (cliente_id)
            ) ENGINE=InnoDB
            """
        )

    def crear_tablas(self):
        con = self.conectar()
        cursor = con.cursor()
        self._crear_tabla_clientes(cursor)
        self._crear_tabla_asistencias(cursor)
        self._crear_tabla_actividad_operador(cursor)
        con.commit()
        cursor.close()
        con.close()

    def normalizar_esquema(self):
        con = self.conectar()
        cursor = con.cursor()
        columnas_clientes = self._obtener_columnas(cursor, 'clientes')
        columnas_asistencias = self._obtener_columnas(cursor, 'asistencias')

        columnas_requeridas_clientes = {
            'telefono': 'ALTER TABLE clientes ADD COLUMN telefono VARCHAR(20) NULL',
            'email': 'ALTER TABLE clientes ADD COLUMN email VARCHAR(100) NULL',
            'fecha_nacimiento': 'ALTER TABLE clientes ADD COLUMN fecha_nacimiento DATE NULL',
            'nivel': "ALTER TABLE clientes ADD COLUMN nivel VARCHAR(20) NOT NULL DEFAULT 'Clasica'",
            'tarjeta': "ALTER TABLE clientes ADD COLUMN tarjeta VARCHAR(50) NOT NULL DEFAULT ''",
            'asistencias_dias': 'ALTER TABLE clientes ADD COLUMN asistencias_dias INT DEFAULT 0'
        }
        columnas_requeridas_asistencias = {
            'fecha': 'ALTER TABLE asistencias ADD COLUMN fecha DATE NULL',
            'hora': "ALTER TABLE asistencias ADD COLUMN hora TIME NOT NULL DEFAULT '00:00:00'"
        }

        legacy_clientes = {
            'Id_Cliente', 'Nombre_Completo', 'Numero_Identificacion', 'Correo_Electronico',
            'Fecha_Nacimiento', 'Nivel_Cliente', 'Numero_Tarjeta'
        }.issubset(columnas_clientes)
        legacy_asistencias = {'Id_Asistencia', 'Id_Cliente', 'Fecha_Asistencia'}.issubset(columnas_asistencias)

        if legacy_clientes or legacy_asistencias:
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0')

        if legacy_asistencias:
            cursor.execute('DROP TABLE IF EXISTS asistencias_legacy_backup')
            cursor.execute('RENAME TABLE asistencias TO asistencias_legacy_backup')

        if legacy_clientes:
            cursor.execute('DROP TABLE IF EXISTS clientes_legacy_backup')
            cursor.execute('RENAME TABLE clientes TO clientes_legacy_backup')

        if legacy_clientes:
            self._crear_tabla_clientes(cursor)
            cursor.execute(
                """
                INSERT INTO clientes (id, nombre, dni, telefono, email, fecha_nacimiento, nivel, tarjeta, asistencias_dias)
                SELECT
                    Id_Cliente,
                    Nombre_Completo,
                    Numero_Identificacion,
                    Telefono,
                    Correo_Electronico,
                    Fecha_Nacimiento,
                    Nivel_Cliente,
                    Numero_Tarjeta,
                    0
                FROM clientes_legacy_backup
                """
            )

        if legacy_asistencias:
            self._crear_tabla_asistencias(cursor)
            cursor.execute(
                """
                INSERT INTO asistencias (id, cliente_id, fecha, hora)
                SELECT
                    Id_Asistencia,
                    Id_Cliente,
                    DATE(Fecha_Asistencia),
                    TIME(Fecha_Asistencia)
                FROM asistencias_legacy_backup
                """
            )

        if not legacy_clientes:
            for columna, sentencia in columnas_requeridas_clientes.items():
                if columna not in columnas_clientes:
                    cursor.execute(sentencia)

        if not legacy_asistencias:
            for columna, sentencia in columnas_requeridas_asistencias.items():
                if columna not in columnas_asistencias and columnas_asistencias:
                    cursor.execute(sentencia)

            if 'fecha' in columnas_asistencias and 'hora' in columnas_asistencias:
                cursor.execute('UPDATE asistencias SET fecha = COALESCE(fecha, CURDATE()) WHERE fecha IS NULL')
                cursor.execute('UPDATE asistencias SET hora = COALESCE(hora, "00:00:00")')
                cursor.execute('ALTER TABLE asistencias MODIFY COLUMN fecha DATE NOT NULL')
                cursor.execute('ALTER TABLE asistencias MODIFY COLUMN hora TIME NOT NULL')

        if legacy_clientes or legacy_asistencias:
            cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

        con.commit()
        cursor.close()
        con.close()

    def insertar_datos_demo_si_vacio(self):
        clientes_demo = [
            ('Juan Miguel Carreno', '1097493234', '3242253587', 'juanmiguel@correo.com', '2006-04-22', 'Clasica', '54165423'),
            ('Maria Gonzalez', '1234567890', '3001234567', 'maria@example.com', '1990-05-15', 'VIP', '12345678'),
            ('Carlos Rodriguez', '0987654321', '3019876543', 'carlos@example.com', '1985-08-20', 'Clasica', '98765432'),
            ('Ana Lopez', '1122334455', '3021122334', 'ana@example.com', '1995-12-10', 'VIP', '11223344'),
            ('Pedro Sanchez', '5566778899', '3035566778', 'pedro@example.com', '1980-03-25', 'Clasica', '55667788'),
            ('Laura Martinez', '6677889900', '3046677889', 'laura@example.com', '1992-07-30', 'VIP', '66778899'),
            ('Diego Fernandez', '7788990011', '3057788990', 'diego@example.com', '1988-11-05', 'Clasica', '77889900'),
            ('Sofia Ramirez', '8899001122', '3068899001', 'sofia@example.com', '1998-01-18', 'Clasica', '88990011'),
            ('Javier Torres', '9900112233', '3079900112', 'javier@example.com', '1975-09-12', 'Clasica', '99001122'),
            ('Elena Morales', '0011223344', '3080011223', 'elena@example.com', '1993-04-08', 'Clasica', '00112233')
        ]

        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute('SELECT id, dni FROM clientes')
        existentes = {fila['dni']: fila['id'] for fila in cursor.fetchall()}

        inserciones_clientes = [cliente for cliente in clientes_demo if cliente[1] not in existentes]
        if inserciones_clientes:
            cursor_insert = con.cursor()
            cursor_insert.executemany(
                """
                INSERT INTO clientes (nombre, dni, telefono, email, fecha_nacimiento, nivel, tarjeta)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                inserciones_clientes
            )
            cursor_insert.close()

        cursor.execute('SELECT id, dni FROM clientes')
        mapa_clientes = {fila['dni']: fila['id'] for fila in cursor.fetchall()}

        hoy = date.today()
        plan_asistencias = {
            '1097493234': {0: ['09:12:00', '14:48:00'], 1: ['10:05:00'], 2: ['12:25:00'], 4: ['18:10:00']},
            '1234567890': {0: ['08:40:00', '16:05:00'], 1: ['09:20:00'], 2: ['09:35:00'], 3: ['10:15:00'], 4: ['11:10:00'], 5: ['18:40:00'], 6: ['20:00:00'], 7: ['17:35:00'], 8: ['16:10:00'], 9: ['19:05:00'], 10: ['13:30:00'], 11: ['14:50:00'], 12: ['15:40:00'], 13: ['21:05:00'], 14: ['22:10:00'], 15: ['10:45:00']},
            '0987654321': {0: ['11:20:00'], 2: ['13:15:00'], 4: ['15:10:00'], 6: ['16:25:00'], 8: ['18:05:00']},
            '1122334455': {0: ['10:30:00'], 1: ['17:20:00'], 2: ['19:10:00'], 3: ['20:30:00'], 4: ['22:00:00'], 5: ['18:45:00'], 6: ['17:10:00'], 7: ['16:15:00'], 8: ['15:00:00'], 9: ['14:20:00'], 10: ['13:10:00'], 11: ['12:40:00'], 12: ['11:50:00'], 13: ['10:10:00'], 14: ['09:15:00']},
            '5566778899': {0: ['18:35:00'], 3: ['20:00:00'], 7: ['19:15:00']},
            '6677889900': {0: ['07:55:00', '23:10:00'], 1: ['08:15:00'], 2: ['09:00:00'], 3: ['09:40:00'], 4: ['10:20:00'], 5: ['11:00:00'], 6: ['12:10:00'], 7: ['13:30:00'], 8: ['14:05:00'], 9: ['15:15:00'], 10: ['16:25:00'], 11: ['17:40:00'], 12: ['18:10:00'], 13: ['19:00:00'], 14: ['20:15:00'], 15: ['21:30:00'], 16: ['22:05:00']},
            '7788990011': {0: ['12:10:00'], 1: ['18:30:00'], 5: ['20:20:00']},
            '8899001122': {0: ['13:45:00'], 2: ['15:50:00'], 6: ['18:25:00']},
            '9900112233': {1: ['11:15:00'], 2: ['11:45:00'], 3: ['12:15:00'], 4: ['12:45:00']},
            '0011223344': {0: ['17:05:00'], 1: ['17:40:00'], 2: ['18:20:00'], 3: ['19:00:00']}
        }

        cursor.execute('SELECT cliente_id, fecha, hora FROM asistencias')
        asistencias_existentes = {
            (fila['cliente_id'], fila['fecha'].isoformat() if hasattr(fila['fecha'], 'isoformat') else str(fila['fecha']), str(fila['hora']))
            for fila in cursor.fetchall()
        }

        registros_asistencia = []
        for dni, visitas_por_dia in plan_asistencias.items():
            if dni not in mapa_clientes:
                continue
            cliente_id = mapa_clientes[dni]
            for dias_atras, horas in visitas_por_dia.items():
                fecha_visita = hoy - timedelta(days=dias_atras)
                for hora in horas:
                    clave = (cliente_id, fecha_visita.isoformat(), hora)
                    if clave not in asistencias_existentes:
                        registros_asistencia.append((cliente_id, fecha_visita, hora))

        if registros_asistencia:
            cursor_insert = con.cursor()
            cursor_insert.executemany(
                'INSERT INTO asistencias (cliente_id, fecha, hora) VALUES (%s, %s, %s)',
                registros_asistencia
            )
            cursor_insert.close()

        con.commit()
        cursor.close()
        con.close()

    def recalcular_asistencias_y_niveles(self):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.id, COUNT(DISTINCT a.fecha) AS total_dias
            FROM clientes c
            LEFT JOIN asistencias a ON a.cliente_id = c.id
            GROUP BY c.id
            """
        )
        resumen = cursor.fetchall()

        actualizador = con.cursor()
        for fila in resumen:
            total_dias = fila['total_dias'] or 0
            nivel = 'VIP' if total_dias >= 15 else 'Clasica'
            actualizador.execute(
                'UPDATE clientes SET asistencias_dias = %s, nivel = %s WHERE id = %s',
                (total_dias, nivel, fila['id'])
            )

        con.commit()
        actualizador.close()
        cursor.close()
        con.close()

    def inserta_producto(self, nombre, dni, tel, email, fecha_nac, nivel, num_tarjeta):
        try:
            con = self.conectar()
            cursor = con.cursor()
            sql = (
                'INSERT INTO clientes (nombre, dni, telefono, email, fecha_nacimiento, nivel, tarjeta) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)'
            )
            cursor.execute(sql, (nombre, dni, tel, email, fecha_nac, nivel, num_tarjeta))
            con.commit()
            cursor.close()
            con.close()
        except Exception as error:
            raise RuntimeError(f'No se pudo guardar: {error}')

    def obtener_clientes(self):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM clientes ORDER BY nombre')
        datos = cursor.fetchall()
        cursor.close()
        con.close()
        return datos

    def obtener_cliente_por_dni(self, dni):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute('SELECT * FROM clientes WHERE dni = %s', (dni,))
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def obtener_cliente_para_edicion(self, dni):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM clientes WHERE dni = %s', (dni,))
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def buscar_tarjeta_por_nivel(self, tarjeta, nivel):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute(
            'SELECT id, tarjeta, nivel FROM clientes WHERE tarjeta = %s AND nivel = %s',
            (tarjeta, nivel)
        )
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def actualizar_cliente(self, id_cliente, nombre, dni, tel, email, fecha_nac, nivel, num_tarjeta):
        try:
            con = self.conectar()
            cursor = con.cursor()
            sql = (
                'UPDATE clientes SET nombre=%s, dni=%s, telefono=%s, email=%s, '
                'fecha_nacimiento=%s, nivel=%s, tarjeta=%s WHERE id=%s'
            )
            cursor.execute(sql, (nombre, dni, tel, email, fecha_nac, nivel, num_tarjeta, id_cliente))
            con.commit()
            cursor.close()
            con.close()
        except Exception as error:
            raise RuntimeError(f'Error al actualizar: {error}')

    def actualizar_clientes(self, id_cliente, nombre, dni, tel, email, fecha_nac, nivel, num_tarjeta):
        self.actualizar_cliente(id_cliente, nombre, dni, tel, email, fecha_nac, nivel, num_tarjeta)

    def registrar_asistencia(self, dni):
        cliente = self.obtener_cliente_por_dni(dni)
        if not cliente:
            return {'status': 'error', 'message': 'Cliente no registrado'}

        cliente_id = cliente['id']
        hoy = date.today()
        ahora = datetime.now().time().replace(microsecond=0)

        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            'INSERT INTO asistencias(cliente_id, fecha, hora) VALUES(%s, %s, %s)',
            (cliente_id, hoy, ahora)
        )
        cursor.execute(
            'SELECT COUNT(*) AS total_hoy FROM asistencias WHERE cliente_id = %s AND fecha = %s',
            (cliente_id, hoy)
        )
        asistencias_hoy = cursor.fetchone()['total_hoy']

        if asistencias_hoy == 1:
            nuevas_asistencias_totales = (cliente['asistencias_dias'] or 0) + 1
            nuevo_nivel = 'VIP' if nuevas_asistencias_totales >= 15 else 'Clasica'
            cursor.execute(
                'UPDATE clientes SET asistencias_dias = %s, nivel = %s WHERE id = %s',
                (nuevas_asistencias_totales, nuevo_nivel, cliente_id)
            )
            nivel_actual = nuevo_nivel
        else:
            nivel_actual = cliente['nivel']

        con.commit()
        cursor.close()
        con.close()

        return {
            'status': 'success',
            'message': f'Entrada registrada. Actividad de hoy: {asistencias_hoy} visitas. | Nivel: {nivel_actual}'
        }

    def obtener_estadisticas_dashboard(self):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM clientes) AS total_clientes,
                (SELECT COUNT(*) FROM asistencias WHERE fecha = CURDATE()) AS visitas_hoy,
                (SELECT COUNT(DISTINCT cliente_id) FROM asistencias WHERE fecha = CURDATE()) AS clientes_unicos_hoy,
                (SELECT COUNT(*) FROM clientes WHERE nivel = 'VIP') AS total_vip,
                (SELECT COUNT(*) FROM clientes WHERE nivel = 'Clasica') AS total_clasica
            """
        )
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def obtener_asistencias_ultimos_dias(self, limite=7):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT fecha, COUNT(*) AS total_visitas, COUNT(DISTINCT cliente_id) AS clientes_unicos
            FROM asistencias
            GROUP BY fecha
            ORDER BY fecha DESC
            LIMIT %s
            """,
            (limite,)
        )
        filas = cursor.fetchall()
        cursor.close()
        con.close()
        return list(reversed(filas))

    def buscar_clientes(self, termino, limite=12):
        termino_busqueda = f'%{termino.strip()}%'
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nombre, dni, nivel, tarjeta, asistencias_dias
            FROM clientes
            WHERE nombre LIKE %s OR dni LIKE %s
            ORDER BY nombre
            LIMIT %s
            """,
            (termino_busqueda, termino_busqueda, limite)
        )
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados

    def obtener_resumen_cliente(self, cliente_id):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                c.id,
                c.nombre,
                c.dni,
                c.nivel,
                c.tarjeta,
                c.asistencias_dias,
                COUNT(a.id) AS total_registros,
                COUNT(DISTINCT a.fecha) AS total_dias,
                SUM(CASE WHEN a.fecha = CURDATE() THEN 1 ELSE 0 END) AS visitas_hoy,
                MAX(CASE WHEN a.fecha = CURDATE() THEN a.hora ELSE NULL END) AS ultima_hora_hoy
            FROM clientes c
            LEFT JOIN asistencias a ON a.cliente_id = c.id
            WHERE c.id = %s
            GROUP BY c.id, c.nombre, c.dni, c.nivel, c.tarjeta, c.asistencias_dias
            """,
            (cliente_id,)
        )
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def obtener_asistencias_por_dia_cliente(self, cliente_id, limite=15):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT fecha, COUNT(*) AS visitas
            FROM asistencias
            WHERE cliente_id = %s
            GROUP BY fecha
            ORDER BY fecha DESC
            LIMIT %s
            """,
            (cliente_id, limite)
        )
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado

    def obtener_movimientos_hoy_cliente(self, cliente_id):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT hora
            FROM asistencias
            WHERE cliente_id = %s AND fecha = CURDATE()
            ORDER BY hora DESC
            """,
            (cliente_id,)
        )
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado

    def obtener_top_clientes(self, limite=5):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                c.nombre,
                c.nivel,
                COUNT(a.id) AS total_registros,
                COUNT(DISTINCT a.fecha) AS total_dias
            FROM clientes c
            LEFT JOIN asistencias a ON a.cliente_id = c.id
            GROUP BY c.id, c.nombre, c.nivel
            ORDER BY total_dias DESC, total_registros DESC, c.nombre ASC
            LIMIT %s
            """,
            (limite,)
        )
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado

    def obtener_clientes_hoy(self, limite=8):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                c.nombre,
                c.nivel,
                COUNT(a.id) AS visitas_hoy,
                MAX(a.hora) AS ultima_entrada
            FROM asistencias a
            JOIN clientes c ON c.id = a.cliente_id
            WHERE a.fecha = CURDATE()
            GROUP BY c.id, c.nombre, c.nivel
            ORDER BY ultima_entrada DESC
            LIMIT %s
            """,
            (limite,)
        )
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado

    def obtener_actividad_todos_operadores(self):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                usuario,
                rol,
                SUM(CASE WHEN fecha = CURDATE() THEN 1 ELSE 0 END) AS hoy,
                SUM(CASE WHEN YEAR(fecha) = YEAR(CURDATE()) AND MONTH(fecha) = MONTH(CURDATE()) THEN 1 ELSE 0 END) AS mes,
                SUM(CASE WHEN YEAR(fecha) = YEAR(CURDATE()) THEN 1 ELSE 0 END) AS anio,
                COUNT(*) AS total_historico,
                MAX(CONCAT(fecha, ' ', hora)) AS ultima_accion
            FROM actividad_operador
            GROUP BY usuario, rol
            ORDER BY hoy DESC, mes DESC
            """
        )
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado

    def obtener_ultimas_acciones_todas(self, limite=12):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT usuario, rol, accion, detalle, fecha, hora
            FROM actividad_operador
            ORDER BY fecha DESC, hora DESC
            LIMIT %s
            """,
            (limite,)
        )
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado

    def registrar_actividad_operador(self, usuario, rol, accion, cliente_id=None, detalle=''):
        if not usuario or not rol:
            return

        ahora = datetime.now()
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute(
            """
            INSERT INTO actividad_operador (usuario, rol, accion, cliente_id, detalle, fecha, hora)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (usuario, rol, accion, cliente_id, detalle, ahora.date(), ahora.time().replace(microsecond=0))
        )
        con.commit()
        cursor.close()
        con.close()

    def obtener_resumen_actividad_operador(self, usuario, rol):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                SUM(CASE WHEN fecha = CURDATE() THEN 1 ELSE 0 END) AS registros_dia,
                SUM(CASE WHEN YEAR(fecha) = YEAR(CURDATE()) AND MONTH(fecha) = MONTH(CURDATE()) THEN 1 ELSE 0 END) AS registros_mes,
                SUM(CASE WHEN YEAR(fecha) = YEAR(CURDATE()) THEN 1 ELSE 0 END) AS registros_anio
            FROM actividad_operador
            WHERE usuario = %s AND rol = %s
            """,
            (usuario, rol)
        )
        resultado = cursor.fetchone() or {}
        cursor.close()
        con.close()
        return {
            'registros_dia': resultado.get('registros_dia') or 0,
            'registros_mes': resultado.get('registros_mes') or 0,
            'registros_anio': resultado.get('registros_anio') or 0
        }

    def obtener_actividad_operador_hoy(self, usuario, rol, limite=20):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT accion, detalle, hora
            FROM actividad_operador
            WHERE usuario = %s AND rol = %s AND fecha = CURDATE()
            ORDER BY hora DESC
            LIMIT %s
            """,
            (usuario, rol, limite)
        )
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado

    def obtener_actividad_operador_mes(self, usuario, rol):
        con = self.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT fecha, COUNT(*) AS total
            FROM actividad_operador
            WHERE usuario = %s AND rol = %s
              AND YEAR(fecha) = YEAR(CURDATE())
              AND MONTH(fecha) = MONTH(CURDATE())
            GROUP BY fecha
            ORDER BY fecha DESC
            """,
            (usuario, rol)
        )
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado
