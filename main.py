import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import os

# Importar módulos de la aplicación
from ui.login_window import mostrar_login
from ui.main_window import mostrar_ventana_principal
from database.db_manager import reiniciar_base_datos


def main():
    """Función principal que inicia la aplicación"""
    # Configurar tema y crear ventana principal
    root = tb.Window(themename="flatly")
    root.title("Sistema de Fotomultas DASU")
    root.geometry("950x700")
    root.minsize(800, 600)  # Tamaño mínimo para asegurar usabilidad

    # Oculta la ventana principal hasta que se complete el login
    root.withdraw()

    # Verificar directorios necesarios
    verificar_directorios()

    def iniciar_app():
        """Función que se ejecuta después del login exitoso"""
        # Mostrar ventana principal
        root.deiconify()

        # Reiniciar base de datos (comentar después del primer uso)
        """reiniciar_base_datos()"""

        # Mostrar ventana principal con la nueva interfaz
        mostrar_ventana_principal(root)

    # Mostrar ventana de login
    mostrar_login(root, iniciar_app)

    # Iniciar el bucle principal
    root.mainloop()


def verificar_directorios():
    """Verifica que existan los directorios necesarios"""
    # Directorio de datos
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Directorio de imágenes
    images_dir = os.path.join(os.getcwd(), "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Directorio de exportaciones
    exports_dir = os.path.join(os.getcwd(), "exports")
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)


if __name__ == "__main__":
    main()