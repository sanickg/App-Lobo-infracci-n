# 🛑 Proyecto de Fotomultas (INCOMPLETO - USO EDUCATIVO)

Este proyecto fue desarrollado como parte de una materia universitaria, y su objetivo principal es **simular un sistema de fotomultas automatizado** con detección de placas, velocidades y registro en una base de datos mediante una interfaz gráfica en Python.

⚠️ **Este repositorio contiene código incompleto**. Algunas funciones pueden no estar terminadas o presentar errores. El objetivo de subirlo es meramente **demostrar el alcance del desarrollo durante el curso** y compartir la estructura general del proyecto.

---

## 📦 Estructura del Proyecto

```plaintext
PythonProject/
├── main.py            # Archivo principal
├──data/               # Base
    └── fotomultas.db
├── ui/            # Contiene la GUI hecha con PyQt y Tkinter
    └── login_window.py
    └── main_window.py
    └── photo_gallery.py
├── sensores/            # Código Arduino o simulación de sensores (por añadir)
├── exports/             # Bases exportadas
├── database/            # Conexión a base de datos y consultas
│   └── db_manager.py
├── logs/
│   └── error.log        # Registro de errores (IGNORADO en Git)
├── .gitignore           # Archivos excluidos del repositorio
└── README.md            # Este archivo
```
🧪 Funcionalidades Planeadas
 Interfaz gráfica con botones y tablas.

 Registro de vehículos detectados con velocidad.

 Conexión con hardware para lectura de placas.

 Análisis de velocidad con sensores externos.

 Módulo de autenticación de usuarios (en progreso).

🚧 Estado del proyecto
Este proyecto no está finalizado. Contiene errores conocidos (como problemas con imágenes y Tkinter), y fue desarrollado como prototipo funcional para presentar en clase.

📚 Propósito educativo
Este repositorio no representa una aplicación lista para producción. Fue hecho con fines académicos, para:

Aprender a integrar interfaces gráficas con bases de datos.

Simular un sistema real usando sensores y software.

Aplicar principios de programación orientada a objetos en Python.

📸 Vista previa

![Captura de pantalla 2025-05-23 093426](https://github.com/user-attachments/assets/75b74180-29c7-4e57-b59f-d0f1ee5c1334)
![Captura de pantalla 2025-05-21 013757](https://github.com/user-attachments/assets/d243aa4d-042f-492b-95c1-a954565707d8)
![Captura de pantalla 2025-05-23 113511](https://github.com/user-attachments/assets/c7b54789-1c9f-4ab8-bc2e-30311ded977e)


🧑‍💻 Autor
Desarrollado por: [Alfonso López]
Para la asignatura de [Administración de Proyectos] — [Benemérita Universidad Autónoma de Puebla]

📝 Licencia
Este código se comparte sin licencia comercial. Puede usarse y modificarse para fines educativos o experimentales.
