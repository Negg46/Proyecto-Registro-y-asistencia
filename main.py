import random
import string
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from Conexion import Registro_datos


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


class SistemaLogin:
    def __init__(self):
        self.usuarios = {'admin': {'password': '1234', 'rol': 'admin'}}
        self.paleta = {
            'fondo': '#08090c',
            'panel': '#111318',
            'panel_secundario': '#171a21',
            'panel_terciario': '#1d212a',
            'borde': '#2a2f3a',
            'acento': '#c71f37',
            'acento_hover': '#94162b',
            'oro': '#d9b15f',
            'texto': '#f4f5f7',
            'texto_suave': '#9ea7b3',
            'exito': '#6fd3c1',
            'info': '#7bb4ff'
        }
        self.ventana = ctk.CTk(fg_color=self.paleta['fondo'])
        self.ventana.title('Casino La Rioja')
        self._maximizar(self.ventana)
        self.registro_casino = Registro_datos()
        self._cargar_fondo_base()
        self.crear_login()
        self.ventana.mainloop()

    def _maximizar(self, ventana):
        ventana.update_idletasks()
        ventana.after(0, lambda: ventana.state('zoomed'))

    def _cargar_fondo_base(self):
        try:
            self.img_pil = Image.open('fondo.jpeg')
        except Exception:
            self.img_pil = None

    def _aplicar_fondo(self, ventana, atributo_imagen):
        if not self.img_pil:
            ventana.configure(fg_color=self.paleta['fondo'])
            return

        imagen = ctk.CTkImage(
            light_image=self.img_pil,
            dark_image=self.img_pil,
            size=(ventana.winfo_screenwidth(), ventana.winfo_screenheight())
        )
        setattr(self, atributo_imagen, imagen)
        label_fondo = ctk.CTkLabel(ventana, image=imagen, text='')
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        ventana.image_ref = imagen

        overlay = ctk.CTkFrame(ventana, fg_color='#05060add', corner_radius=0)
        overlay.place(x=0, y=0, relwidth=1, relheight=1)

    def _crear_boton_volver(self, ventana, comando):
        boton = ctk.CTkButton(
            ventana,
            text='<',
            width=46,
            height=36,
            font=('Bahnschrift', 20, 'bold'),
            fg_color=self.paleta['panel'],
            hover_color=self.paleta['acento'],
            border_width=1,
            border_color=self.paleta['borde'],
            text_color=self.paleta['texto'],
            corner_radius=12,
            command=comando
        )
        boton.place(x=24, y=22)

    def _crear_tarjeta_resumen(self, parent, titulo, valor, descripcion, color_texto=None):
        tarjeta = ctk.CTkFrame(
            parent,
            fg_color=self.paleta['panel_secundario'],
            border_color=self.paleta['borde'],
            border_width=1,
            corner_radius=18
        )
        tarjeta.pack(side='left', fill='x', expand=True, padx=8)
        ctk.CTkLabel(tarjeta, text=titulo, font=('Segoe UI', 12, 'bold'), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=18, pady=(16, 4))
        ctk.CTkLabel(tarjeta, text=str(valor), font=('Bahnschrift', 30, 'bold'), text_color=color_texto or self.paleta['texto']).pack(anchor='w', padx=18)
        ctk.CTkLabel(tarjeta, text=descripcion, font=('Segoe UI', 11), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=18, pady=(4, 16))
        return tarjeta

    def _formatear_fecha(self, valor):
        return valor.strftime('%d/%m/%Y') if hasattr(valor, 'strftime') else str(valor)

    def _formatear_hora(self, valor):
        return valor.strftime('%H:%M:%S') if hasattr(valor, 'strftime') else str(valor)

    def crear_login(self):
        self._aplicar_fondo(self.ventana, 'img_fondo_login')

        contenedor = ctk.CTkFrame(
            self.ventana,
            fg_color='#0b0d12',
            border_color='#2d323d',
            border_width=1,
            corner_radius=28,
            width=1120,
            height=650
        )
        contenedor.place(relx=0.5, rely=0.5, anchor='center')
        contenedor.pack_propagate(False)

        lado_izquierdo = ctk.CTkFrame(contenedor, fg_color='#12151c', corner_radius=24, width=560)
        lado_izquierdo.pack(side='left', fill='both', padx=18, pady=18)
        lado_izquierdo.pack_propagate(False)

        lado_derecho = ctk.CTkFrame(contenedor, fg_color='#0d1016', corner_radius=24, width=470)
        lado_derecho.pack(side='left', fill='both', padx=(0, 18), pady=18)
        lado_derecho.pack_propagate(False)

        ctk.CTkLabel(lado_izquierdo, text='CASINO LA RIOJA', font=('Bahnschrift', 40, 'bold'), text_color=self.paleta['oro']).pack(anchor='w', padx=34, pady=(42, 10))
        ctk.CTkLabel(lado_izquierdo, text='Control premium de acceso, clientes y asistencia diaria.', font=('Segoe UI', 18), text_color=self.paleta['texto'], wraplength=440, justify='left').pack(anchor='w', padx=34)
        ctk.CTkLabel(lado_izquierdo, text='Un dashboard pensado para revisar el movimiento del dia y el historial de cada cliente.', font=('Segoe UI', 13), text_color=self.paleta['texto_suave'], wraplength=430, justify='left').pack(anchor='w', padx=34, pady=(12, 26))

        estadisticas = self.registro_casino.obtener_estadisticas_dashboard()
        banda = ctk.CTkFrame(lado_izquierdo, fg_color='#161a22', corner_radius=18, border_width=1, border_color=self.paleta['borde'])
        banda.pack(fill='x', padx=28, pady=(6, 18))
        self._crear_tarjeta_resumen(banda, 'Clientes', estadisticas['total_clientes'], 'Base activa')
        self._crear_tarjeta_resumen(banda, 'Visitas hoy', estadisticas['visitas_hoy'], 'Entradas actuales', self.paleta['oro'])

        puntos = [
            'Dashboard diario con estadisticas y busqueda de clientes.',
            'Registro y actualizacion de datos con nivel Clasica y VIP.',
            'Datos demo listos para ver el sistema funcionando desde el primer inicio.'
        ]
        for texto in puntos:
            fila = ctk.CTkFrame(lado_izquierdo, fg_color='transparent')
            fila.pack(fill='x', padx=34, pady=8)
            ctk.CTkLabel(fila, text='|', font=('Bahnschrift', 24, 'bold'), text_color=self.paleta['acento']).pack(side='left', padx=(0, 10))
            ctk.CTkLabel(fila, text=texto, font=('Segoe UI', 14), text_color=self.paleta['texto']).pack(side='left')

        ctk.CTkLabel(lado_izquierdo, text='Acceso demo: usuario admin / clave 1234', font=('Segoe UI', 13, 'bold'), text_color=self.paleta['exito']).pack(anchor='w', padx=34, pady=(40, 10))

        ctk.CTkLabel(lado_derecho, text='Iniciar sesion', font=('Bahnschrift', 34, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=44, pady=(56, 8))
        ctk.CTkLabel(lado_derecho, text='Ingresa al panel de administracion del casino.', font=('Segoe UI', 14), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=44, pady=(0, 24))

        self.entry_usuario = ctk.CTkEntry(
            lado_derecho,
            width=360,
            height=48,
            fg_color=self.paleta['panel'],
            border_color=self.paleta['borde'],
            border_width=1,
            text_color=self.paleta['texto'],
            placeholder_text='Usuario',
            placeholder_text_color='#7e8591',
            font=('Segoe UI', 15)
        )
        self.entry_usuario.pack(padx=44, pady=(16, 12))

        self.entry_password = ctk.CTkEntry(
            lado_derecho,
            width=360,
            height=48,
            show='*',
            fg_color=self.paleta['panel'],
            border_color=self.paleta['borde'],
            border_width=1,
            text_color=self.paleta['texto'],
            placeholder_text='Contrasena',
            placeholder_text_color='#7e8591',
            font=('Segoe UI', 15)
        )
        self.entry_password.pack(padx=44, pady=12)

        ctk.CTkButton(
            lado_derecho,
            text='Ingresar al sistema',
            width=360,
            height=52,
            font=('Bahnschrift', 18, 'bold'),
            fg_color=self.paleta['acento'],
            hover_color=self.paleta['acento_hover'],
            text_color=self.paleta['texto'],
            corner_radius=16,
            command=self.validar_login
        ).pack(padx=44, pady=(26, 18))

        bloque = ctk.CTkFrame(lado_derecho, fg_color=self.paleta['panel'], corner_radius=18, border_width=1, border_color=self.paleta['borde'])
        bloque.pack(fill='x', padx=44, pady=(8, 0))
        ctk.CTkLabel(bloque, text='Recomendacion', font=('Segoe UI', 12, 'bold'), text_color=self.paleta['oro']).pack(anchor='w', padx=18, pady=(14, 4))
        ctk.CTkLabel(bloque, text='Usa el dashboard para revisar las asistencias por fecha y luego buscar el cliente que quieras analizar.', font=('Segoe UI', 12), text_color=self.paleta['texto_suave'], wraplength=320, justify='left').pack(anchor='w', padx=18, pady=(0, 16))

        self.entry_password.bind('<Return>', lambda _event: self.validar_login())

    def validar_login(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        if usuario in self.usuarios and self.usuarios[usuario]['password'] == password:
            self.usuario = usuario
            self.ventana.withdraw()
            self.ventana_admin()
        else:
            messagebox.showerror('Error', 'Usuario o contrasena incorrectos')

    def ventana_admin(self):
        admin = ctk.CTkToplevel(fg_color=self.paleta['fondo'])
        admin.title('Panel Administrador')
        self._maximizar(admin)
        self._aplicar_fondo(admin, 'img_fondo_admin')

        estadisticas = self.registro_casino.obtener_estadisticas_dashboard()

        panel = ctk.CTkFrame(admin, fg_color='#0b0d12', border_color=self.paleta['borde'], border_width=1, corner_radius=28)
        panel.place(relx=0.5, rely=0.52, anchor='center', relwidth=0.93, relheight=0.88)

        cabecera = ctk.CTkFrame(panel, fg_color='transparent')
        cabecera.pack(fill='x', padx=30, pady=(28, 18))
        ctk.CTkLabel(cabecera, text='Panel principal', font=('Bahnschrift', 34, 'bold'), text_color=self.paleta['texto']).pack(anchor='w')
        ctk.CTkLabel(cabecera, text='Administra clientes, revisa actividad diaria y consulta historicos con una vista ejecutiva.', font=('Segoe UI', 14), text_color=self.paleta['texto_suave']).pack(anchor='w', pady=(6, 0))

        fila_metricas = ctk.CTkFrame(panel, fg_color='transparent')
        fila_metricas.pack(fill='x', padx=22, pady=(0, 20))
        self._crear_tarjeta_resumen(fila_metricas, 'Clientes', estadisticas['total_clientes'], 'Registros disponibles')
        self._crear_tarjeta_resumen(fila_metricas, 'Visitas hoy', estadisticas['visitas_hoy'], 'Actividad del dia', self.paleta['oro'])
        self._crear_tarjeta_resumen(fila_metricas, 'Clientes unicos', estadisticas['clientes_unicos_hoy'], 'Asistencia individual', self.paleta['info'])
        self._crear_tarjeta_resumen(fila_metricas, 'VIP', estadisticas['total_vip'], f"Clasica: {estadisticas['total_clasica']}", self.paleta['exito'])

        cuerpo = ctk.CTkFrame(panel, fg_color='transparent')
        cuerpo.pack(fill='both', expand=True, padx=24, pady=(0, 24))

        acciones = ctk.CTkFrame(cuerpo, fg_color='transparent')
        acciones.pack(side='left', fill='both', expand=True, padx=(0, 12))

        lateral = ctk.CTkFrame(cuerpo, fg_color=self.paleta['panel_secundario'], border_color=self.paleta['borde'], border_width=1, corner_radius=22, width=350)
        lateral.pack(side='left', fill='both')
        lateral.pack_propagate(False)

        self._crear_tarjeta_accion(
            acciones,
            'Registrar cliente',
            'Agrega nuevos clientes con tarjeta y datos de contacto.',
            self.paleta['acento'],
            lambda: [admin.destroy(), self.Registro_Clientes()]
        )
        self._crear_tarjeta_accion(
            acciones,
            'Abrir dashboard',
            'Consulta asistencia por dia, top de clientes y detalle individual.',
            self.paleta['oro'],
            lambda: [admin.destroy(), self.reportes_clientes()]
        )
        self._crear_tarjeta_accion(
            acciones,
            'Actualizar cliente',
            'Busca por documento y corrige informacion existente.',
            self.paleta['info'],
            lambda: [admin.destroy(), self.seleccionar_cliente_para_actualizar()]
        )

        ctk.CTkLabel(lateral, text='Vista rapida', font=('Bahnschrift', 22, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=22, pady=(22, 8))
        ctk.CTkLabel(lateral, text='El sistema ya tiene datos demo para que puedas abrir el dashboard y ver el software con contenido.', font=('Segoe UI', 13), text_color=self.paleta['texto_suave'], wraplength=290, justify='left').pack(anchor='w', padx=22, pady=(0, 18))

        clientes_hoy = self.registro_casino.obtener_clientes_hoy(6)
        bloque_hoy = ctk.CTkScrollableFrame(lateral, fg_color=self.paleta['panel'], corner_radius=16, height=280)
        bloque_hoy.pack(fill='x', padx=18, pady=(0, 18))
        ctk.CTkLabel(bloque_hoy, text='Entradas del dia', font=('Segoe UI', 13, 'bold'), text_color=self.paleta['oro']).pack(anchor='w', padx=6, pady=(8, 8))
        for cliente in clientes_hoy:
            item = ctk.CTkFrame(bloque_hoy, fg_color=self.paleta['panel_terciario'], corner_radius=12)
            item.pack(fill='x', padx=4, pady=4)
            ctk.CTkLabel(item, text=cliente['nombre'], font=('Segoe UI', 12, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=12, pady=(10, 0))
            subtitulo = f"{cliente['nivel']} | {cliente['visitas_hoy']} visitas | Ultima: {self._formatear_hora(cliente['ultima_entrada'])}"
            ctk.CTkLabel(item, text=subtitulo, font=('Segoe UI', 11), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=12, pady=(2, 10))

        ctk.CTkButton(
            lateral,
            text='Cerrar sesion',
            height=46,
            fg_color='transparent',
            hover_color=self.paleta['acento'],
            border_width=1,
            border_color=self.paleta['borde'],
            text_color=self.paleta['texto'],
            font=('Bahnschrift', 16, 'bold'),
            corner_radius=14,
            command=lambda: [admin.destroy(), self.cerrar_sesion()]
        ).pack(fill='x', padx=18, pady=(6, 18))

    def _crear_tarjeta_accion(self, parent, titulo, descripcion, color, comando):
        tarjeta = ctk.CTkFrame(parent, fg_color=self.paleta['panel_secundario'], border_color=self.paleta['borde'], border_width=1, corner_radius=22)
        tarjeta.pack(fill='x', pady=10)
        barra = ctk.CTkFrame(tarjeta, fg_color=color, height=6, corner_radius=8)
        barra.pack(fill='x', padx=16, pady=(16, 18))
        ctk.CTkLabel(tarjeta, text=titulo, font=('Bahnschrift', 24, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=22)
        ctk.CTkLabel(tarjeta, text=descripcion, font=('Segoe UI', 13), text_color=self.paleta['texto_suave'], wraplength=600, justify='left').pack(anchor='w', padx=22, pady=(8, 18))
        ctk.CTkButton(
            tarjeta,
            text='Abrir',
            width=140,
            height=42,
            fg_color=color if color != self.paleta['oro'] else '#a67d29',
            hover_color=self.paleta['acento_hover'],
            text_color=self.paleta['texto'],
            font=('Bahnschrift', 16, 'bold'),
            corner_radius=14,
            command=comando
        ).pack(anchor='w', padx=22, pady=(0, 20))

    def cerrar_sesion(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.ventana.deiconify()
        self._maximizar(self.ventana)

    def Registro_Clientes(self, datos_cliente=None):
        self.registro = ctk.CTkToplevel(fg_color=self.paleta['fondo'])
        self.registro.title('Actualizar cliente' if datos_cliente else 'Registrar cliente')
        self._maximizar(self.registro)
        self._aplicar_fondo(self.registro, 'img_fondo_registro')
        self._crear_boton_volver(self.registro, lambda: [self.registro.destroy(), self.ventana_admin()])

        panel = ctk.CTkFrame(self.registro, fg_color='#0b0d12', border_color=self.paleta['borde'], border_width=1, corner_radius=28)
        panel.place(relx=0.5, rely=0.52, anchor='center', relwidth=0.84, relheight=0.82)

        izquierdo = ctk.CTkFrame(panel, fg_color=self.paleta['panel_secundario'], corner_radius=22, width=350)
        izquierdo.pack(side='left', fill='both', padx=20, pady=20)
        izquierdo.pack_propagate(False)

        derecho = ctk.CTkFrame(panel, fg_color=self.paleta['panel'], corner_radius=22)
        derecho.pack(side='left', fill='both', expand=True, padx=(0, 20), pady=20)

        titulo = 'Actualizar datos' if datos_cliente else 'Registro de cliente'
        subtitulo = 'Edita la informacion del cliente seleccionado.' if datos_cliente else 'Crea un nuevo registro y genera su tarjeta automaticamente.'
        ctk.CTkLabel(izquierdo, text=titulo, font=('Bahnschrift', 30, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=26, pady=(34, 8))
        ctk.CTkLabel(izquierdo, text=subtitulo, font=('Segoe UI', 13), text_color=self.paleta['texto_suave'], wraplength=270, justify='left').pack(anchor='w', padx=26, pady=(0, 24))

        badges = [
            'Nivel VIP automatico desde 15 dias asistidos.',
            'El dashboard ya tiene datos demo para pruebas.',
            'Todos los cambios impactan el panel de asistencias.'
        ]
        for texto in badges:
            item = ctk.CTkFrame(izquierdo, fg_color=self.paleta['panel'], corner_radius=14)
            item.pack(fill='x', padx=20, pady=6)
            ctk.CTkLabel(item, text=texto, font=('Segoe UI', 12), text_color=self.paleta['texto']).pack(anchor='w', padx=14, pady=12)

        form = ctk.CTkScrollableFrame(derecho, fg_color='transparent')
        form.pack(fill='both', expand=True, padx=26, pady=24)
        ctk.CTkLabel(form, text='Datos del cliente', font=('Bahnschrift', 28, 'bold'), text_color=self.paleta['oro']).pack(anchor='w', pady=(0, 10))

        def crear_campo(label_texto, placeholder):
            ctk.CTkLabel(form, text=label_texto, font=('Segoe UI', 13, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', pady=(10, 4))
            entry = ctk.CTkEntry(
                form,
                width=420,
                height=42,
                fg_color=self.paleta['panel_secundario'],
                border_color=self.paleta['borde'],
                border_width=1,
                text_color=self.paleta['texto'],
                placeholder_text=placeholder,
                placeholder_text_color='#7e8591',
                font=('Segoe UI', 14)
            )
            entry.pack(anchor='w', pady=(0, 4))
            return entry

        self.e_nombre = crear_campo('Nombre y apellido', 'Nombre completo')
        self.e_dni = crear_campo('Identificacion', 'Solo numeros')
        self.e_tel = crear_campo('Telefono de contacto', 'Ejemplo: 3511234567')
        self.e_email = crear_campo('Correo electronico', 'usuario@dominio.com')
        self.e_fecha_nac = crear_campo('Fecha de nacimiento', 'AAAA-MM-DD')

        if datos_cliente:
            self.e_nombre.insert(0, datos_cliente[1])
            self.e_dni.insert(0, datos_cliente[2])
            self.e_tel.insert(0, datos_cliente[3])
            self.e_email.insert(0, datos_cliente[4])
            self.e_fecha_nac.insert(0, str(datos_cliente[5]))

            ctk.CTkLabel(form, text='Nivel de tarjeta', font=('Segoe UI', 13, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', pady=(12, 4))
            self.e_nivel = ctk.CTkOptionMenu(
                form,
                width=260,
                height=40,
                values=['Clasica', 'VIP'],
                fg_color=self.paleta['panel_secundario'],
                button_color=self.paleta['acento'],
                button_hover_color=self.paleta['acento_hover'],
                text_color=self.paleta['texto'],
                font=('Segoe UI', 14, 'bold')
            )
            self.e_nivel.set(datos_cliente[6])
            self.e_nivel.pack(anchor='w', pady=(0, 4))

            self.e_num_tarjeta = crear_campo('Numero de tarjeta', 'Tarjeta')
            self.e_num_tarjeta.insert(0, datos_cliente[7])
            texto_boton = 'Guardar cambios'
            comando = lambda: self.procesar_actualizacion(datos_cliente[0])
        else:
            self.nivel_cliente = 'Clasica'
            texto_boton = 'Registrar cliente'
            comando = self.procesar_guardado

        ctk.CTkButton(
            form,
            text=texto_boton,
            width=320,
            height=50,
            fg_color=self.paleta['acento'],
            hover_color=self.paleta['acento_hover'],
            text_color=self.paleta['texto'],
            font=('Bahnschrift', 17, 'bold'),
            corner_radius=16,
            command=comando
        ).pack(anchor='w', pady=(24, 16))

    def procesar_guardado(self):
        nombre = self.e_nombre.get().strip()
        dni = self.e_dni.get().strip()
        tel = self.e_tel.get().strip()
        email = self.e_email.get().strip()
        fecha_nac = self.e_fecha_nac.get().strip()
        nivel = self.nivel_cliente

        if any(not campo for campo in [nombre, dni, tel, email, fecha_nac]):
            messagebox.showwarning('Atencion', 'Todos los campos son obligatorios.')
            return

        if '@' not in email or '.' not in email.split('@')[-1]:
            messagebox.showerror('Error', 'Formato de correo invalido.')
            return

        if not dni.isdigit():
            messagebox.showerror('Error', 'La identificacion debe ser numerica.')
            return

        try:
            if self.registro_casino.obtener_cliente_por_dni(dni):
                messagebox.showerror('Error', 'Ya existe un cliente con esta identificacion.')
                return

            while True:
                tarjeta = ''.join(random.choices(string.digits, k=8))
                if not self.registro_casino.buscar_tarjeta_por_nivel(tarjeta, nivel):
                    break

            self.registro_casino.inserta_producto(nombre, dni, tel, email, fecha_nac, nivel, tarjeta)
            messagebox.showinfo('Exito', f'Cliente registrado correctamente. Tarjeta generada: {tarjeta}')
            self.registro.destroy()
            self.ventana_admin()
        except Exception as error:
            messagebox.showerror('Error de base de datos', f'Detalle: {error}')

    def procesar_actualizacion(self, id_cliente):
        nombre = self.e_nombre.get().strip()
        dni = self.e_dni.get().strip()
        tel = self.e_tel.get().strip()
        email = self.e_email.get().strip()
        fecha_nac = self.e_fecha_nac.get().strip()
        nivel = self.e_nivel.get()
        tarjeta = self.e_num_tarjeta.get().strip()

        if any(not campo for campo in [nombre, dni, tel, email, fecha_nac, tarjeta]) or not nivel:
            messagebox.showwarning('Atencion', 'Todos los campos son obligatorios.')
            return

        if '@' not in email or '.' not in email.split('@')[-1]:
            messagebox.showerror('Error', 'Formato de correo invalido.')
            return

        if not dni.isdigit() or not tarjeta.isdigit():
            messagebox.showerror('Error', 'Identificacion y tarjeta deben ser numericas.')
            return

        cliente_con_dni = self.registro_casino.obtener_cliente_por_dni(dni)
        if cliente_con_dni and cliente_con_dni['id'] != id_cliente:
            messagebox.showerror('Error', 'Ya existe otro cliente con esta identificacion.')
            return

        cliente_con_tarjeta = self.registro_casino.buscar_tarjeta_por_nivel(tarjeta, nivel)
        if cliente_con_tarjeta and cliente_con_tarjeta[0] != id_cliente:
            messagebox.showerror('Error', f'La tarjeta {tarjeta} ya esta registrada en el nivel {nivel}.')
            return

        try:
            self.registro_casino.actualizar_clientes(id_cliente, nombre, dni, tel, email, fecha_nac, nivel, tarjeta)
            self.registro.destroy()
            self.ventana_admin()
        except Exception as error:
            messagebox.showerror('Error de base de datos', f'Detalle: {error}')

    def seleccionar_cliente_para_actualizar(self):
        ventana = ctk.CTkToplevel(fg_color=self.paleta['fondo'])
        ventana.title('Buscar cliente')
        self._maximizar(ventana)
        self._aplicar_fondo(ventana, 'img_fondo_busqueda')
        self._crear_boton_volver(ventana, lambda: [ventana.destroy(), self.ventana_admin()])

        panel = ctk.CTkFrame(ventana, fg_color='#0b0d12', border_color=self.paleta['borde'], border_width=1, corner_radius=28, width=860, height=520)
        panel.place(relx=0.5, rely=0.5, anchor='center')
        panel.pack_propagate(False)

        ctk.CTkLabel(panel, text='Buscar cliente', font=('Bahnschrift', 30, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=34, pady=(36, 8))
        ctk.CTkLabel(panel, text='Ingresa la identificacion del cliente para abrir su ficha editable.', font=('Segoe UI', 14), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=34, pady=(0, 24))

        entry_dni = ctk.CTkEntry(
            panel,
            width=380,
            height=46,
            fg_color=self.paleta['panel_secundario'],
            border_color=self.paleta['borde'],
            border_width=1,
            text_color=self.paleta['texto'],
            placeholder_text='Identificacion del cliente',
            font=('Segoe UI', 15)
        )
        entry_dni.pack(anchor='w', padx=34, pady=(0, 18))

        top_clientes = self.registro_casino.obtener_top_clientes(5)
        vista = ctk.CTkScrollableFrame(panel, fg_color=self.paleta['panel'], corner_radius=18, height=220)
        vista.pack(fill='x', padx=28, pady=(0, 18))
        ctk.CTkLabel(vista, text='Clientes destacados', font=('Segoe UI', 13, 'bold'), text_color=self.paleta['oro']).pack(anchor='w', padx=8, pady=(8, 10))
        for cliente in top_clientes:
            item = ctk.CTkFrame(vista, fg_color=self.paleta['panel_terciario'], corner_radius=12)
            item.pack(fill='x', padx=4, pady=4)
            ctk.CTkLabel(item, text=cliente['nombre'], font=('Segoe UI', 12, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=12, pady=(10, 0))
            detalle = f"{cliente['nivel']} | {cliente['total_dias']} dias asistidos | {cliente['total_registros']} registros"
            ctk.CTkLabel(item, text=detalle, font=('Segoe UI', 11), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=12, pady=(2, 10))

        def buscar():
            dni = entry_dni.get().strip()
            cliente = self.registro_casino.obtener_cliente_para_edicion(dni)
            if cliente:
                ventana.destroy()
                self.Registro_Clientes(datos_cliente=cliente)
            else:
                messagebox.showinfo('Info', 'No se encontro un cliente con esa identificacion.')

        ctk.CTkButton(
            panel,
            text='Buscar y editar',
            width=220,
            height=48,
            fg_color=self.paleta['acento'],
            hover_color=self.paleta['acento_hover'],
            text_color=self.paleta['texto'],
            font=('Bahnschrift', 16, 'bold'),
            corner_radius=14,
            command=buscar
        ).pack(anchor='w', padx=34)
        entry_dni.bind('<Return>', lambda _event: buscar())

    def reportes_clientes(self):
        ventana = ctk.CTkToplevel(fg_color=self.paleta['fondo'])
        ventana.title('Dashboard de asistencias')
        self._maximizar(ventana)
        self._aplicar_fondo(ventana, 'img_fondo_dashboard')
        self._crear_boton_volver(ventana, lambda: [ventana.destroy(), self.ventana_admin()])

        estadisticas = self.registro_casino.obtener_estadisticas_dashboard()
        historico = self.registro_casino.obtener_asistencias_ultimos_dias(7)
        top_clientes = self.registro_casino.obtener_top_clientes(5)
        clientes_hoy = self.registro_casino.obtener_clientes_hoy(8)

        panel = ctk.CTkFrame(ventana, fg_color='#0b0d12', border_color=self.paleta['borde'], border_width=1, corner_radius=28)
        panel.place(relx=0.5, rely=0.52, anchor='center', relwidth=0.95, relheight=0.90)

        ctk.CTkLabel(panel, text='Dashboard de asistencia', font=('Bahnschrift', 32, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=28, pady=(24, 6))
        ctk.CTkLabel(panel, text='Consulta el movimiento por fecha, observa el top de clientes y luego busca al cliente para ver su detalle diario.', font=('Segoe UI', 14), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=28, pady=(0, 18))

        fila_metricas = ctk.CTkFrame(panel, fg_color='transparent')
        fila_metricas.pack(fill='x', padx=20, pady=(0, 18))
        self._crear_tarjeta_resumen(fila_metricas, 'Clientes registrados', estadisticas['total_clientes'], 'Base general')
        self._crear_tarjeta_resumen(fila_metricas, 'Visitas hoy', estadisticas['visitas_hoy'], 'Entradas del dia', self.paleta['oro'])
        self._crear_tarjeta_resumen(fila_metricas, 'Clientes unicos hoy', estadisticas['clientes_unicos_hoy'], 'Personas diferentes', self.paleta['info'])
        self._crear_tarjeta_resumen(fila_metricas, 'Clientes VIP', estadisticas['total_vip'], f"Clasica: {estadisticas['total_clasica']}", self.paleta['exito'])

        cuerpo = ctk.CTkFrame(panel, fg_color='transparent')
        cuerpo.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        izquierda = ctk.CTkFrame(cuerpo, fg_color=self.paleta['panel_secundario'], border_color=self.paleta['borde'], border_width=1, corner_radius=22)
        izquierda.pack(side='left', fill='both', expand=True, padx=(0, 10))

        centro = ctk.CTkFrame(cuerpo, fg_color=self.paleta['panel_secundario'], border_color=self.paleta['borde'], border_width=1, corner_radius=22, width=390)
        centro.pack(side='left', fill='both', padx=(0, 10))
        centro.pack_propagate(False)

        derecha = ctk.CTkFrame(cuerpo, fg_color=self.paleta['panel_secundario'], border_color=self.paleta['borde'], border_width=1, corner_radius=22, width=430)
        derecha.pack(side='left', fill='both')
        derecha.pack_propagate(False)

        ctk.CTkLabel(izquierda, text='Asistencias por dia', font=('Bahnschrift', 24, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=22, pady=(20, 4))
        ctk.CTkLabel(izquierda, text='Ultimos 7 dias con total de visitas y clientes unicos.', font=('Segoe UI', 12), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=22, pady=(0, 10))

        canvas = tk.Canvas(izquierda, bg='#0d1016', highlightthickness=0, height=290)
        canvas.pack(fill='x', padx=20, pady=(0, 12))

        tabla_dias = ctk.CTkScrollableFrame(izquierda, fg_color='#0d1016', corner_radius=16, height=210)
        tabla_dias.pack(fill='both', expand=True, padx=20, pady=(0, 14))
        encabezado = ctk.CTkFrame(tabla_dias, fg_color=self.paleta['panel_terciario'], corner_radius=12)
        encabezado.pack(fill='x', padx=6, pady=(6, 8))
        for texto, ancho in [('Fecha', 110), ('Visitas', 80), ('Clientes unicos', 140)]:
            ctk.CTkLabel(encabezado, text=texto, width=ancho, anchor='w', font=('Segoe UI', 12, 'bold'), text_color=self.paleta['texto']).pack(side='left', padx=(12, 0), pady=10)

        for fila in historico:
            registro = ctk.CTkFrame(tabla_dias, fg_color=self.paleta['panel'], corner_radius=12)
            registro.pack(fill='x', padx=6, pady=4)
            ctk.CTkLabel(registro, text=self._formatear_fecha(fila['fecha']), width=110, anchor='w', text_color=self.paleta['texto']).pack(side='left', padx=(12, 0), pady=10)
            ctk.CTkLabel(registro, text=str(fila['total_visitas']), width=80, anchor='w', text_color=self.paleta['oro']).pack(side='left', padx=(12, 0), pady=10)
            ctk.CTkLabel(registro, text=str(fila['clientes_unicos']), width=140, anchor='w', text_color=self.paleta['info']).pack(side='left', padx=(12, 0), pady=10)

        def dibujar_grafico(_event=None):
            canvas.delete('all')
            ancho = max(canvas.winfo_width(), 620)
            alto = max(canvas.winfo_height(), 290)
            base_y = alto - 42
            margen_x = 48
            margen_superior = 24
            canvas.create_line(margen_x, base_y, ancho - margen_x, base_y, fill='#38404d', width=2)
            canvas.create_line(margen_x, margen_superior, margen_x, base_y, fill='#38404d', width=2)

            if not historico:
                canvas.create_text(ancho / 2, alto / 2, text='Sin asistencias registradas.', fill='#9ea7b3', font=('Segoe UI', 14))
                return

            maximo = max(fila['total_visitas'] for fila in historico) or 1
            paso = (ancho - (margen_x * 2)) / max(len(historico), 1)
            ancho_barra = min(54, paso * 0.55)

            for indice, fila in enumerate(historico):
                centro_x = margen_x + (paso * indice) + (paso / 2)
                altura = ((fila['total_visitas'] / maximo) * (base_y - margen_superior - 12))
                x0 = centro_x - (ancho_barra / 2)
                y0 = base_y - altura
                x1 = centro_x + (ancho_barra / 2)
                canvas.create_rectangle(x0, y0, x1, base_y, fill='#c71f37', outline='')
                canvas.create_text(centro_x, y0 - 12, text=str(fila['total_visitas']), fill='#f4f5f7', font=('Segoe UI', 10, 'bold'))
                canvas.create_text(centro_x, base_y + 16, text=fila['fecha'].strftime('%d/%m'), fill='#9ea7b3', font=('Segoe UI', 10))

        canvas.bind('<Configure>', dibujar_grafico)

        ctk.CTkLabel(centro, text='Ranking y actividad del dia', font=('Bahnschrift', 22, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=20, pady=(20, 6))
        ctk.CTkLabel(centro, text='Clientes con mayor asistencia y ultimos ingresos del dia.', font=('Segoe UI', 12), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=20, pady=(0, 10))

        top_frame = ctk.CTkScrollableFrame(centro, fg_color='#0d1016', corner_radius=16, height=220)
        top_frame.pack(fill='x', padx=18, pady=(0, 12))
        for indice, cliente in enumerate(top_clientes, start=1):
            item = ctk.CTkFrame(top_frame, fg_color=self.paleta['panel'], corner_radius=12)
            item.pack(fill='x', padx=4, pady=4)
            ctk.CTkLabel(item, text=f'{indice}. {cliente["nombre"]}', font=('Segoe UI', 12, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=12, pady=(10, 0))
            detalle = f"{cliente['nivel']} | {cliente['total_dias']} dias | {cliente['total_registros']} registros"
            ctk.CTkLabel(item, text=detalle, font=('Segoe UI', 11), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=12, pady=(2, 10))

        hoy_frame = ctk.CTkScrollableFrame(centro, fg_color='#0d1016', corner_radius=16, height=260)
        hoy_frame.pack(fill='both', expand=True, padx=18, pady=(0, 18))
        for cliente in clientes_hoy:
            item = ctk.CTkFrame(hoy_frame, fg_color=self.paleta['panel'], corner_radius=12)
            item.pack(fill='x', padx=4, pady=4)
            ctk.CTkLabel(item, text=cliente['nombre'], font=('Segoe UI', 12, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=12, pady=(10, 0))
            detalle = f"{cliente['nivel']} | {cliente['visitas_hoy']} visitas | Ultima entrada: {self._formatear_hora(cliente['ultima_entrada'])}"
            ctk.CTkLabel(item, text=detalle, font=('Segoe UI', 11), text_color=self.paleta['texto_suave']).pack(anchor='w', padx=12, pady=(2, 10))

        ctk.CTkLabel(derecha, text='Buscar cliente', font=('Bahnschrift', 24, 'bold'), text_color=self.paleta['texto']).pack(anchor='w', padx=20, pady=(20, 6))
        ctk.CTkLabel(derecha, text='Busca por nombre o identificacion y revisa sus asistencias del dia y su historico.', font=('Segoe UI', 12), text_color=self.paleta['texto_suave'], wraplength=360, justify='left').pack(anchor='w', padx=20, pady=(0, 10))

        buscador = ctk.CTkFrame(derecha, fg_color='transparent')
        buscador.pack(fill='x', padx=20, pady=(0, 12))
        entry_busqueda = ctk.CTkEntry(
            buscador,
            placeholder_text='Nombre o DNI',
            height=42,
            fg_color='#0d1016',
            border_color=self.paleta['borde'],
            border_width=1,
            text_color=self.paleta['texto'],
            font=('Segoe UI', 14)
        )
        entry_busqueda.pack(side='left', fill='x', expand=True, padx=(0, 8))
        resultados_busqueda = ctk.CTkScrollableFrame(derecha, fg_color='#0d1016', corner_radius=16, height=170)
        resultados_busqueda.pack(fill='x', padx=20, pady=(0, 12))

        detalle = ctk.CTkFrame(derecha, fg_color='#0d1016', corner_radius=16)
        detalle.pack(fill='both', expand=True, padx=20, pady=(0, 18))
        titulo_cliente = ctk.CTkLabel(detalle, text='Selecciona un cliente', font=('Bahnschrift', 22, 'bold'), text_color=self.paleta['texto'])
        titulo_cliente.pack(anchor='w', padx=16, pady=(16, 10))
        resumen_cliente = ctk.CTkFrame(detalle, fg_color='transparent')
        resumen_cliente.pack(fill='x', padx=16, pady=(0, 12))
        ctk.CTkLabel(detalle, text='Asistencia por dia', font=('Segoe UI', 13, 'bold'), text_color=self.paleta['oro']).pack(anchor='w', padx=16)
        historial_cliente = ctk.CTkScrollableFrame(detalle, fg_color=self.paleta['panel'], corner_radius=12, height=140)
        historial_cliente.pack(fill='x', padx=16, pady=(6, 12))
        ctk.CTkLabel(detalle, text='Movimientos de hoy', font=('Segoe UI', 13, 'bold'), text_color=self.paleta['info']).pack(anchor='w', padx=16)
        movimientos_hoy = ctk.CTkScrollableFrame(detalle, fg_color=self.paleta['panel'], corner_radius=12, height=110)
        movimientos_hoy.pack(fill='x', padx=16, pady=(6, 16))

        def limpiar(contenedor):
            for widget in contenedor.winfo_children():
                widget.destroy()

        def mostrar_detalle_cliente(cliente_id):
            cliente = self.registro_casino.obtener_resumen_cliente(cliente_id)
            asistencias = self.registro_casino.obtener_asistencias_por_dia_cliente(cliente_id)
            visitas_hoy = self.registro_casino.obtener_movimientos_hoy_cliente(cliente_id)

            titulo_cliente.configure(text=cliente['nombre'])
            limpiar(resumen_cliente)
            limpiar(historial_cliente)
            limpiar(movimientos_hoy)

            resumenes = [
                ('DNI', cliente['dni']),
                ('Nivel', cliente['nivel']),
                ('Tarjeta', cliente['tarjeta']),
                ('Dias asistidos', cliente['total_dias']),
                ('Registros totales', cliente['total_registros']),
                ('Visitas hoy', cliente['visitas_hoy'] or 0)
            ]
            for etiqueta, valor in resumenes:
                fila = ctk.CTkFrame(resumen_cliente, fg_color=self.paleta['panel'], corner_radius=10)
                fila.pack(fill='x', pady=3)
                ctk.CTkLabel(fila, text=etiqueta, font=('Segoe UI', 11, 'bold'), text_color=self.paleta['texto_suave']).pack(side='left', padx=12, pady=8)
                ctk.CTkLabel(fila, text=str(valor), font=('Segoe UI', 12), text_color=self.paleta['texto']).pack(side='right', padx=12, pady=8)

            if asistencias:
                for fila_dia in asistencias:
                    item = ctk.CTkFrame(historial_cliente, fg_color=self.paleta['panel_terciario'], corner_radius=10)
                    item.pack(fill='x', padx=4, pady=3)
                    ctk.CTkLabel(item, text=self._formatear_fecha(fila_dia['fecha']), text_color=self.paleta['texto']).pack(side='left', padx=12, pady=8)
                    ctk.CTkLabel(item, text=f"{fila_dia['visitas']} visitas", text_color=self.paleta['oro']).pack(side='right', padx=12, pady=8)
            else:
                ctk.CTkLabel(historial_cliente, text='Sin asistencias registradas.', text_color=self.paleta['texto_suave']).pack(anchor='w', padx=10, pady=10)

            if visitas_hoy:
                for movimiento in visitas_hoy:
                    item = ctk.CTkFrame(movimientos_hoy, fg_color=self.paleta['panel_terciario'], corner_radius=10)
                    item.pack(fill='x', padx=4, pady=3)
                    ctk.CTkLabel(item, text=f"Entrada a las {self._formatear_hora(movimiento['hora'])}", text_color=self.paleta['texto']).pack(anchor='w', padx=12, pady=8)
            else:
                ctk.CTkLabel(movimientos_hoy, text='Este cliente no tiene entradas hoy.', text_color=self.paleta['texto_suave']).pack(anchor='w', padx=10, pady=10)

        def buscar_clientes_dashboard():
            resultados = self.registro_casino.buscar_clientes(entry_busqueda.get().strip())
            limpiar(resultados_busqueda)
            if not resultados:
                ctk.CTkLabel(resultados_busqueda, text='No se encontraron clientes.', text_color=self.paleta['texto_suave']).pack(anchor='w', padx=10, pady=10)
                return

            for cliente in resultados:
                texto = f"{cliente['nombre']} | DNI {cliente['dni']} | {cliente['nivel']}"
                ctk.CTkButton(
                    resultados_busqueda,
                    text=texto,
                    height=40,
                    anchor='w',
                    fg_color=self.paleta['panel'],
                    hover_color=self.paleta['acento'],
                    text_color=self.paleta['texto'],
                    corner_radius=12,
                    command=lambda cliente_id=cliente['id']: mostrar_detalle_cliente(cliente_id)
                ).pack(fill='x', padx=6, pady=4)

            mostrar_detalle_cliente(resultados[0]['id'])

        ctk.CTkButton(
            buscador,
            text='Buscar',
            width=96,
            height=42,
            fg_color=self.paleta['acento'],
            hover_color=self.paleta['acento_hover'],
            text_color=self.paleta['texto'],
            font=('Bahnschrift', 15, 'bold'),
            corner_radius=12,
            command=buscar_clientes_dashboard
        ).pack(side='left')

        entry_busqueda.bind('<Return>', lambda _event: buscar_clientes_dashboard())
        buscar_clientes_dashboard()


if __name__ == '__main__':
    SistemaLogin()