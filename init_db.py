"""Script auxiliar para inicializar la base de datos y cargar datos de ejemplo."""
from app import app, db, Tarea

with app.app_context():
    db.create_all()

    ejemplos = [
        Tarea(titulo='Aprender Flask',
              descripcion='Completar el tutorial oficial de Flask y construir una API REST.',
              estado='en_progreso'),
        Tarea(titulo='Revisar SQL',
              descripcion='Repasar consultas JOIN, índices y transacciones en SQLite.',
              estado='pendiente'),
        Tarea(titulo='Instalar dependencias',
              descripcion='Ejecutar pip install -r requirements.txt en el entorno virtual.',
              estado='completada'),
    ]
    db.session.add_all(ejemplos)
    db.session.commit()
    print('Base de datos inicializada con 3 tareas de ejemplo.')
