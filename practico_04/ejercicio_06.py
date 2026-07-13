"""Base de Datos SQL - Creación de tablas auxiliares"""

from practico_04.ejercicio_01 import _conectar, borrar_tabla, crear_tabla


def crear_tabla_peso():
    """Implementar la funcion crear_tabla_peso, que cree una tabla PersonaPeso con:
        - IdPersona: Int() (Clave Foranea Persona)
        - Fecha: Date()
        - Peso: Int()
    """
    with _conectar() as conexion:
        conexion.execute("DROP TABLE IF EXISTS PersonaPeso")
        conexion.execute(
            """
            CREATE TABLE PersonaPeso (
                IdPersona INTEGER,
                Fecha TIMESTAMP,
                Peso INTEGER,
                FOREIGN KEY (IdPersona) REFERENCES Persona(IdPersona)
            )
            """
        )


def borrar_tabla_peso():
    """Implementar la funcion borrar_tabla, que borra la tabla creada 
    anteriormente."""
    with _conectar() as conexion:
        conexion.execute("DROP TABLE IF EXISTS PersonaPeso")


# NO MODIFICAR - INICIO
def reset_tabla(func):
    def func_wrapper():
        crear_tabla()
        crear_tabla_peso()
        func()
        borrar_tabla_peso()
        borrar_tabla()
    return func_wrapper
# NO MODIFICAR - FIN
