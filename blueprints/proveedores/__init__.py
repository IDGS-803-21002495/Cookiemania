from flask import Blueprint

proveedores_bp = Blueprint('proveedores', __name__, url_prefix='/proveedores', template_folder='templates')

from . import routes