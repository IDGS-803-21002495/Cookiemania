from flask import Blueprint

ventas_bp = Blueprint('venta', __name__, url_prefix='/ventas', template_folder='templates')

from . import routes