from flask import Flask, redirect, request, url_for, render_template
from flask_login import login_required, current_user
from flask_mail import Mail
from flask import g
import os
from models import db
from models.usuario import Usuario  
from models.detalleventa import DetalleVenta
from models.venta import Venta
from models.galleta import Galleta
from models.receta import Receta
from models.detallereceta import DetalleReceta
from models.insumo import Insumo
from models.loteinsumo import LoteInsumo
from models.presentacioninsumo import PresentacionInsumo

from config import DevelopmentConfig, mail
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from datetime import timedelta
from decimal import Decimal
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
from sqlalchemy import func
import plotly.io as pio
import plotly.express as px


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
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

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

    if rol in ['ADMIN', 'VENDEDOR', 'PRODUCCION']:
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
# Obtener las ventas diarias
    ventas_diarias = db.session.query(
        func.date(Venta.fecha_registro).label('fecha'),
        func.sum(DetalleVenta.cantidad_unidades * DetalleVenta.precio_unitario).label('total_ventas')
    ).join(DetalleVenta).group_by(func.date(Venta.fecha_registro)).all()

    # Obtener los productos más vendidos
    productos_mas_vendidos = db.session.query(
        Galleta.nombre, 
        func.sum(DetalleVenta.cantidad_unidades).label('cantidad_vendida')
    ).join(DetalleVenta).group_by(Galleta.nombre).order_by(func.sum(DetalleVenta.cantidad_unidades).desc()).limit(5).all()

    # Obtener las presentaciones más vendidas
    presentaciones_mas_vendidas = db.session.query(
        DetalleVenta.tipo_venta,
        func.sum(DetalleVenta.cantidad_unidades).label('cantidad_vendida')
    ).group_by(DetalleVenta.tipo_venta).order_by(func.sum(DetalleVenta.cantidad_unidades).desc()).all()

    # Obtener el costo de producción de las galletas
    galletas = Galleta.query.all()  # Obtener todas las galletas
    costos_produccion = []
    margenes = []
    for galleta in galletas:
        # Obtener la receta de la galleta
        receta = Receta.query.filter_by(galleta_id=galleta.id).first()
        if receta:
            total_cost_insumos = 0.0
            detalles = DetalleReceta.query.filter_by(receta_id=receta.id).all()

            for detalle in detalles:
                insumo = Insumo.query.get(detalle.insumo_id)
                lote_insumo = LoteInsumo.query.filter_by(insumo_id=detalle.insumo_id).order_by(LoteInsumo.id.desc()).first()
                if lote_insumo:
                    presentacion = PresentacionInsumo.query.get(lote_insumo.presentacion_id)
                    if presentacion and presentacion.cantidad_base:
                        cost_unit_base = float(lote_insumo.precio_unitario) / float(presentacion.cantidad_base)
                        cost_insumo = cost_unit_base * float(detalle.cantidad_insumo)
                    else:
                        cost_insumo = float(lote_insumo.precio_unitario) * float(detalle.cantidad_insumo)
                    
                    total_cost_insumos += cost_insumo

            if receta.cantidad_lote > 0:
                costo_produccion = total_cost_insumos / float(receta.cantidad_lote)
            else:
                costo_produccion = 0.0

            # Obtener el precio de venta de la galleta
            precio_venta = db.session.query(func.sum(DetalleVenta.cantidad_unidades * DetalleVenta.precio_unitario)) \
            .join(Venta, DetalleVenta.venta_id == Venta.id) \
            .filter(DetalleVenta.galleta_id == galleta.id) \
            .scalar()

            
            # Calcular margen de ganancia
            if precio_venta:
                precio_venta = Decimal(precio_venta) if not isinstance(precio_venta, Decimal) else precio_venta
                margen = precio_venta - Decimal(costo_produccion)
            else:
                margen = 0.0
            
            costos_produccion.append((galleta.nombre, costo_produccion))
            margenes.append((galleta.nombre, margen))

    # Ordenar los productos por margen de ganancia (de mayor a menor)
    margenes.sort(key=lambda x: x[1], reverse=True)

    # Crear gráfico de productos recomendados para vender (por margen de ganancia)
    nombres_productos = [m[0] for m in margenes]
    margenes_ganancia = [m[1] for m in margenes]
    fig5 = px.bar(x=nombres_productos, y=margenes_ganancia, labels={'x': 'Producto', 'y': 'Margen de Ganancia'}, title='Productos Más Rentables para Vender')
    graph5_html = pio.to_html(fig5, full_html=False)

    # Crear gráfico de ventas diarias
    fechas = [v[0] for v in ventas_diarias]
    totales = [v[1] for v in ventas_diarias]
    fig1 = px.line(x=fechas, y=totales, labels={'x': 'Fecha', 'y': 'Total de Ventas'}, title='Ventas Diarias')
    graph1_html = pio.to_html(fig1, full_html=False)

    # Crear gráfico de productos más vendidos
    productos = [p[0] for p in productos_mas_vendidos]
    cantidades = [p[1] for p in productos_mas_vendidos]
    fig2 = px.bar(x=productos, y=cantidades, labels={'x': 'Producto', 'y': 'Cantidad Vendida'}, title='Productos Más Vendidos')
    graph2_html = pio.to_html(fig2, full_html=False)

    # Crear gráfico de presentaciones más vendidas
    presentaciones = [p[0] for p in presentaciones_mas_vendidas]
    cantidades_presentaciones = [p[1] for p in presentaciones_mas_vendidas]
    fig3 = px.bar(x=presentaciones, y=cantidades_presentaciones, labels={'x': 'Presentación', 'y': 'Cantidad Vendida'}, title='Presentaciones Más Vendidas')
    graph3_html = pio.to_html(fig3, full_html=False)

    # Crear gráfico de costo de producción de galletas
    nombres_galletas = [g[0] for g in costos_produccion]
    costos = [g[1] for g in costos_produccion]
    fig4 = px.bar(x=nombres_galletas, y=costos, labels={'x': 'Galleta', 'y': 'Costo de Producción'}, title='Costo de Producción de Galletas')
    graph4_html = pio.to_html(fig4, full_html=False)

    return render_template('index.html', graph1_html=graph1_html, graph2_html=graph2_html, graph3_html=graph3_html, graph4_html=graph4_html, graph5_html=graph5_html)



@app.route("/inventarioProduccion")
def prueba():
	return render_template("inventarioProducto.html")

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all() 

    app.run(debug=True)