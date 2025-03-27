<<<<<<< Updated upstream
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask import g
import os
from models import db
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")
=======
from flask import Flask, redirect, url_for, render_template
from flask_mail import Mail
from models import db
from models.usuario import Usuario  
from config import DevelopmentConfig, mail
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from blueprints.auth import auth_bp
from blueprints.compras import compras_bp
from blueprints.inventario import inventario_bp
from blueprints.pedidos import pedidos_bp
from blueprints.produccion import produccion_bp
from blueprints.proveedores import proveedores_bp
from blueprints.recetas import recetas_bp
from blueprints.usuarios import usuarios_bp
from blueprints.ventas import ventas_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

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
    return Usuario.query.get(int(user_id))

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

# Rutas generales
@app.route("/")
def home():
    return redirect(url_for("index"))
>>>>>>> Stashed changes

@app.route("/index")
def index():
    return render_template('index.html')

# 7. Arranque de la aplicación
if __name__ == '__main__':
<<<<<<< Updated upstream
	csrf.init_app(app)
	db.init_app(app)

	with app.app_context():
		db.create_all()
	app.run()
=======
    with app.app_context():
        db.create_all()  

    app.run(debug=True)
>>>>>>> Stashed changes
