# API REST – Administrador de Tareas

API CRUD completa construida con **Flask** y **SQLite** (via SQLAlchemy).

---

## Requisitos

- Python 3.9+
- pip

---

## Instalación rápida

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. (Opcional) Cargar datos de ejemplo
python init_db.py

# 4. Iniciar servidor
python app.py
```

El servidor queda disponible en `http://127.0.0.1:5000`.

---

## Endpoints

| Método | Ruta            | Descripción               |
|--------|-----------------|---------------------------|
| POST   | `/tareas`       | Crear una nueva tarea     |
| GET    | `/tareas`       | Listar todas las tareas   |
| GET    | `/tareas/<id>`  | Obtener una tarea por ID  |
| PUT    | `/tareas/<id>`  | Actualizar una tarea      |
| DELETE | `/tareas/<id>`  | Eliminar una tarea        |

### Filtro opcional en GET /tareas

```
GET /tareas?estado=pendiente
```

### Estados válidos

| Valor        | Significado         |
|--------------|---------------------|
| `pendiente`  | Sin iniciar (default) |
| `en_progreso`| En curso            |
| `completada` | Finalizada          |

---

## Ejemplos con curl

### Crear tarea
```bash
curl -X POST http://127.0.0.1:5000/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Estudiar Flask","descripcion":"Repasar rutas y blueprints","estado":"pendiente"}'
```

### Listar todas
```bash
curl http://127.0.0.1:5000/tareas
```

### Obtener por ID
```bash
curl http://127.0.0.1:5000/tareas/1
```

### Actualizar
```bash
curl -X PUT http://127.0.0.1:5000/tareas/1 \
  -H "Content-Type: application/json" \
  -d '{"estado":"completada"}'
```

### Eliminar
```bash
curl -X DELETE http://127.0.0.1:5000/tareas/1
```

---

## Ejecutar pruebas

```bash
python -m pytest test_api.py -v
# o bien
python test_api.py
```

---

## Estructura del proyecto

```
api_tareas/
├── app.py            ← Aplicación principal (modelos + rutas)
├── init_db.py        ← Inicializador con datos de ejemplo
├── test_api.py       ← Suite de pruebas unitarias
├── requirements.txt  ← Dependencias
└── README.md         ← Esta guía
```

---

## Estructura de una Tarea (JSON)

```json
{
  "id": 1,
  "titulo": "Estudiar Flask",
  "descripcion": "Repasar rutas y blueprints",
  "estado": "pendiente",
  "creada_en": "2026-03-19T10:00:00",
  "actualizada": "2026-03-19T10:00:00"
}
```
