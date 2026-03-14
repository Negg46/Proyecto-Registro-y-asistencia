import mysql.connector #pip install mysql-connector-python

class Registro_datos():
    def __init__(self):
        # Configuración de la conexión a la base de datos
        self.conexion = mysql.connector.connect(
            host='localhost',
            database='registro_casino',
            user='root',
            password='',
        )
        # Asegurarse de que exista la tabla de asistencias para llevar el conteo de visitas
        self._crear_tabla_asistencias()
        # Asegurarse de que exista la columna Fecha_VIP en la tabla clientes
        self._asegurar_columna_fecha_vip()
        
    def _crear_tabla_asistencias(self):
        """Crea la tabla de asistencias si aún no existe."""
        try:
            cur = self.conexion.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS asistencias (
                    Id_Asistencia INT NOT NULL AUTO_INCREMENT,
                    Id_Cliente INT NOT NULL,
                    Fecha_Asistencia TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (Id_Asistencia),
                    INDEX (Id_Cliente),
                    FOREIGN KEY (Id_Cliente) REFERENCES clientes(Id_Cliente)
                ) ENGINE=InnoDB;
                """
            )
            self.conexion.commit()
            cur.close()
        except Exception as e:
            print(f"No se pudo crear la tabla de asistencias: {e}")

    def _asegurar_columna_fecha_vip(self):
        """Agrega la columna Fecha_VIP en clientes si todavía no existe."""
        try:
            cur = self.conexion.cursor()
            cur.execute(
                "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS Fecha_VIP TIMESTAMP NULL DEFAULT NULL"
            )
            self.conexion.commit()
            cur.close()
        except Exception as e:
            print(f"No se pudo asegurar la columna Fecha_VIP: {e}")

    def inserta_producto(self, nombre, dni, Tel, email, fecha_nac, nivel, tarjeta):
        """Inserta un nuevo cliente con la fecha y hora actual de registro.

        Nota: El nivel se asigna automáticamente como 'Clasica' al crear el cliente.
        """
        nivel = "Clasica"  # Nivel inicial por defecto
        cur = self.conexion.cursor()
        sql = ("INSERT INTO clientes (Nombre_Completo, Numero_Identificacion, Telefono, Correo_Electronico, Fecha_Nacimiento, Nivel_Cliente, Numero_Tarjeta, Fecha_Registro, Fecha_VIP) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NULL)")
        cur.execute(sql, (nombre, dni, Tel, email, fecha_nac, nivel, tarjeta))
        self.conexion.commit()
        last_id = cur.lastrowid
        cur.close()
        return last_id

    def obtener_clientes(self):
        """Devuelve la lista completa de clientes."""
        cur = self.conexion.cursor(buffered=True)
        cur.execute("SELECT Id_Cliente, Nombre_Completo, Numero_Identificacion, Telefono, Correo_Electronico, Fecha_Nacimiento, Nivel_Cliente, Numero_Tarjeta, Fecha_Registro FROM clientes")
        resultados = cur.fetchall()
        cur.close()
        return resultados

    def obtener_cliente_por_dni(self, dni):
        """Busca un cliente específico por su número de identificación."""
        try:

            # El parámetro buffered=True es la clave para evitar "Unread result found"
            cur = self.conexion.cursor(buffered=True) 
            cur.execute("SELECT * FROM clientes WHERE Numero_Identificacion = %s", (dni,))
            resultado = cur.fetchone()
            cur.close()
            return resultado
        except Exception as e:
            print(f"Error al buscar por identificación: {e}")
            return None

    def obtener_cliente_por_id(self, id_cliente):
        """Busca un cliente específico por su ID."""
        try:
            cur = self.conexion.cursor(buffered=True)
            cur.execute("SELECT * FROM clientes WHERE Id_Cliente = %s", (id_cliente,))
            resultado = cur.fetchone()
            cur.close()
            return resultado
        except Exception as e:
            print(f"Error al buscar por ID: {e}")
            return None

    def actualizar_clientes(self, id, nombre, dni, Tel, email, fecha_nac, nivel, tarjeta):
        """Actualiza la información de un cliente existente mediante su ID.

        El nivel de cliente puede ser modificado (por admin) y, si se actualiza a VIP,
        se almacena la fecha en `Fecha_VIP`.
        """
        # Obtener datos actuales para detectar cambios de nivel
        cur = self.conexion.cursor(buffered=True)
        cur.execute("SELECT Nivel_Cliente, Fecha_VIP FROM clientes WHERE Id_Cliente = %s", (id,))
        prev = cur.fetchone() or (None, None)
        nivel_prev, fecha_vip_prev = prev

        nueva_fecha_vip = fecha_vip_prev
        if nivel_prev != 'VIP' and nivel == 'VIP':
            nueva_fecha_vip = 'NOW()'
        elif nivel != 'VIP':
            nueva_fecha_vip = None

        sql = ("UPDATE clientes SET Nombre_Completo=%s, Numero_Identificacion=%s, Telefono=%s, Correo_Electronico=%s, "
               "Fecha_Nacimiento=%s, Nivel_Cliente=%s, Numero_Tarjeta=%s, Fecha_VIP=" + ("NOW()" if nueva_fecha_vip == 'NOW()' else "%s") + " WHERE Id_Cliente = %s")

        params = [nombre, dni, Tel, email, fecha_nac, nivel, tarjeta]
        if nueva_fecha_vip == 'NOW()':
            # ya está en la query con NOW()
            params.append(id)
        else:
            params.extend([nueva_fecha_vip, id])

        cur.execute(sql, tuple(params))
        self.conexion.commit()
        cur.close()
        
    def buscar_por_tarjeta(self, numero_tarjeta):
        """Busca si una tarjeta existe en la base de datos (independientemente del nivel)."""
        try:
           # Buffered=True permite que después de esta consulta puedas hacer un INSERT o UPDATE
            cur = self.conexion.cursor(buffered=True)
            cur.execute("SELECT * FROM clientes WHERE Numero_Tarjeta = %s", (numero_tarjeta,))
            resultado = cur.fetchone()
            cur.close()
            return resultado
        except Exception as e:
            print(f"Error al buscar por tarjeta: {e}")
            return None
        
    def buscar_tarjeta_por_nivel(self, numero_tarjeta, nivel):
        """Lógica especial: Busca si existe la tarjeta específicamente en un nivel (Clasica/VIP)."""
        try:
            cur = self.conexion.cursor(buffered=True)
            # El operador AND asegura que se cumplan ambas condiciones
            sql = "SELECT * FROM clientes WHERE Numero_Tarjeta = %s AND Nivel_Cliente = %s"
            cur.execute(sql, (numero_tarjeta, nivel))
            resultado = cur.fetchone()
            cur.close() 
            return resultado
        except Exception as e:
            print(f"Error en búsqueda por nivel: {e}")
            return None
        
    def registrar_asistencia(self, dni):
        """Registra una asistencia para el cliente identificado por DNI.

        Devuelve un dict con información de la asistencia y el nivel actual.
        """
        cliente = self.obtener_cliente_por_dni(dni)
        if not cliente:
            return None

        id_cliente = cliente[0]
        nivel_actual = cliente[6]

        try:
            cur = self.conexion.cursor()
            cur.execute("INSERT INTO asistencias (Id_Cliente) VALUES (%s)", (id_cliente,))
            self.conexion.commit()

            cur.execute(
                "SELECT COUNT(*) FROM asistencias WHERE Id_Cliente = %s AND YEAR(Fecha_Asistencia)=YEAR(CURDATE()) AND MONTH(Fecha_Asistencia)=MONTH(CURDATE())",
                (id_cliente,)
            )
            visitas_mes = cur.fetchone()[0] or 0

            nuevo_nivel = nivel_actual
            if visitas_mes >= 15 and nivel_actual != 'VIP':
                cur.execute("UPDATE clientes SET Nivel_Cliente='VIP' WHERE Id_Cliente = %s", (id_cliente,))
                self.conexion.commit()
                nuevo_nivel = 'VIP'

            cur.close()
            return {
                'id_cliente': id_cliente,
                'visitas_mes': visitas_mes,
                'nivel': nuevo_nivel,
            }
        except Exception as e:
            print(f"Error al registrar asistencia: {e}")
            return None

    def contar_visitas_distintas(self, periodo='dia'):
        """Cuenta cuántos clientes diferentes ingresaron en el periodo especificado."""
        sql = "SELECT COUNT(DISTINCT Id_Cliente) FROM asistencias"
        params = []

        if periodo == 'dia':
            sql += " WHERE DATE(Fecha_Asistencia)=CURDATE()"
        elif periodo == 'mes':
            sql += " WHERE YEAR(Fecha_Asistencia)=YEAR(CURDATE()) AND MONTH(Fecha_Asistencia)=MONTH(CURDATE())"
        elif periodo == 'anio':
            sql += " WHERE YEAR(Fecha_Asistencia)=YEAR(CURDATE())"

        cur = self.conexion.cursor()
        cur.execute(sql, params)
        resultado = cur.fetchone()[0] or 0
        cur.close()
        return resultado

    def contar_clientes_registrados(self, periodo='dia'):
        """Cuenta cuántos clientes fueron registrados en el periodo especificado."""
        sql = "SELECT COUNT(*) FROM clientes"
        if periodo == 'dia':
            sql += " WHERE DATE(Fecha_Registro)=CURDATE()"
        elif periodo == 'mes':
            sql += " WHERE YEAR(Fecha_Registro)=YEAR(CURDATE()) AND MONTH(Fecha_Registro)=MONTH(CURDATE())"
        elif periodo == 'anio':
            sql += " WHERE YEAR(Fecha_Registro)=YEAR(CURDATE())"

        cur = self.conexion.cursor()
        cur.execute(sql)
        resultado = cur.fetchone()[0] or 0
        cur.close()
        return resultado

    def contar_visitas_por_nivel(self, nivel, periodo='dia'):
        """Cuenta cuántos clientes con un nivel específico realizaron al menos una visita en el periodo."""
        sql = ("SELECT COUNT(DISTINCT a.Id_Cliente) FROM asistencias a "
               "JOIN clientes c ON a.Id_Cliente = c.Id_Cliente")

        if periodo == 'dia':
            sql += " WHERE DATE(a.Fecha_Asistencia)=CURDATE()"
        elif periodo == 'mes':
            sql += " WHERE YEAR(a.Fecha_Asistencia)=YEAR(CURDATE()) AND MONTH(a.Fecha_Asistencia)=MONTH(CURDATE())"
        elif periodo == 'anio':
            sql += " WHERE YEAR(a.Fecha_Asistencia)=YEAR(CURDATE())"

        sql += " AND c.Nivel_Cliente = %s"

        cur = self.conexion.cursor()
        cur.execute(sql, (nivel,))
        resultado = cur.fetchone()[0] or 0
        cur.close()
        return resultado

    def contar_vip_convertidos(self, periodo='dia'):
        """Cuenta cuántos clientes alcanzaron VIP por fecha de conversión."""
        sql = "SELECT COUNT(*) FROM clientes WHERE Fecha_VIP IS NOT NULL"
        if periodo == 'dia':
            sql += " AND DATE(Fecha_VIP)=CURDATE()"
        elif periodo == 'mes':
            sql += " AND YEAR(Fecha_VIP)=YEAR(CURDATE()) AND MONTH(Fecha_VIP)=MONTH(CURDATE())"
        elif periodo == 'anio':
            sql += " AND YEAR(Fecha_VIP)=YEAR(CURDATE())"

        cur = self.conexion.cursor()
        cur.execute(sql)
        resultado = cur.fetchone()[0] or 0
        cur.close()
        return resultado
