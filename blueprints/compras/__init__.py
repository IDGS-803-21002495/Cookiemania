from flask import Blueprint

compras_bp = Blueprint('compras', __name__, url_prefix='/compras', template_folder='templates')

from . import routes