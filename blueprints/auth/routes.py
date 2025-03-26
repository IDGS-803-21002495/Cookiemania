from flask import render_template
from . import auth_bp  

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    return "Cerrar sesión"
