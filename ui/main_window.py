import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ui.photo_gallery import mostrar_galeria_fotos
from database.db_manager import conectar_db
import csv
from tkinter import filedialog
from datetime import datetime
import os


def mostrar_ventana_principal(root):
    # Configuración básica de la ventana
    root.title("Sistema de Fotomultas")
    root.geometry("950x700")
    root.resizable(True, True)

    # Crear un estilo personalizado
    estilo = tb.Style()
    estilo.configure('TButton', font=('Helvetica', 10))
    estilo.configure('Accent.TButton', background='#0063B1')

    # Crear un canvas con scrollbars para permitir desplazamiento
    canvas_container = tb.Frame(root)
    canvas_container.pack(fill="both", expand=True)

    # Scrollbar vertical para el canvas
    vscrollbar = tb.Scrollbar(canvas_container, orient="vertical", bootstyle="round-info")
    vscrollbar.pack(side="right", fill="y")

    # Scrollbar horizontal para el canvas
    hscrollbar = tb.Scrollbar(canvas_container, orient="horizontal", bootstyle="round-info")
    hscrollbar.pack(side="bottom", fill="x")

    # Canvas donde colocaremos todo el contenido
    canvas = tb.Canvas(canvas_container)
    canvas.pack(side="left", fill="both", expand=True)

    # Configurar scrollbars para el canvas
    canvas.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
    vscrollbar.configure(command=canvas.yview)
    hscrollbar.configure(command=canvas.xview)

    # Frame principal dentro del canvas que contendrá todos los widgets
    main_container = tb.Frame(canvas, padding=15)

    # Agregar el frame al canvas
    canvas_window = canvas.create_window((0, 0), window=main_container, anchor="nw")

    # ---- Encabezado con degradado ----
    header_frame = tb.Frame(main_container)
    header_frame.pack(fill="x", pady=(0, 15))

    # Logo y título con mejor diseño
    title_frame = tb.Frame(header_frame)
    title_frame.pack(pady=10)

    logo_label = tb.Label(
        title_frame,
        text="🚓🐺",
        font=("Arial", 28),
        bootstyle="info"
    )
    logo_label.pack(side="left", padx=(0, 10))

    etiqueta = tb.Label(
        title_frame,
        text="Sistema de Fotomultas DASU",
        font=("Helvetica", 24, "bold"),
        bootstyle="info"
    )
    etiqueta.pack(side="left")

    # Panel de búsqueda con mejor diseño
    search_frame = tb.LabelFrame(
        main_container,
        text="Filtros de búsqueda",
        padding=15,
        bootstyle="info"
    )
    search_frame.pack(fill="x", pady=(0, 15))

    # Primera fila de filtros
    filtros_row1 = tb.Frame(search_frame)
    filtros_row1.pack(fill="x", pady=5)

    # Columna 1: Placa
    filtro_placa = tb.Frame(filtros_row1)
    filtro_placa.pack(side="left", expand=True, fill="x", padx=(0, 10))

    tb.Label(
        filtro_placa,
        text="Placa:",
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(0, 3))

    entrada_placa = tb.Entry(filtro_placa)
    entrada_placa.pack(fill="x")

    # Columna 2: Fecha
    filtro_fecha = tb.Frame(filtros_row1)
    filtro_fecha.pack(side="left", expand=True, fill="x", padx=(0, 10))

    tb.Label(
        filtro_fecha,
        text="Fecha (YYYY-MM-DD):",
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(0, 3))

    entrada_fecha = tb.Entry(filtro_fecha)
    entrada_fecha.pack(fill="x")

    # Columna 3: Velocidad
    filtro_velocidad = tb.Frame(filtros_row1)
    filtro_velocidad.pack(side="left", expand=True, fill="x")

    tb.Label(
        filtro_velocidad,
        text="Velocidad máxima:",
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(0, 3))

    entrada_velocidad = tb.Entry(filtro_velocidad)
    entrada_velocidad.pack(fill="x")

    # Botones de acción para búsqueda
    buttons_frame = tb.Frame(search_frame)
    buttons_frame.pack(fill="x", pady=(15, 0))

    boton_buscar = tb.Button(
        buttons_frame,
        text="🔍 Buscar",
        command=lambda: buscar(),
        bootstyle="info",
        width=15
    )
    boton_buscar.pack(side="left", padx=(0, 10))

    boton_limpiar = tb.Button(
        buttons_frame,
        text="🧹 Limpiar filtros",
        command=lambda: limpiar_filtros(),
        bootstyle="secondary",
        width=15
    )
    boton_limpiar.pack(side="left")

    # Función para limpiar los filtros
    def limpiar_filtros():
        entrada_placa.delete(0, tb.END)
        entrada_fecha.delete(0, tb.END)
        entrada_velocidad.delete(0, tb.END)

    # ---- Tabla de resultados con mejor diseño ----
    tabla_frame = tb.LabelFrame(
        main_container,
        text="Registros de infracciones",
        padding=15,
        bootstyle="info"
    )
    tabla_frame.pack(fill="both", expand=True, pady=(0, 15))

    # Columnas definidas
    columnas = ("Id", "Placa", "Fecha", "Velocidad", "Estado")

    # Tabla con mejor diseño y más información
    tabla = tb.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        bootstyle="info",
        height=12
    )

    # Configurando encabezados
    tabla.heading("Id", text="#")
    tabla.heading("Placa", text="🔖 Placa")
    tabla.heading("Fecha", text="📅 Fecha")
    tabla.heading("Velocidad", text="💨 Velocidad (km/h)")
    tabla.heading("Estado", text="📋 Estado")

    # Configurando anchos de columna
    tabla.column("Id", width=50, anchor="center")
    tabla.column("Placa", width=120, anchor="center")
    tabla.column("Fecha", width=150, anchor="center")
    tabla.column("Velocidad", width=150, anchor="center")
    tabla.column("Estado", width=150, anchor="center")

    # Empaquetando la tabla con scrollbars
    tabla.pack(side="left", fill="both", expand=True)

    # Scrollbar vertical mejorada
    scroll_y = tb.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview,
        bootstyle="info-round"
    )
    tabla.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    # Scrollbar horizontal
    scroll_x = tb.Scrollbar(
        tabla_frame,
        orient="horizontal",
        command=tabla.xview,
        bootstyle="info-round"
    )
    tabla.configure(xscrollcommand=scroll_x.set)
    scroll_x.pack(side="bottom", fill="x")

    # ---- Sección para agregar nueva infracción con mejor diseño ----
    frame_nuevo = tb.LabelFrame(
        main_container,
        text="Registrar nueva infracción",
        padding=15,
        bootstyle="info"
    )
    frame_nuevo.pack(fill="x", pady=(0, 15))

    # Contenedor para campos de entrada
    input_container = tb.Frame(frame_nuevo)
    input_container.pack(fill="x", pady=(0, 10))

    # Columna 1: Placa
    placa_frame = tb.Frame(input_container)
    placa_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))

    tb.Label(
        placa_frame,
        text="Placa:",
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(0, 3))

    entrada_nueva_placa = tb.Entry(placa_frame)
    entrada_nueva_placa.pack(fill="x")

    # Columna 2: Fecha
    fecha_frame = tb.Frame(input_container)
    fecha_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))

    tb.Label(
        fecha_frame,
        text="Fecha (YYYY-MM-DD):",
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(0, 3))

    entrada_nueva_fecha = tb.Entry(fecha_frame)
    entrada_nueva_fecha.pack(fill="x")

    # Fecha actual como valor predeterminado
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    entrada_nueva_fecha.insert(0, fecha_actual)

    # Columna 3: Velocidad
    velocidad_frame = tb.Frame(input_container)
    velocidad_frame.pack(side="left", expand=True, fill="x")

    tb.Label(
        velocidad_frame,
        text="Velocidad (km/h):",
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(0, 3))

    entrada_nueva_velocidad = tb.Entry(velocidad_frame)
    entrada_nueva_velocidad.pack(fill="x")

    # Guardar infracción
    def guardar_nueva_placa():
        placa = entrada_nueva_placa.get().strip().upper()
        fecha = entrada_nueva_fecha.get().strip()
        velocidad = entrada_nueva_velocidad.get().strip()

        # Validaciones
        if not placa or not fecha or not velocidad:
            Messagebox.show_error(
                "Todos los campos son obligatorios",
                "Error de validación"
            )
            return

        try:
            velocidad = float(velocidad)
            if velocidad <= 0:
                raise ValueError("La velocidad debe ser un número positivo")
        except ValueError:
            Messagebox.show_error(
                "La velocidad debe ser un número positivo",
                "Error de validación"
            )
            return

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            Messagebox.show_error(
                "El formato de fecha debe ser YYYY-MM-DD",
                "Error de validación"
            )
            return

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO placas (numero_placa, fecha, velocidad) VALUES (?, ?, ?)",
                (placa, fecha, velocidad)
            )
            conn.commit()

            # Mostrar mensaje de éxito
            Messagebox.show_info(
                f"Infracción para la placa {placa} registrada exitosamente",
                "Registro exitoso"
            )

            # Limpiar campos
            entrada_nueva_placa.delete(0, tb.END)
            entrada_nueva_fecha.delete(0, tb.END)
            entrada_nueva_fecha.insert(0, fecha_actual)
            entrada_nueva_velocidad.delete(0, tb.END)

            # Actualizar tabla
            buscar()
        except Exception as e:
            Messagebox.show_error(
                f"Error al guardar: {str(e)}",
                "Error de base de datos"
            )
        finally:
            conn.close()

    # Botones de acción
    buttons_container = tb.Frame(frame_nuevo)
    buttons_container.pack(fill="x")

    boton_guardar = tb.Button(
        buttons_container,
        text="💾 Guardar",
        command=guardar_nueva_placa,
        bootstyle="success",
        width=15
    )
    boton_guardar.pack(side="left", padx=(0, 10))

    boton_limpiar_form = tb.Button(
        buttons_container,
        text="🧹 Limpiar",
        command=lambda: limpiar_formulario(),
        bootstyle="secondary",
        width=15
    )
    boton_limpiar_form.pack(side="left")

    # Función para limpiar el formulario
    def limpiar_formulario():
        entrada_nueva_placa.delete(0, tb.END)
        entrada_nueva_fecha.delete(0, tb.END)
        entrada_nueva_fecha.insert(0, fecha_actual)
        entrada_nueva_velocidad.delete(0, tb.END)

    # ---- Barra de herramientas en la parte inferior ----
    toolbar_frame = tb.Frame(main_container)
    toolbar_frame.pack(fill="x")

    # Estadísticas
    stats_frame = tb.LabelFrame(
        toolbar_frame,
        text="Estadísticas",
        bootstyle="secondary",
        padding=10
    )
    stats_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

    label_total = tb.Label(
        stats_frame,
        text="Total de registros: 0",
        font=("Helvetica", 10),
        bootstyle="secondary"
    )
    label_total.pack(side="left", padx=(0, 20))

    label_promedio = tb.Label(
        stats_frame,
        text="Velocidad promedio: 0 km/h",
        font=("Helvetica", 10),
        bootstyle="secondary"
    )
    label_promedio.pack(side="left")

    # Acciones
    actions_frame = tb.Frame(toolbar_frame)
    actions_frame.pack(side="right")

    boton_exportar = tb.Button(
        actions_frame,
        text="📁 Exportar a CSV",
        command=lambda: exportar_a_csv(),
        bootstyle="info-outline",
        width=15
    )
    boton_exportar.pack(side="left", padx=(0, 10))

    boton_fotos = tb.Button(
        actions_frame,
        text="📷 Ver Fotos",
        command=lambda: mostrar_fotos(),
        bootstyle="info-outline",
        width=15
    )
    boton_fotos.pack(side="left", padx=(0, 10))

    boton_acerca = tb.Button(
        actions_frame,
        text="ℹ️ Acerca de",
        command=lambda: mostrar_acerca_de(),
        bootstyle="secondary-outline",
        width=15
    )
    boton_acerca.pack(side="left")

    # ---- Funciones para mostrar fotos de infracciones ----
    def mostrar_fotos():
        """Muestra la galería de fotos de infracciones"""
        # Obtener el registro seleccionado si hay uno
        selection = tabla.selection()
        id_registro = None

        if selection:
            # Si hay una fila seleccionada, mostrar solo esas fotos
            item = tabla.item(selection[0])
            id_registro = item['values'][0]  # El ID está en la primera columna

        # Mostrar galería
        mostrar_galeria_fotos(root, id_registro)

        def on_double_click(event):
            """Maneja el doble clic en una fila de la tabla"""
            selection = tabla.selection()
            if selection:
                item = tabla.item(selection[0])
                id_registro = item['values'][0]
                mostrar_galeria_fotos(root, id_registro)

        # Agregar el evento de doble clic a la tabla
        tabla.bind("<Double-1>", on_double_click)

        # Opcional: Agregar menú contextual (clic derecho)
        def mostrar_menu_contextual(event):
            """Muestra menú contextual al hacer clic derecho"""
            selection = tabla.selection()
            if selection:
                menu = tb.Menu(root, tearoff=0)

                item = tabla.item(selection[0])
                id_registro = item['values'][0]
                placa = item['values'][1]

                menu.add_command(
                    label=f"Ver fotos de {placa}",
                    command=lambda: mostrar_galeria_fotos(root, id_registro)
                )

                menu.add_separator()
                menu.add_command(label="Cancelar")

                try:
                    menu.tk_popup(event.x_root, event.y_root)
                finally:
                    menu.grab_release()

        # Agregar el evento de clic derecho
        tabla.bind("<Button-3>", mostrar_menu_contextual)

    # ---- Funciones internas mejoradas ----
    def buscar():
        placa = entrada_placa.get().strip()
        fecha = entrada_fecha.get().strip()
        velocidad_max = entrada_velocidad.get().strip()

        conn = conectar_db()
        cursor = conn.cursor()

        query = "SELECT * FROM placas WHERE 1=1"
        params = []

        if placa:
            query += " AND numero_placa LIKE ?"
            params.append(f"%{placa}%")

        if fecha:
            query += " AND fecha = ?"
            params.append(fecha)

        if velocidad_max:
            try:
                velocidad_max = float(velocidad_max)
                query += " AND velocidad <= ?"
                params.append(velocidad_max)
            except ValueError:
                pass

        query += " ORDER BY id DESC"

        cursor.execute(query, params)
        resultados = cursor.fetchall()

        # Limpiar tabla
        for fila in tabla.get_children():
            tabla.delete(fila)

        # Insertar resultados
        total_registros = 0
        suma_velocidad = 0

        for fila in resultados:
            id_registro = fila[0]
            placa = fila[1]
            fecha = fila[2]
            velocidad = fila[3]

            # Determinar estado según velocidad
            estado = "Normal"
            if velocidad > 80 and velocidad <= 100:
                estado = "Exceso leve"
            elif velocidad > 100 and velocidad <= 120:
                estado = "Exceso moderado"
            elif velocidad > 120:
                estado = "Exceso grave"

            # Color de fila según estado
            tag = ""
            if estado == "Exceso leve":
                tag = "amarillo"
            elif estado == "Exceso moderado":
                tag = "naranja"
            elif estado == "Exceso grave":
                tag = "rojo"

            tabla.insert("", tb.END, values=(id_registro, placa, fecha, f"{velocidad:.1f}", estado), tags=(tag,))

            total_registros += 1
            suma_velocidad += velocidad

        # Configurar colores
        tabla.tag_configure("amarillo", background="#FFF9C4")
        tabla.tag_configure("naranja", background="#FFE0B2")
        tabla.tag_configure("rojo", background="#FFCDD2")

        # Actualizar estadísticas
        label_total.config(text=f"Total de registros: {total_registros}")

        if total_registros > 0:
            promedio = suma_velocidad / total_registros
            label_promedio.config(text=f"Velocidad promedio: {promedio:.1f} km/h")
        else:
            label_promedio.config(text="Velocidad promedio: 0 km/h")

        conn.close()

    def exportar_a_csv():
        # Verificar si hay datos para exportar
        if not tabla.get_children():
            Messagebox.show_warning(
                "No hay datos para exportar",
                "Exportación cancelada"
            )
            return

        # Crear directorio de exportación si no existe
        export_dir = os.path.join(os.getcwd(), "exports")
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        # Nombre de archivo predeterminado con fecha
        default_filename = f"fotomultas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        default_path = os.path.join(export_dir, default_filename)

        archivo = filedialog.asksaveasfilename(
            initialdir=export_dir,
            initialfile=default_filename,
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            title="Guardar reporte como"
        )

        if not archivo:
            return

        try:
            with open(archivo, mode="w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Placa", "Fecha", "Velocidad (km/h)", "Estado"])

                for fila in tabla.get_children():
                    valores = tabla.item(fila)["values"]
                    writer.writerow(valores)

            Messagebox.show_info(
                f"Datos exportados exitosamente a:\n{archivo}",
                "Exportación exitosa"
            )
        except Exception as e:
            Messagebox.show_error(
                f"Error al exportar: {str(e)}",
                "Error de exportación"
            )

    def mostrar_acerca_de():
        ventana_acerca = tb.Toplevel(root)
        ventana_acerca.title("Acerca de")
        ventana_acerca.geometry("400x300")
        ventana_acerca.resizable(False, False)

        # Contenedor principal
        frame_acerca = tb.Frame(ventana_acerca, padding=20)
        frame_acerca.pack(fill="both", expand=True)

        # Título
        tb.Label(
            frame_acerca,
            text="Sistema de Fotomultas DASU",
            font=("Helvetica", 16, "bold"),
            bootstyle="info"
        ).pack(pady=(0, 10))

        # Versión
        tb.Label(
            frame_acerca,
            text="Versión 1.0.0",
            font=("Helvetica", 12),
            bootstyle="secondary"
        ).pack(pady=(0, 20))

        # Descripción
        tb.Label(
            frame_acerca,
            text="Sistema desarrollado para el registro y\ngestión de infracciones de tránsito por exceso\nde velocidad.",
            font=("Helvetica", 10),
            justify="center"
        ).pack(pady=(0, 20))

        # Año
        tb.Label(
            frame_acerca,
            text=f"© {datetime.now().year} - Dirección de Apoyo y\nSeguridad Universitaria",
            font=("Helvetica", 10),
            justify="center",
            bootstyle="secondary"
        ).pack(pady=(0, 20))

        # Botón de cerrar
        tb.Button(
            frame_acerca,
            text="Cerrar",
            command=ventana_acerca.destroy,
            bootstyle="info",
            width=15
        ).pack()

    # Función para actualizar el scrollregion cuando el tamaño de los widgets cambia
    def ajustar_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Asegurar que el ancho del canvas sea al menos el ancho del frame
        canvas_width = main_container.winfo_reqwidth()
        if canvas_width > root.winfo_width():
            canvas.itemconfigure(canvas_window, width=canvas_width)
        else:
            canvas.itemconfigure(canvas_window, width=root.winfo_width() - 20)  # 20 pixels para el scrollbar

    # Vincular eventos para ajustar el scrollregion
    main_container.bind("<Configure>", ajustar_scroll_region)

    # Función para manejar el desplazamiento con la rueda del mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Vincular el evento de la rueda del mouse para desplazamiento
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Vincular eventos de redimensionamiento de la ventana
    def on_window_resize(event):
        # Actualizar el ancho del canvas_window cuando se redimensiona la ventana
        canvas_width = canvas.winfo_width()
        canvas.itemconfigure(canvas_window, width=canvas_width)

    root.bind("<Configure>", on_window_resize)

    # Mostrar registros al iniciar
    buscar()