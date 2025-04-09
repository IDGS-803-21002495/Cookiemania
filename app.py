from flask import Flask, redirect, request, url_for, render_template
from flask_login import login_required, current_user
from flask_mail import Mail
from flask import g
import os
from models import db
from models.usuario import Usuario  
from config import DevelopmentConfig, mail
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from roles import require_role
from blueprints.auth import auth_bp
from blueprints.compras import compras_bp
from blueprints.inventario import inventario_bp
from blueprints.pedidos import pedidos_bp
from blueprints.produccion import produccion_bp
from blueprints.proveedores import proveedores_bp
from blueprints.recetas import recetas_bp
from blueprints.usuarios import usuarios_bp
from blueprints.ventas import ventas_bp
from blueprints.clientes import clientes_bp
from blueprints.clientes.forms import SelectProduct
from blueprints.clientes.routes import consulta_precios


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['UPLOAD_FOLDER'] = "static/uploads"

csrf = CSRFProtect(app)

db.init_app(app)

# Inicializamos Flask-Mail
mail.init_app(app)


# Configuracion Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

# Registro de blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(compras_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(recetas_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(clientes_bp)

# Rutas generales

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/")
def home():
    # Si no esta logueado el usuario lo dirige a index 
    if not current_user.is_authenticated:
        return redirect(url_for("cookiemania"))
    
    rol = current_user.rol

    if rol == 'ADMIN' or 'VENDEDOR' or 'PRODUCCION':
        # Dirigir a index (cookiemania)
        return redirect(url_for('index'))
    else:
        # Si es cliente dirigir a index de nuevo 
        return redirect(url_for('cookiemania'))
    
    # Si esta logueado, se verifica el rol

@app.route("/cookiemania")
def cookiemania():
    resultados = consulta_precios()
    create_form = SelectProduct(request.form)
    return render_template('clientes.html', form = create_form, resultados=resultados)

@app.route('/index')
@login_required
@require_role(['ADMIN', 'VENDEDOR', 'PRODUCCION'])
def index():
    return render_template('index.html')



if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all() 

    app.run(debug=True)