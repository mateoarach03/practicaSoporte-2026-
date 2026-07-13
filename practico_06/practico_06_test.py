# Implementar los casos de prueba descriptos.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest

from practico_05.ejercicio_01 import Socio
from practico_06.capa_negocio import NegocioSocio, LongitudInvalida, DniRepetido, MaximoAlcanzado


class TestsNegocio(unittest.TestCase):

    def setUp(self):
        super(TestsNegocio, self).setUp()
        self.ns = NegocioSocio()

    def tearDown(self):
        super(TestsNegocio, self).tearDown()
        self.ns.datos.borrar_todos()

    def test_alta(self):
        # pre-condiciones: no hay socios registrados
        self.assertEqual(len(self.ns.todos()), 0)

        # ejecuto la logica
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        exito = self.ns.alta(socio)

        # post-condiciones: 1 socio registrado
        self.assertTrue(exito)
        self.assertEqual(len(self.ns.todos()), 1)
        print('[OK] test_alta: alta de socio exitoso')

    def test_regla_1(self):
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(socio)

        duplicado = Socio(dni=12345678, nombre='Otro', apellido='Otro')
        self.assertRaises(DniRepetido, self.ns.regla_1, duplicado)
        print('[OK] test_regla_1: DNI repetido detectado correctamente')

    def test_regla_2_nombre_menor_3(self):
        # valida regla
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.assertTrue(self.ns.regla_2(valido))

        # nombre menor a 3 caracteres
        invalido = Socio(dni=12345678, nombre='J', apellido='Perez')
        self.assertRaises(LongitudInvalida, self.ns.regla_2, invalido)
        print('[OK] test_regla_2_nombre_menor_3: nombre con menos de 3 caracteres rechazado')

    def test_regla_2_nombre_mayor_15(self):
        invalido = Socio(dni=12345678, nombre='Nombresuperlargo123', apellido='Perez')
        self.assertRaises(LongitudInvalida, self.ns.regla_2, invalido)
        print('[OK] test_regla_2_nombre_mayor_15: nombre con mas de 15 caracteres rechazado')

    def test_regla_2_apellido_menor_3(self):
        invalido = Socio(dni=12345678, nombre='Juan', apellido='Pe')
        self.assertRaises(LongitudInvalida, self.ns.regla_2, invalido)
        print('[OK] test_regla_2_apellido_menor_3: apellido con menos de 3 caracteres rechazado')

    def test_regla_2_apellido_mayor_15(self):
        invalido = Socio(dni=12345678, nombre='Juan', apellido='Apellidosuperlargo')
        self.assertRaises(LongitudInvalida, self.ns.regla_2, invalido)
        print('[OK] test_regla_2_apellido_mayor_15: apellido con mas de 15 caracteres rechazado')

    def test_regla_3(self):
        for i in range(self.ns.MAX_SOCIOS):
            s = Socio(dni=10000000 + i, nombre='Nombre', apellido='Apellido')
            self.ns.datos.alta(s)

        self.assertRaises(MaximoAlcanzado, self.ns.regla_3)
        print('[OK] test_regla_3: maximo de socios alcanzado detectado correctamente')

    def test_baja(self):
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(socio)
        self.assertEqual(len(self.ns.todos()), 1)

        exito = self.ns.baja(socio.id)
        self.assertTrue(exito)
        self.assertEqual(len(self.ns.todos()), 0)
        print('[OK] test_baja: baja de socio exitosa')

    def test_buscar(self):
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(socio)

        encontrado = self.ns.buscar(socio.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, 'Juan')
        print('[OK] test_buscar: busqueda por id exitosa')

    def test_buscar_dni(self):
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(socio)

        encontrado = self.ns.buscar_dni(12345678)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, 'Juan')
        print('[OK] test_buscar_dni: busqueda por DNI exitosa')

    def test_todos(self):
        self.assertEqual(len(self.ns.todos()), 0)

        self.ns.alta(Socio(dni=12345678, nombre='Juan', apellido='Perez'))
        self.ns.alta(Socio(dni=12345679, nombre='Carlos', apellido='Lopez'))

        self.assertEqual(len(self.ns.todos()), 2)
        print('[OK] test_todos: listado de socios exitoso')

    def test_modificacion(self):
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(socio)

        socio.nombre = 'Pedro'
        socio.apellido = 'Gomez'
        exito = self.ns.modificacion(socio)
        self.assertTrue(exito)

        modificado = self.ns.buscar(socio.id)
        self.assertEqual(modificado.nombre, 'Pedro')
        self.assertEqual(modificado.apellido, 'Gomez')
        print('[OK] test_modificacion: modificacion de socio exitosa')

#ejecucion de los tests
if __name__ == '__main__':
    unittest.main()
    