# Casos de prueba de la capa de presentacion (TP7 - Flask).

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest

from practico_05.ejercicio_01 import Socio
from practico_06.capa_negocio import NegocioSocio
from practico_07.app import create_app


class TestsPresentacion(unittest.TestCase):

    def setUp(self):
        super(TestsPresentacion, self).setUp()
        self.negocio = NegocioSocio()
        self.app = create_app(negocio=self.negocio)
        self.client = self.app.test_client()

    def tearDown(self):
        super(TestsPresentacion, self).tearDown()
        self.negocio.datos.borrar_todos()

    def alta_via_form(self, dni=12345678, nombre='Juan', apellido='Perez'):
        return self.client.post('/socios/nuevo', data={
            'dni': str(dni),
            'nombre': nombre,
            'apellido': apellido,
        })

    def test_index_inicial(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Socios', response.data)
        self.assertIn(b'<table', response.data)
        self.assertEqual(len(self.negocio.todos()), 0)
        print('[OK] test_index_inicial: listado inicial vacio renderizado')

    def test_alta_socio_ok(self):
        response = self.alta_via_form()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/')
        self.assertEqual(len(self.negocio.todos()), 1)
        print('[OK] test_alta_socio_ok: alta por formulario exitosa')

    def test_alta_dni_repetido(self):
        self.alta_via_form()
        response = self.alta_via_form()

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'El DNI ya se encuentra registrado', response.data)
        self.assertEqual(len(self.negocio.todos()), 1)
        print('[OK] test_alta_dni_repetido: DNI repetido informado al usuario')

    def test_alta_dni_invalido(self):
        response = self.client.post('/socios/nuevo', data={
            'dni': 'abc',
            'nombre': 'Juan',
            'apellido': 'Perez',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'El DNI', response.data)
        self.assertEqual(len(self.negocio.todos()), 0)
        print('[OK] test_alta_dni_invalido: DNI no numerico rechazado')

    def test_alta_nombre_corto(self):
        response = self.alta_via_form(nombre='J')

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'El nombre y apellido deben tener entre 4 y 14 caracteres',
            response.data,
        )
        self.assertEqual(len(self.negocio.todos()), 0)
        print('[OK] test_alta_nombre_corto: longitud invalida rechazada')

    def test_baja_socio_ok(self):
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.negocio.alta(socio)

        response = self.client.post('/socios/{0}/baja'.format(socio.id))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.negocio.todos()), 0)
        print('[OK] test_baja_socio_ok: baja por formulario exitosa')

    def test_modificar_get_precargado(self):
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.negocio.alta(socio)

        response = self.client.get('/socios/{0}/modificar'.format(socio.id))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Juan', response.data)
        print('[OK] test_modificar_get_precargado: formulario precargado')

    def test_modificar_ok(self):
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.negocio.alta(socio)

        response = self.client.post('/socios/{0}/modificar'.format(socio.id), data={
            'dni': '12345678',
            'nombre': 'Pedro',
            'apellido': 'Gomez',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.negocio.buscar(socio.id).nombre, 'Pedro')
        print('[OK] test_modificar_ok: modificacion por formulario exitosa')

    def test_modificar_inexistente(self):
        response = self.client.get('/socios/999/modificar')

        self.assertEqual(response.status_code, 404)
        print('[OK] test_modificar_inexistente: socio inexistente devuelve 404')


# ejecucion de los tests
if __name__ == '__main__':
    unittest.main()
