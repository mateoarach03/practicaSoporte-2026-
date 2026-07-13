"""Base de Datos SQL - Crear y Borrar Tablas"""

import datetime
import os
import sqlite3

sqlite3.register_adapter(datetime.datetime, lambda value: value.isoformat(" "))
sqlite3.register_converter("TIMESTAMP", lambda value: datetime.datetime.fromisoformat(value.decode()))

DB_PATH = os.path.join(os.path.dirname(__file__), "practico_04.sqlite3")


def _conectar():
    conexion = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def crear_tabla():
    """Implementar la funcion crear_tabla, que cree una tabla Persona con:
        - IdPersona: Int() (autoincremental)
        - Nombre: Char(30)
        - FechaNacimiento: Date()
        - DNI: Int()
        - Altura: Int()
    """
    with _conectar() as conexion:
        conexion.execute("DROP TABLE IF EXISTS Persona")
        conexion.execute(
            """
            CREATE TABLE Persona (
                IdPersona INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre TEXT,
                FechaNacimiento TIMESTAMP,
                DNI INTEGER,
                Altura INTEGER
            )
            """
        )


def borrar_tabla():
    """Implementar la funcion borrar_tabla, que borra la tabla creada 
    anteriormente."""
    with _conectar() as conexion:
        conexion.execute("DROP TABLE IF EXISTS Persona")


# NO MODIFICAR - INICIO
def reset_tabla(func):
    def func_wrapper():
        crear_tabla()
        func()
        borrar_tabla()
    return func_wrapper
# NO MODIFICAR - FIN
