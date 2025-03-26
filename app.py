from flask import Flask, redirect, url_for
from models import db
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
# Importar blueprints
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
csrf = CSRFProtect()
app.config.from_object(DevelopmentConfig)
# Registrar los blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(compras_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(recetas_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(ventas_bp)

# Redirigir la página de inicio al login
@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()

	app.run(debug=True)