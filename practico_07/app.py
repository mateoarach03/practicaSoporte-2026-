"""Capa de presentacion del TP7: gestion de socios con Flask."""

import os

from flask import (
    Flask,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
)
from sqlalchemy.exc import IntegrityError

from practico_05.ejercicio_01 import Socio
from practico_05.ejercicio_02 import DatosSocio
from practico_06.capa_negocio import (
    DniRepetido,
    LongitudInvalida,
    MaximoAlcanzado,
    NegocioSocio,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'socios.db')
DB_URL = 'sqlite:///' + DB_PATH.replace(os.sep, '/')

SECRET_KEY = 'practico_07_secret_key'

MENSAJE_DNI_INVALIDO = 'El DNI debe ser un número entero'
MENSAJE_DNI_REPETIDO = 'El DNI ya se encuentra registrado'
MENSAJE_LONGITUD = 'El nombre y apellido deben tener entre 4 y 14 caracteres'
MENSAJE_MAXIMO = 'Se alcanzó el máximo de socios'


class NegocioSocioArchivo(NegocioSocio):
    """Capa de negocio con persistencia en un archivo SQLite.

    Reutiliza la logica de NegocioSocio cambiando unicamente la capa de datos
    para que trabaje contra un archivo en lugar de memoria.
    """

    def __init__(self, db_url=DB_URL):
        self.datos = DatosSocio(db_url=db_url)


def _negocio():
    """Devuelve la capa de negocio registrada en la aplicacion activa."""
    return current_app.extensions['socio_negocio']


def _datos_formulario():
    """Extrae y normaliza los campos del formulario de socio."""
    dni = request.form.get('dni', '').strip()
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    return dni, nombre, apellido


def index():
    """Muestra la tabla con todos los socios."""
    return render_template('index.html', socios=_negocio().todos())


def alta_socio():
    """Alta de un socio: muestra el formulario o procesa el envio."""
    if request.method == 'GET':
        return render_template('alta.html', dni='', nombre='', apellido='')

    dni, nombre, apellido = _datos_formulario()
    contexto = {'dni': dni, 'nombre': nombre, 'apellido': apellido}

    if not dni.isdigit():
        flash(MENSAJE_DNI_INVALIDO, 'error')
        return render_template('alta.html', **contexto), 200

    try:
        _negocio().alta(Socio(dni=int(dni), nombre=nombre, apellido=apellido))
    except DniRepetido:
        flash(MENSAJE_DNI_REPETIDO, 'error')
        return render_template('alta.html', **contexto), 200
    except LongitudInvalida:
        flash(MENSAJE_LONGITUD, 'error')
        return render_template('alta.html', **contexto), 200
    except MaximoAlcanzado:
        flash(MENSAJE_MAXIMO, 'error')
        return render_template('alta.html', **contexto), 200

    flash('Socio registrado correctamente', 'success')
    return redirect('/')


def baja_socio(id_socio):
    """Da de baja el socio indicado."""
    _negocio().baja(id_socio)
    flash('Socio dado de baja correctamente', 'success')
    return redirect('/')


def modificar_socio(id_socio):
    """Modifica un socio: muestra el formulario precargado o procesa el envio."""
    socio = _negocio().buscar(id_socio)
    if socio is None:
        abort(404)

    if request.method == 'GET':
        return render_template(
            'modificar.html',
            id_socio=id_socio,
            dni=socio.dni,
            nombre=socio.nombre,
            apellido=socio.apellido,
        )

    dni, nombre, apellido = _datos_formulario()
    contexto = {
        'id_socio': id_socio,
        'dni': dni,
        'nombre': nombre,
        'apellido': apellido,
    }

    if not dni.isdigit():
        flash(MENSAJE_DNI_INVALIDO, 'error')
        return render_template('modificar.html', **contexto), 200

    socio.dni = int(dni)
    socio.nombre = nombre
    socio.apellido = apellido
    try:
        _negocio().modificacion(socio)
    except LongitudInvalida:
        flash(MENSAJE_LONGITUD, 'error')
        return render_template('modificar.html', **contexto), 200
    except IntegrityError:
        _negocio().datos.session.rollback()
        flash(MENSAJE_DNI_REPETIDO, 'error')
        return render_template('modificar.html', **contexto), 200

    flash('Socio modificado correctamente', 'success')
    return redirect('/')


def create_app(negocio=None):
    """Crea y configura la aplicacion Flask.

    Si no se inyecta una capa de negocio, se crea una con persistencia en el
    archivo socios.db del propio paquete.
    """
    template_folder = os.path.join(BASE_DIR, 'templates')
    static_folder = os.path.join(BASE_DIR, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    app.secret_key = SECRET_KEY
    app.extensions['socio_negocio'] = negocio if negocio is not None else NegocioSocioArchivo()

    app.add_url_rule('/', 'index', index, methods=['GET'])
    app.add_url_rule('/socios/nuevo', 'alta_socio', alta_socio, methods=['GET', 'POST'])
    app.add_url_rule('/socios/<int:id_socio>/baja', 'baja_socio', baja_socio, methods=['POST'])
    app.add_url_rule(
        '/socios/<int:id_socio>/modificar',
        'modificar_socio',
        modificar_socio,
        methods=['GET', 'POST'],
    )
    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
