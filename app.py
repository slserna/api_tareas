from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ──────────────────────────────────────────
# Modelo
# ──────────────────────────────────────────
class Tarea(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    titulo      = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado      = db.Column(db.String(20), nullable=False, default='pendiente')
    creada_en   = db.Column(db.DateTime, default=datetime.utcnow)
    actualizada = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ESTADOS_VALIDOS = {'pendiente', 'en_progreso', 'completada'}

    def to_dict(self):
        return {
            'id':          self.id,
            'titulo':      self.titulo,
            'descripcion': self.descripcion,
            'estado':      self.estado,
            'creada_en':   self.creada_en.isoformat(),
            'actualizada': self.actualizada.isoformat(),
        }

# ──────────────────────────────────────────
# Rutas
# ──────────────────────────────────────────

# POST /tareas  – crear tarea
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'Se esperaba JSON en el cuerpo de la petición'}), 400

    titulo      = datos.get('titulo', '').strip()
    descripcion = datos.get('descripcion', '').strip()
    estado      = datos.get('estado', 'pendiente').strip()

    if not titulo:
        return jsonify({'error': 'El campo "titulo" es obligatorio'}), 400
    if not descripcion:
        return jsonify({'error': 'El campo "descripcion" es obligatorio'}), 400
    if estado not in Tarea.ESTADOS_VALIDOS:
        return jsonify({'error': f'Estado inválido. Valores permitidos: {sorted(Tarea.ESTADOS_VALIDOS)}'}), 400

    tarea = Tarea(titulo=titulo, descripcion=descripcion, estado=estado)
    db.session.add(tarea)
    db.session.commit()
    return jsonify(tarea.to_dict()), 201


# GET /tareas  – listar tareas (con filtro opcional por estado)
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    estado = request.args.get('estado')
    query  = Tarea.query

    if estado:
        if estado not in Tarea.ESTADOS_VALIDOS:
            return jsonify({'error': f'Estado inválido. Valores permitidos: {sorted(Tarea.ESTADOS_VALIDOS)}'}), 400
        query = query.filter_by(estado=estado)

    tareas = query.order_by(Tarea.creada_en.desc()).all()
    return jsonify({'total': len(tareas), 'tareas': [t.to_dict() for t in tareas]}), 200


# GET /tareas/<id>  – obtener una tarea
@app.route('/tareas/<int:id>', methods=['GET'])
def obtener_tarea(id):
    tarea = db.session.get(Tarea, id)
    if not tarea:
        return jsonify({'error': f'Tarea {id} no encontrada'}), 404
    return jsonify(tarea.to_dict()), 200


# PUT /tareas/<id>  – actualizar tarea
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    tarea = db.session.get(Tarea, id)
    if not tarea:
        return jsonify({'error': f'Tarea {id} no encontrada'}), 404

    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'Se esperaba JSON en el cuerpo de la petición'}), 400

    if 'titulo' in datos:
        titulo = datos['titulo'].strip()
        if not titulo:
            return jsonify({'error': 'El campo "titulo" no puede estar vacío'}), 400
        tarea.titulo = titulo

    if 'descripcion' in datos:
        desc = datos['descripcion'].strip()
        if not desc:
            return jsonify({'error': 'El campo "descripcion" no puede estar vacío'}), 400
        tarea.descripcion = desc

    if 'estado' in datos:
        estado = datos['estado'].strip()
        if estado not in Tarea.ESTADOS_VALIDOS:
            return jsonify({'error': f'Estado inválido. Valores permitidos: {sorted(Tarea.ESTADOS_VALIDOS)}'}), 400
        tarea.estado = estado

    tarea.actualizada = datetime.utcnow()
    db.session.commit()
    return jsonify(tarea.to_dict()), 200


# DELETE /tareas/<id>  – eliminar tarea
@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    tarea = db.session.get(Tarea, id)
    if not tarea:
        return jsonify({'error': f'Tarea {id} no encontrada'}), 404

    db.session.delete(tarea)
    db.session.commit()
    return jsonify({'mensaje': f'Tarea {id} eliminada correctamente'}), 200


# ──────────────────────────────────────────
# Inicialización
# ──────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
