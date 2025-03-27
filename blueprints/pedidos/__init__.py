from flask import Blueprint

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos', template_folder='templates')

from . import routes