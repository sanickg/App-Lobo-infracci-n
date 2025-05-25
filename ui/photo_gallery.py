import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
from database.db_manager import conectar_db, obtener_registro_por_id
import shutil


class GaleriaFotos:
    def __init__(self, parent):
        self.parent = parent
        self.images_dir = os.path.join(os.getcwd(), "images")

        # Crear directorio de imágenes si no existe
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

        # Lista para almacenar referencias a las imágenes
        self.photo_references = []

        # Extensiones de archivo soportadas
        self.supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')

    def mostrar_galeria(self, id_registro=None):
        """Muestra la galería de fotos de infracciones"""
        # Crear ventana de galería
        ventana = tb.Toplevel(self.parent)
        ventana.title("Galería de Fotomultas")
        ventana.geometry("1000x700")
        ventana.resizable(True, True)

        # Centrar la ventana
        ventana.transient(self.parent)
        ventana.grab_set()

        # Contenedor principal con scrollbar
        main_frame = tb.Frame(ventana, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Header con información
        header_frame = tb.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 15))

        titulo = "Galería de Fotomultas"
        subtitulo = ""

        # Si se proporciona un ID, mostrar información específica
        if id_registro:
            registro = obtener_registro_por_id(id_registro)
            if registro:
                titulo = f"Infracción #{id_registro} - Placa: {registro['numero_placa']}"
                subtitulo = f"Fecha: {registro['fecha']} - Velocidad: {registro['velocidad']} km/h"
                if registro['ubicacion']:
                    subtitulo += f" - Ubicación: {registro['ubicacion']}"

        # Título principal
        tb.Label(
            header_frame,
            text=titulo,
            font=("Helvetica", 18, "bold"),
            bootstyle="info"
        ).pack(anchor="w")

        # Subtítulo si existe
        if subtitulo:
            tb.Label(
                header_frame,
                text=subtitulo,
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(anchor="w", pady=(5, 0))

        # Separador
        tb.Separator(main_frame, orient="horizontal").pack(fill="x", pady=(0, 15))

        # Contenedor de la galería con scrollbars
        gallery_container = tb.Frame(main_frame)
        gallery_container.pack(fill="both", expand=True, pady=(0, 15))

        # Canvas para scrolling
        canvas = tb.Canvas(gallery_container, background="#f8f9fa")

        # Scrollbars
        v_scrollbar = tb.Scrollbar(gallery_container, orient="vertical", command=canvas.yview, bootstyle="info-round")
        h_scrollbar = tb.Scrollbar(gallery_container, orient="horizontal", command=canvas.xview, bootstyle="info-round")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Empaquetar scrollbars y canvas
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame para las imágenes dentro del canvas
        gallery_frame = tb.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=gallery_frame, anchor="nw")

        # Cargar y mostrar imágenes
        self._cargar_imagenes(gallery_frame, id_registro, ventana)

        # Configurar scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Ajustar ancho del frame al canvas
            canvas_width = canvas.winfo_width()
            if gallery_frame.winfo_reqwidth() < canvas_width:
                canvas.itemconfig(canvas_window, width=canvas_width)

        gallery_frame.bind("<Configure>", configure_scroll_region)

        # Scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Frame para botones
        buttons_frame = tb.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))

        # Botón para agregar imágenes
        tb.Button(
            buttons_frame,
            text="📁 Agregar Imagen",
            command=lambda: self._agregar_imagen(gallery_frame, id_registro, ventana),
            bootstyle="success-outline",
            width=15
        ).pack(side="left", padx=(0, 10))

        # Botón para actualizar galería
        tb.Button(
            buttons_frame,
            text="🔄 Actualizar",
            command=lambda: self._actualizar_galeria(gallery_frame, id_registro, ventana),
            bootstyle="info-outline",
            width=15
        ).pack(side="left", padx=(0, 10))

        # Botón para cerrar
        tb.Button(
            buttons_frame,
            text="❌ Cerrar",
            command=ventana.destroy,
            bootstyle="secondary",
            width=15
        ).pack(side="right")

        # Configurar ventana para que se cierre con Escape
        ventana.bind("<Escape>", lambda e: ventana.destroy())

    def _cargar_imagenes(self, container, id_registro=None, ventana_parent=None):
        """Carga las imágenes en el contenedor"""
        # Limpiar el contenedor
        for widget in container.winfo_children():
            widget.destroy()

        # Limpiar referencias anteriores
        self.photo_references.clear()

        # Obtener imágenes
        imagenes = self._obtener_imagenes(id_registro)

        if not imagenes:
            # Mostrar mensaje si no hay imágenes
            no_images_frame = tb.Frame(container)
            no_images_frame.pack(fill="both", expand=True, pady=50)

            tb.Label(
                no_images_frame,
                text="📷 No hay imágenes disponibles",
                font=("Helvetica", 16),
                bootstyle="secondary"
            ).pack()

            tb.Label(
                no_images_frame,
                text="Haga clic en 'Agregar Imagen' para subir fotos",
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(pady=(10, 0))
            return

        # Configurar grid
        max_cols = 3
        current_row = 0
        current_col = 0

        for idx, img_info in enumerate(imagenes):
            img_path = img_info['path']
            img_name = img_info['name']

            try:
                # Cargar imagen
                img = Image.open(img_path)

                # Crear thumbnail manteniendo proporción
                img.thumbnail((280, 210), Image.Resampling.LANCZOS)

                # Convertir a PhotoImage
                photo = ImageTk.PhotoImage(img)
                self.photo_references.append(photo)

                # Frame para cada imagen
                img_frame = tb.LabelFrame(
                    container,
                    text=img_name,
                    padding=10,
                    bootstyle="info"
                )
                img_frame.grid(
                    row=current_row,
                    column=current_col,
                    padx=10,
                    pady=10,
                    sticky="nsew"
                )

                # Label para la imagen
                img_label = tb.Label(img_frame, image=photo, cursor="hand2")
                img_label.pack(pady=(0, 5))

                # Información de la imagen
                info_frame = tb.Frame(img_frame)
                info_frame.pack(fill="x")

                # Mostrar tamaño del archivo
                try:
                    file_size = os.path.getsize(img_path)
                    size_text = self._format_file_size(file_size)
                    tb.Label(
                        info_frame,
                        text=f"Tamaño: {size_text}",
                        font=("Helvetica", 8),
                        bootstyle="secondary"
                    ).pack(side="left")
                except:
                    pass

                # Botón para ver imagen completa
                tb.Button(
                    info_frame,
                    text="👁️ Ver",
                    command=lambda p=img_path, n=img_name: self._mostrar_imagen_completa(p, n, ventana_parent),
                    bootstyle="info-outline",
                    width=8
                ).pack(side="right")

                # Evento click en imagen para ver completa
                img_label.bind(
                    "<Button-1>",
                    lambda e, p=img_path, n=img_name: self._mostrar_imagen_completa(p, n, ventana_parent)
                )

                # Actualizar posición
                current_col += 1
                if current_col >= max_cols:
                    current_col = 0
                    current_row += 1

            except Exception as e:
                print(f"Error al cargar imagen {img_path}: {e}")
                # Mostrar frame de error
                error_frame = tb.LabelFrame(
                    container,
                    text=f"Error: {img_name}",
                    padding=10,
                    bootstyle="danger"
                )
                error_frame.grid(
                    row=current_row,
                    column=current_col,
                    padx=10,
                    pady=10,
                    sticky="nsew"
                )

                tb.Label(
                    error_frame,
                    text="❌ No se pudo cargar\nla imagen",
                    bootstyle="danger",
                    justify="center"
                ).pack()

                current_col += 1
                if current_col >= max_cols:
                    current_col = 0
                    current_row += 1

        # Configurar peso de las columnas y filas
        for i in range(max_cols):
            container.grid_columnconfigure(i, weight=1)
        for i in range(current_row + 1):
            container.grid_rowconfigure(i, weight=0)

    def _obtener_imagenes(self, id_registro=None):
        """Obtiene la lista de imágenes para mostrar"""
        imagenes = []

        if id_registro:
            # Obtener imagen específica del registro
            registro = obtener_registro_por_id(id_registro)
            if registro and registro['imagen_path']:
                img_path = os.path.join(self.images_dir, registro['imagen_path'])
                if os.path.exists(img_path):
                    imagenes.append({
                        'path': img_path,
                        'name': registro['imagen_path'],
                        'registro_id': id_registro
                    })
        else:
            # Obtener todas las imágenes del directorio
            try:
                for filename in os.listdir(self.images_dir):
                    if filename.lower().endswith(self.supported_formats):
                        img_path = os.path.join(self.images_dir, filename)
                        if os.path.isfile(img_path):
                            imagenes.append({
                                'path': img_path,
                                'name': filename,
                                'registro_id': None
                            })

                # Ordenar por nombre
                imagenes.sort(key=lambda x: x['name'])

            except OSError as e:
                print(f"Error al leer directorio de imágenes: {e}")

        return imagenes

    def _mostrar_imagen_completa(self, img_path, img_name, parent):
        """Muestra la imagen en tamaño completo"""
        try:
            # Crear ventana para imagen completa
            img_window = tb.Toplevel(parent)
            img_window.title(f"Imagen: {img_name}")
            img_window.geometry("800x600")
            img_window.resizable(True, True)
            img_window.transient(parent)

            # Frame principal
            main_frame = tb.Frame(img_window, padding=10)
            main_frame.pack(fill="both", expand=True)

            # Cargar imagen original
            img = Image.open(img_path)

            # Calcular tamaño máximo manteniendo proporción
            max_width, max_height = 750, 500
            img_width, img_height = img.size

            ratio = min(max_width / img_width, max_height / img_height)
            if ratio < 1:
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convertir a PhotoImage
            photo = ImageTk.PhotoImage(img)

            # Mostrar imagen
            img_label = tb.Label(main_frame, image=photo)
            img_label.pack(pady=(0, 10))

            # Información de la imagen
            info_frame = tb.Frame(main_frame)
            info_frame.pack(fill="x", pady=(0, 10))

            original_img = Image.open(img_path)
            file_size = os.path.getsize(img_path)

            info_text = f"Archivo: {img_name}\n"
            info_text += f"Dimensiones: {original_img.size[0]} x {original_img.size[1]} píxeles\n"
            info_text += f"Tamaño: {self._format_file_size(file_size)}"

            tb.Label(
                info_frame,
                text=info_text,
                font=("Helvetica", 10),
                bootstyle="secondary",
                justify="left"
            ).pack(anchor="w")

            # Botón cerrar
            tb.Button(
                main_frame,
                text="Cerrar",
                command=img_window.destroy,
                bootstyle="secondary"
            ).pack()

            # Mantener referencia a la imagen
            img_label.image = photo

        except Exception as e:
            Messagebox.show_error(
                f"Error al mostrar imagen: {str(e)}",
                "Error",
                parent=parent
            )

    def _agregar_imagen(self, gallery_frame, id_registro, ventana_parent):
        """Permite agregar una nueva imagen"""
        from tkinter import filedialog

        # Seleccionar archivo
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("GIF", "*.gif"),
                ("BMP", "*.bmp"),
                ("TIFF", "*.tiff"),
                ("WebP", "*.webp"),
                ("Todos los archivos", "*.*")
            ],
            parent=ventana_parent
        )

        if not file_path:
            return

        try:
            # Obtener nombre del archivo
            filename = os.path.basename(file_path)

            # Crear nombre único si ya existe
            destination_path = os.path.join(self.images_dir, filename)
            counter = 1
            name, ext = os.path.splitext(filename)

            while os.path.exists(destination_path):
                new_filename = f"{name}_{counter}{ext}"
                destination_path = os.path.join(self.images_dir, new_filename)
                counter += 1

            # Copiar archivo
            shutil.copy2(file_path, destination_path)

            # Actualizar galería
            self._actualizar_galeria(gallery_frame, id_registro, ventana_parent)

            Messagebox.show_info(
                f"Imagen agregada exitosamente:\n{os.path.basename(destination_path)}",
                "Imagen agregada",
                parent=ventana_parent
            )

        except Exception as e:
            Messagebox.show_error(
                f"Error al agregar imagen: {str(e)}",
                "Error",
                parent=ventana_parent
            )

    def _actualizar_galeria(self, gallery_frame, id_registro, ventana_parent):
        """Actualiza la galería recargando las imágenes"""
        self._cargar_imagenes(gallery_frame, id_registro, ventana_parent)

    def _format_file_size(self, size_bytes):
        """Formatea el tamaño del archivo en una forma legible"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.1f} {size_names[i]}"


# Función para mostrar la galería desde otras partes del código
def mostrar_galeria_fotos(parent, id_registro=None):
    """Función helper para mostrar la galería"""
    galeria = GaleriaFotos(parent)
    galeria.mostrar_galeria(id_registro)