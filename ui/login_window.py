import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import os

# Simulación de credenciales
USUARIOS = {
    "Admin": "admin123",
    "dasu": "seguridad2025"
}


def mostrar_login(root, on_success):
    # Crear ventana de login
    ventana_login = tb.Toplevel(root)
    ventana_login.title("Sistema de Fotomultas DASU - Acceso")
    ventana_login.geometry("400x450")
    ventana_login.resizable(False, False)
    ventana_login.grab_set()

    # Centrar la ventana
    ventana_login.update_idletasks()
    ancho = ventana_login.winfo_width()
    alto = ventana_login.winfo_height()
    x = (ventana_login.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_login.winfo_screenheight() // 2) - (alto // 2)
    ventana_login.geometry(f'{ancho}x{alto}+{x}+{y}')

    # Contenedor principal con padding
    main_frame = tb.Frame(ventana_login, padding=25)
    main_frame.pack(fill="both", expand=True)

    # Logo superior
    logo_frame = tb.Frame(main_frame)
    logo_frame.pack(fill="x", pady=(0, 20))

    logo_label = tb.Label(
        logo_frame,
        text="🐺",
        font=("Arial", 48),
        bootstyle="info"
    )
    logo_label.pack()

    # Título
    titulo_label = tb.Label(
        main_frame,
        text="Sistema de Fotomultas",
        font=("Helvetica", 18, "bold"),
        bootstyle="info"
    )
    titulo_label.pack(pady=(0, 5))

    # Subtítulo
    subtitulo_label = tb.Label(
        main_frame,
        text="Dirección de Apoyo y Seguridad Universitaria",
        font=("Helvetica", 10),
        bootstyle="secondary"
    )
    subtitulo_label.pack(pady=(0, 30))

    # Formulario de acceso
    form_frame = tb.Frame(main_frame)
    form_frame.pack(fill="x")

    # Campo de usuario
    user_frame = tb.Frame(form_frame)
    user_frame.pack(fill="x", pady=(0, 15))

    tb.Label(
        user_frame,
        text="Usuario:",
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    entrada_usuario = tb.Entry(user_frame, font=("Helvetica", 11))
    entrada_usuario.pack(fill="x", ipady=5)
    entrada_usuario.focus_set()  # Enfoque inicial

    # Campo de contraseña
    password_frame = tb.Frame(form_frame)
    password_frame.pack(fill="x", pady=(0, 20))

    tb.Label(
        password_frame,
        text="Contraseña:",
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    entrada_contrasena = tb.Entry(password_frame, show="•", font=("Helvetica", 11))
    entrada_contrasena.pack(fill="x", ipady=5)

    # Contenedor para mensaje de error
    error_frame = tb.Frame(form_frame)
    error_frame.pack(fill="x", pady=(0, 15))

    error_label = tb.Label(
        error_frame,
        text="",
        font=("Helvetica", 9),
        bootstyle="danger",
        justify="center"
    )
    error_label.pack(fill="x")

    # Botón de acceso
    button_frame = tb.Frame(form_frame)
    button_frame.pack(fill="x", pady=(0, 20))

    def verificar_login(event=None):  # Parámetro event para el binding con Enter
        usuario = entrada_usuario.get().strip()
        contra = entrada_contrasena.get().strip()

        if not usuario or not contra:
            error_label.config(text="Por favor, complete todos los campos")
            return

        if USUARIOS.get(usuario) == contra:
            ventana_login.destroy()
            on_success()
        else:
            error_label.config(text="Usuario o contraseña incorrectos")
            entrada_contrasena.delete(0, tb.END)
            entrada_contrasena.focus_set()

    boton_acceso = tb.Button(
        button_frame,
        text="Iniciar sesión",
        command=verificar_login,
        bootstyle="info",
        width=20
    )
    boton_acceso.pack(ipady=5)

    # Línea divisoria
    separator = tb.Separator(form_frame)
    separator.pack(fill="x", pady=15)

    # Pie de página
    footer_label = tb.Label(
        form_frame,
        text="© 2025 - DASU\nTodos los derechos reservados",
        font=("Helvetica", 9),
        bootstyle="secondary",
        justify="center"
    )
    footer_label.pack(fill="x")

    # Bindings
    entrada_usuario.bind("<Return>", lambda e: entrada_contrasena.focus_set())
    entrada_contrasena.bind("<Return>", verificar_login)

    # Verificar directorio de datos
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)