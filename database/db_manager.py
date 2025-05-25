import sqlite3
import os
from datetime import datetime, timedelta
import random

# Ruta de la base de datos
DB_PATH = os.path.join("data", "fotomultas.db")


def conectar_db():
    """Crea la conexión a la base de datos"""
    # Asegurar que el directorio exista
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
    return conn


def eliminar_db():
    """Elimina la base de datos si existe"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Base de datos eliminada: {DB_PATH}")
    else:
        print("No existe base de datos para eliminar")


def crear_tabla_placas():
    """Crea la tabla principal de placas si no existe"""
    conn = conectar_db()
    cursor = conn.cursor()

    # Crear la tabla con los campos necesarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS placas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_placa TEXT NOT NULL,
            fecha TEXT NOT NULL,
            velocidad REAL,
            imagen_path TEXT,
            ubicacion TEXT,
            observaciones TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Tabla 'placas' creada correctamente")


def generar_datos_prueba(num_registros=20):
    """Genera datos de prueba más variados y realistas"""
    placas = [
        "ABC123", "XYZ789", "MNO456", "PQR789", "DEF321",
        "JKL654", "GHI987", "STU234", "VWX567", "YZA890",
        "BCD123", "EFG456", "HIJ789", "KLM012", "NOP345"
    ]

    ubicaciones = [
        "Av. Libertador km 5",
        "Calle Principal y Av. Central",
        "Autopista Norte km 23",
        "Ruta 7 km 15",
        "Circunvalación Este km 8",
        "Av. San Martín 1200",
        "Ruta Panamericana km 50",
        "Acceso Sur km 3"
    ]

    observaciones = [
        "Conductor con exceso de velocidad en zona escolar",
        "Reincidente en infracción de velocidad",
        "Clima lluvioso",
        "Conductor no acató señalización",
        "Zona de obras",
        "Día festivo con alto tránsito",
        "Conductor se dio a la fuga",
        "",  # Algunos registros sin observaciones
        "Velocidad excesivamente alta, se remite a fiscalía",
        "Infracción en horario nocturno"
    ]

    # Fecha base (hace 30 días desde hoy)
    fecha_base = datetime.now() - timedelta(days=30)

    datos = []
    for _ in range(num_registros):
        # Generar placa aleatoria o usar una de la lista
        placa = random.choice(placas)

        # Generar fecha aleatoria entre hace 30 días y hoy
        dias_aleatorios = random.randint(0, 30)
        fecha = fecha_base + timedelta(days=dias_aleatorios)
        fecha_str = fecha.strftime("%Y-%m-%d")

        # Generar velocidad aleatoria entre 60 y 150 km/h
        velocidad = round(random.uniform(60, 150), 1)

        # Generar datos adicionales
        ubicacion = random.choice(ubicaciones)
        observacion = random.choice(observaciones)

        # Ruta de imagen (se implementará en el punto 1)
        imagen_path = f"images/img_{random.randint(1, 5)}.jpg" if random.random() > 0.3 else ""

        datos.append((placa, fecha_str, velocidad, imagen_path, ubicacion, observacion))

    return datos


def insertar_datos_prueba(num_registros=20):
    """Inserta datos de prueba en la tabla placas"""
    conn = conectar_db()
    cursor = conn.cursor()

    # Generar datos aleatorios
    datos = generar_datos_prueba(num_registros)

    # Insertar cada registro
    for placa, fecha, velocidad, imagen_path, ubicacion, observacion in datos:
        cursor.execute(
            """
            INSERT INTO placas 
            (numero_placa, fecha, velocidad, imagen_path, ubicacion, observaciones) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (placa, fecha, velocidad, imagen_path, ubicacion, observacion)
        )

    conn.commit()
    conn.close()
    print(f"{num_registros} registros de prueba insertados correctamente")


def reiniciar_base_datos():
    """Elimina la base de datos existente y crea una nueva con datos de prueba"""
    # Eliminar base de datos si existe
    eliminar_db()

    # Crear estructura de base de datos
    crear_tabla_placas()

    # Insertar datos de prueba
    insertar_datos_prueba(25)  # 25 registros aleatorios

    print("Base de datos reiniciada correctamente")


def obtener_registro_por_id(id_registro):
    """Obtiene un registro específico por su ID"""
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM placas WHERE id = ?", (id_registro,))
    registro = cursor.fetchone()

    conn.close()
    return dict(registro) if registro else None


def actualizar_registro(id_registro, datos):
    """Actualiza un registro existente"""
    conn = conectar_db()
    cursor = conn.cursor()

    campos = []
    valores = []

    for campo, valor in datos.items():
        campos.append(f"{campo} = ?")
        valores.append(valor)

    # Añadir el ID al final de los valores
    valores.append(id_registro)

    cursor.execute(
        f"UPDATE placas SET {', '.join(campos)} WHERE id = ?",
        valores
    )

    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def eliminar_registro(id_registro):
    """Elimina un registro por su ID"""
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM placas WHERE id = ?", (id_registro,))

    conn.commit()
    conn.close()
    return cursor.rowcount > 0