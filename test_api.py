"""Pruebas unitarias para la API de tareas."""
import json
import unittest
from app import app, db, Tarea


class APITareasTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    # ── helpers ──────────────────────────
    def _crear(self, titulo='Test', descripcion='Desc', estado='pendiente'):
        return self.client.post('/tareas',
                                data=json.dumps({'titulo': titulo,
                                                 'descripcion': descripcion,
                                                 'estado': estado}),
                                content_type='application/json')

    # ── tests ────────────────────────────
    def test_crear_tarea_exitoso(self):
        r = self._crear('Mi tarea', 'Descripción de prueba')
        self.assertEqual(r.status_code, 201)
        data = r.get_json()
        self.assertEqual(data['titulo'], 'Mi tarea')
        self.assertEqual(data['estado'], 'pendiente')

    def test_crear_sin_titulo_falla(self):
        r = self._crear(titulo='')
        self.assertEqual(r.status_code, 400)

    def test_crear_estado_invalido_falla(self):
        r = self._crear(estado='inexistente')
        self.assertEqual(r.status_code, 400)

    def test_obtener_lista_vacia(self):
        r = self.client.get('/tareas')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['total'], 0)

    def test_obtener_tarea_por_id(self):
        self._crear()
        r = self.client.get('/tareas/1')
        self.assertEqual(r.status_code, 200)

    def test_obtener_tarea_inexistente(self):
        r = self.client.get('/tareas/99')
        self.assertEqual(r.status_code, 404)

    def test_actualizar_tarea(self):
        self._crear()
        r = self.client.put('/tareas/1',
                            data=json.dumps({'estado': 'completada'}),
                            content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['estado'], 'completada')

    def test_eliminar_tarea(self):
        self._crear()
        r = self.client.delete('/tareas/1')
        self.assertEqual(r.status_code, 200)
        r2 = self.client.get('/tareas/1')
        self.assertEqual(r2.status_code, 404)

    def test_filtrar_por_estado(self):
        self._crear(estado='pendiente')
        self._crear(titulo='Otra', descripcion='Desc2', estado='completada')
        r = self.client.get('/tareas?estado=pendiente')
        self.assertEqual(r.get_json()['total'], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
