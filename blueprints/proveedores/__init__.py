from flask import Blueprint
from . import forms

from models.enums import UserStatus

proveedores_bp = Blueprint('proveedores', __name__, url_prefix='/proveedores', template_folder='templates')

from . import routes