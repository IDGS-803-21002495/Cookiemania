from flask import Blueprint

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario', template_folder='templates')

from . import routes