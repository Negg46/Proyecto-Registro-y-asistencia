import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
from PIL import Image
from Conexion import Registro_datos

class SistemaLogin:
    def __init__(self):
        self.usuarios = {
            "admin": {"password": "1234", "rol": "admin"},
            "cajero": {"password": "1234", "rol": "cajero"}
        }
        self.lista_clientes = []
        self.usuario_activo = None
        self.rol_activo = None
        self.ventana = ctk.CTk()
        self.ventana.title("PANEL LOGIN")
        
        self.ventana.update_idletasks() 
        self.ventana.after(0, lambda: self.ventana.state('zoomed'))
        
        try:
            img_path = "fondo.jpeg" 
            self.img_pil = Image.open(img_path)
            self.img_fondo = ctk.CTkImage(
                light_image=self.img_pil,
                dark_image=self.img_pil,
                size=(self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight())
            )
            self.label_fondo = ctk.CTkLabel(self.ventana, image=self.img_fondo, text="")
            self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"No se pudo cargar la imagen: {e}")
            self.ventana.configure(fg_color="#141414")

        self.registro_casino = Registro_datos()
        self.crear_login()
        self.ventana.mainloop()

    def crear_login(self):
        self.frame_login = ctk.CTkFrame(
            self.ventana, 
            fg_color="#000000",
            width=500, 
            height=650, 
            border_color='red', 
            border_width=2
        )
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_login.pack_propagate(False)
        
        ctk.CTkLabel(self.frame_login, text="Casino la Rioja", 
                     text_color="#E60000", font=("Arial", 35, "bold")).pack(pady=(100, 40))

        ctk.CTkLabel(self.frame_login, text="Usuario", text_color="white", 
                     font=("Arial", 16)).pack(pady=5)
        self.entry_usuario = ctk.CTkEntry(self.frame_login, width=250, height=35, 
                                          fg_color="#1a1a1a", border_color="#1a1a1a", 
                                          text_color="white")
        self.entry_usuario.pack(pady=10)
        
        ctk.CTkLabel(self.frame_login, text="Contraseña", text_color="white", 
                     font=("Arial", 16)).pack(pady=5)
        self.entry_password = ctk.CTkEntry(self.frame_login, show="*", width=250, 
                                           height=35, fg_color="#1a1a1a", border_color="#1a1a1a", 
                                           text_color="white")
        self.entry_password.pack(pady=10)

        ctk.CTkButton(self.frame_login, text="Ingresar", font=("Arial", 16), fg_color="#000000", 
                      border_color="red", border_width=2, text_color="white", hover_color="red", width=200, height=45, 
                      command=self.validar_login).pack(pady=40)

    def validar_login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        if usuario in self.usuarios and self.usuarios[usuario]["password"] == password:
            self.usuario_activo = usuario
            self.rol_activo = self.usuarios[usuario]["rol"]
            self.ventana.withdraw()
            self.ventana_admin()
        else:
            messagebox.showerror("Error", "Datos incorrectos")

    def ventana_admin(self):
        admin = ctk.CTkToplevel()
        admin.title("Panel Administrador")
        admin.state('zoomed') 
        
        try:
            self.img_fondo_admin = ctk.CTkImage(
                light_image=self.img_pil,
                dark_image=self.img_pil,
                size=(admin.winfo_screenwidth(), admin.winfo_screenheight())
            )
            label_fondo = ctk.CTkLabel(admin, image=self.img_fondo_admin, text="")
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
            admin.image_ref = self.img_fondo_admin
        except Exception as e:
            admin.configure(fg_color="#141414")
        
        self.frame_admin = ctk.CTkFrame(admin, fg_color="#000000", width=500, 
                                        height=600, border_color="red", border_width=2)
        self.frame_admin.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_admin.pack_propagate(False)

        ctk.CTkLabel(self.frame_admin, text="PANEL ADMINISTRADOR", 
                     font=("Arial", 30, "bold"), text_color="red").pack(pady=(80, 50))

        ctk.CTkButton(self.frame_admin, text="Registro Clientes", 
                      width=250, height=45, font=("Arial", 16), fg_color="gold", 
                      text_color="black", hover_color="#DAA520", 
                      command=lambda: [admin.destroy(), self.Registro_Clientes()]).pack(pady=10)

        ctk.CTkButton(self.frame_admin, text="Ver Reportes", 
                      width=250, height=45, font=("Arial", 16), 
                      fg_color="gold", text_color="black", hover_color="#DAA520", 
                      command=lambda: [admin.destroy(), self.reportes_clientes()]).pack(pady=10)

        ctk.CTkButton(self.frame_admin, text="Actualizar Datos", 
                      width=250, height=45, font=("Arial",16), fg_color="gold", 
                      text_color="black", hover_color="#DAA520", 
                      command=lambda: [admin.destroy(), self.seleccionar_cliente_para_actualizar()]).pack(pady=10)

        ctk.CTkButton(self.frame_admin, text="Cerrar Sesión", width=250, 
                      height=45, font=("Arial", 16), fg_color="#000000", 
                      border_color="red", border_width=2, text_color="white", hover_color="red", 
                      command=lambda: [admin.destroy(), self.cerrar_sesion()]).pack(pady=30)

    def cerrar_sesion(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.ventana.deiconify()
        self.ventana.state('zoomed')

    def Registro_Clientes(self, datos_cliente=None):
        self.registro = ctk.CTkToplevel()
        title = "ACTUALIZAR DATOS" if datos_cliente else "PANEL REGISTRO DE CLIENTES"
        self.registro.title(title)
        self.registro.state('zoomed')

        try:
            self.img_fondo_reg = ctk.CTkImage(
                light_image=self.img_pil,
                dark_image=self.img_pil,
                size=(self.registro.winfo_screenwidth(), self.registro.winfo_screenheight())
            )
            label_fondo = ctk.CTkLabel(self.registro, image=self.img_fondo_reg, text="")
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
            self.registro.image_ref = self.img_fondo_reg
        except Exception as e:
            self.registro.configure(fg_color="#000000")
            
        btn_volver = ctk.CTkButton(
            self.registro, text="<", font=("Arial", 20, "bold"), width=50, height=30, 
            fg_color="#000000", border_color="red", border_width=1, hover_color="red", 
            command=lambda: [self.registro.destroy(), self.ventana_admin()]
        )
        btn_volver.place(x=20, y=20)

        frame_registro = ctk.CTkFrame(
            self.registro, fg_color="#000000", border_color="red", border_width=3, 
            width=550, height=775, corner_radius=0
        )
        frame_registro.place(relx=0.5, rely=0.5, anchor="center")
        frame_registro.pack_propagate(False)

        ctk.CTkLabel(frame_registro, text="Casino La Rioja - Registro", 
                     font=("Arial", 28, "bold"), text_color="red").pack(pady=(30, 20))

        def crear_campo(label_text):
            ctk.CTkLabel(frame_registro, text=label_text, font=("Arial", 14), text_color="white").pack(pady=(10, 2), padx=80, anchor="w")
            entry = ctk.CTkEntry(frame_registro, width=400, height=35, fg_color="#1a1a1a", border_color="#1a1a1a", text_color="white")
            entry.pack(pady=2, padx=80)
            return entry

        self.e_nombre = crear_campo("Nombre y Apellido:")
        self.e_dni = crear_campo("Identificación:")
        self.e_tel = crear_campo("Teléfono de Contacto:")
        self.e_email = crear_campo("Correo Electrónico:")
        self.e_fecha_nac = crear_campo("Fecha de Nacimiento (AAAA/MM/DD):")
        
        # El nivel de cliente se determina por la asistencia mensual (comienza como Clasica)
        self.e_num_tarjeta = crear_campo("Número de Tarjeta:")

        if datos_cliente:
            self.e_nombre.insert(0, datos_cliente[1])
            self.e_dni.insert(0, datos_cliente[2])
            self.e_tel.insert(0, datos_cliente[3])
            self.e_email.insert(0, datos_cliente[4])
            fecha_bd = datos_cliente[5]
            fecha_formateada = fecha_bd.strftime("%Y/%m/%d") if hasattr(fecha_bd, 'strftime') else str(fecha_bd)
            self.e_fecha_nac.insert(0, fecha_formateada)
            self.e_num_tarjeta.insert(0, datos_cliente[7])

            # Solo el admin puede editar el nivel de cliente
            if self.rol_activo == 'admin':
                ctk.CTkLabel(frame_registro, text="Nivel del Cliente:", font=("Arial", 14), text_color="white").pack(pady=(10, 2), padx=80, anchor="w")
                self.e_nivel = ctk.CTkOptionMenu(frame_registro, width=400, height=35, values=["Clasica", "VIP"], fg_color="#1a1a1a", button_color="red")
                self.e_nivel.pack(pady=2, padx=60)
                self.e_nivel.set(datos_cliente[6])

            texto_boton = "ACTUALIZAR DATOS"
            comando_boton = lambda: self.procesar_actualizacion(datos_cliente[0])
        else:
            texto_boton = "CONFIRMAR REGISTRO"
            comando_boton = self.procesar_guardado

        ctk.CTkButton(frame_registro, text=texto_boton, fg_color="red", hover_color="#8b0000",
                      width=400, height=50, font=("Arial", 16, "bold"), command=comando_boton).pack(pady=40)

    def procesar_guardado(self):
        # Obtener datos eliminando espacios accidentales
        nombre = self.e_nombre.get().strip()
        dni = self.e_dni.get().strip()
        tel = self.e_tel.get().strip()
        email = self.e_email.get().strip()
        fecha_nac = self.e_fecha_nac.get().strip()
        nivel = "Clasica"  # Nivel inicial por defecto; se actualiza automáticamente según asistencia mensual
        tarjeta = self.e_num_tarjeta.get().strip()

        # 1. Validar que no haya campos vacíos
        campos = [nombre, dni, tel, email, fecha_nac, tarjeta]
        if any(not campo for campo in campos):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        # 2. Validar formato de correo (debe tener @ y un punto después del @)
        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Error", "Formato de correo inválido (ejemplo: usuario@dominio.com)")
            return

        # 3. Validaciones de formato numérico (Original)
        if not dni.isdigit() or not tarjeta.isdigit():
            messagebox.showerror("Error", "Identificación y Tarjeta deben ser numéricos")
            return

        try:
            # 4. Verificar Identificación (Original)
            if self.registro_casino.obtener_cliente_por_dni(dni):
                messagebox.showerror("Error", "Ya existe un cliente con esta identificación")
                return

            # 5. Verificar Tarjeta (única en todo el sistema)
            if self.registro_casino.buscar_por_tarjeta(tarjeta):
                messagebox.showerror("Error", f"La tarjeta {tarjeta} ya está registrada")
                return

            # 6. Registro si todo está bien (Original)
            self.registro_casino.inserta_producto(nombre, dni, tel, email, fecha_nac, nivel, tarjeta)
            messagebox.showinfo("Éxito", "Cliente registrado correctamente")
        
            self.registro.destroy()
            self.ventana_admin()

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Detalle: {str(e)}")
            

    def procesar_actualizacion(self, id_cliente):
        nombre = self.e_nombre.get().strip()
        dni = self.e_dni.get().strip()
        tel = self.e_tel.get().strip()
        email = self.e_email.get().strip()
        fecha_nac = self.e_fecha_nac.get().strip()
        tarjeta = self.e_num_tarjeta.get().strip()

        # Nivel solo lo puede editar el admin; para otros roles usamos el nivel actual.
        if self.rol_activo == 'admin' and hasattr(self, 'e_nivel'):
            nivel = self.e_nivel.get()
        else:
            cliente_actual = self.registro_casino.obtener_cliente_por_id(id_cliente)
            nivel = cliente_actual[6] if cliente_actual else 'Clasica'

        # 1. Validar que no haya campos vacíos
        campos = [nombre, dni, tel, email, fecha_nac, tarjeta]
        if any(not campo for campo in campos):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        # 2. Validar formato de correo
        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Error", "Formato de correo inválido (ejemplo: usuario@dominio.com)")
            return

        # 3. Validaciones numéricas
        if not dni.isdigit() or not tarjeta.isdigit():
            messagebox.showerror("Error", "Identificación y Tarjeta deben ser numéricos")
            return

        # 4. Verificar Identificación (excluyendo el cliente actual)
        cliente_con_dni = self.registro_casino.obtener_cliente_por_dni(dni)
        if cliente_con_dni and cliente_con_dni[0] != id_cliente:
            messagebox.showerror("Error", "Ya existe otro cliente con esta identificación")
            return

        # 5. Verificar Tarjeta (única en todo el sistema, excluyendo al cliente actual)
        cliente_con_tarjeta = self.registro_casino.buscar_por_tarjeta(tarjeta)
        if cliente_con_tarjeta and cliente_con_tarjeta[0] != id_cliente:
            messagebox.showerror("Error", f"La tarjeta {tarjeta} ya está registrada por otro cliente")
            return

        try:
            self.registro_casino.actualizar_clientes(id_cliente, nombre, dni, tel, email, fecha_nac, nivel, tarjeta)
            messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            self.registro.destroy()
            self.ventana_admin()
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Detalle: {str(e)}")

    def seleccionar_cliente_para_actualizar(self):
        ventana_buscar = ctk.CTkToplevel()
        ventana_buscar.title("Buscar Cliente")
        ventana_buscar.state('zoomed')
    
        try:
            self.img_fondo_bus = ctk.CTkImage(
                light_image=self.img_pil,
                dark_image=self.img_pil,
                size=(ventana_buscar.winfo_screenwidth(), ventana_buscar.winfo_screenheight())
            )
            label_fondo = ctk.CTkLabel(ventana_buscar, image=self.img_fondo_bus, text="")
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
            ventana_buscar.image_ref = self.img_fondo_bus
        except:
            ventana_buscar.configure(fg_color="#000000")

        ctk.CTkButton(ventana_buscar, text="<", font=("Arial", 20, "bold"), width=50, height=30, 
                      fg_color="#000000", border_color="red", border_width=1, 
                      command=lambda: [ventana_buscar.destroy(), self.ventana_admin()]).place(x=20, y=20)
        
        frame_buscar = ctk.CTkFrame(ventana_buscar, fg_color="#000000", border_color="red", border_width=2, width=500, height=400)
        frame_buscar.place(relx=0.5, rely=0.5, anchor="center")
        frame_buscar.pack_propagate(False)

        ctk.CTkLabel(frame_buscar, text="Buscar Cliente", font=("Arial", 23, "bold"), text_color="red").pack(pady=(100, 50))
        entry_dni = ctk.CTkEntry(frame_buscar, width=300, height=35, fg_color="#1a1a1a", border_color="red", text_color="white")
        entry_dni.pack(pady=10)

        def buscar():
            dni = entry_dni.get().strip()
            cliente = self.registro_casino.obtener_cliente_por_dni(dni)
            if cliente:
                ventana_buscar.destroy()
                self.Registro_Clientes(datos_cliente=cliente)
            else:
                messagebox.showinfo("Info", "No encontrado")

        ctk.CTkButton(frame_buscar, text="Buscar", width=300, height=40, fg_color="red", hover_color="#8b0000", command=buscar).pack(pady=20)

    def reportes_clientes(self):
        ventana_rep = ctk.CTkToplevel()
        ventana_rep.title("Reportes")
        ventana_rep.state('zoomed')
        
        try:
            self.img_fondo_rep = ctk.CTkImage(
                light_image=self.img_pil,
                dark_image=self.img_pil,
                size=(ventana_rep.winfo_screenwidth(), ventana_rep.winfo_screenheight())
            )
            label_fondo = ctk.CTkLabel(ventana_rep, image=self.img_fondo_rep, text="")
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
            ventana_rep.image_ref = self.img_fondo_rep
        except:
            ventana_rep.configure(fg_color="#000000")

        ctk.CTkButton(ventana_rep, text="<", font=("Arial", 20, "bold"), width=50, height=30, 
                      fg_color="#000000", border_color="red", border_width=1, 
                      command=lambda: [ventana_rep.destroy(), self.ventana_admin()]).place(x=20, y=20)

        # --- Resumen de actividad ---
        visitas_dia = self.registro_casino.contar_visitas_distintas('dia')
        visitas_mes = self.registro_casino.contar_visitas_distintas('mes')
        visitas_anio = self.registro_casino.contar_visitas_distintas('anio')

        registrados_dia = self.registro_casino.contar_clientes_registrados('dia')
        registrados_mes = self.registro_casino.contar_clientes_registrados('mes')
        registrados_anio = self.registro_casino.contar_clientes_registrados('anio')

        vip_dia = self.registro_casino.contar_visitas_por_nivel('VIP', 'dia')
        vip_mes = self.registro_casino.contar_visitas_por_nivel('VIP', 'mes')
        vip_anio = self.registro_casino.contar_visitas_por_nivel('VIP', 'anio')

        clasica_dia = self.registro_casino.contar_visitas_por_nivel('Clasica', 'dia')
        clasica_mes = self.registro_casino.contar_visitas_por_nivel('Clasica', 'mes')
        clasica_anio = self.registro_casino.contar_visitas_por_nivel('Clasica', 'anio')

        vip_conv_dia = self.registro_casino.contar_vip_convertidos('dia')
        vip_conv_mes = self.registro_casino.contar_vip_convertidos('mes')
        vip_conv_anio = self.registro_casino.contar_vip_convertidos('anio')

        resumen_text = (
            f"Hoy: {visitas_dia} clientes ingresaron (VIP: {vip_dia}, Clasica: {clasica_dia}) - "
            f"Registrados hoy: {registrados_dia} - Nuevos VIP hoy: {vip_conv_dia}\n"
            f"Este mes: {visitas_mes} clientes ingresaron (VIP: {vip_mes}, Clasica: {clasica_mes}) - "
            f"Registrados este mes: {registrados_mes} - Nuevos VIP mes: {vip_conv_mes}\n"
            f"Este año: {visitas_anio} clientes ingresaron (VIP: {vip_anio}, Clasica: {clasica_anio}) - "
            f"Registrados este año: {registrados_anio} - Nuevos VIP año: {vip_conv_anio}"
        )

        frame_resumen = ctk.CTkFrame(ventana_rep, fg_color="#000000", border_color="red", border_width=2)
        frame_resumen.place(relx=0.5, rely=0.12, anchor="n", width=1100, height=140)

        ctk.CTkLabel(frame_resumen, text="Resumen de actividad", font=("Arial", 20, "bold"), text_color="red").pack(pady=(10, 0))
        ctk.CTkLabel(frame_resumen, text=resumen_text, font=("Arial", 13), text_color="white", justify="left").pack(pady=(5, 10), padx=15)

        # --- Gráfico de registros por mes ---
        clientes_db = self.registro_casino.obtener_clientes()
        if not clientes_db:
            messagebox.showinfo("Reporte", "No hay datos")
            return

        canvas = tk.Canvas(ventana_rep, width=1200, height=600, bg="white")
        canvas.pack(pady=(190, 50))
        
        meses_nombres = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        conteo = {m: 0 for m in meses_nombres}
        
        for fila in clientes_db:
            try:
                f = fila[8]
                if isinstance(f, str): f = datetime.strptime(f[:10], "%Y-%m-%d")
                conteo[meses_nombres[f.month-1]] += 1
            except:
                continue

        x, base_y = 100, 500
        valores = list(conteo.values())
        max_v = max(valores) if any(valores) else 1
        
        for mes, total in conteo.items():
            h = (total/max_v)*400
            canvas.create_rectangle(x, base_y-h, x+60, base_y, fill="red")
            canvas.create_text(x+30, base_y+20, text=mes)
            canvas.create_text(x+30, base_y-h-10, text=str(total))
            x += 90

if __name__ == "__main__":
    SistemaLogin()