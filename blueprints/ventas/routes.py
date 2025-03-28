from . import ventas_bp
from flask import render_template

@ventas_bp.route('/')
def ventas():
    return render_template('ventas.html')