from flask import flash, render_template, redirect, request, url_for, session
from flask_login import login_required, current_user
from models import db, LoteProduccion, Receta, Galleta, Venta
from . import ventas_bp
from roles import require_role
import logging
from .forms import SelectProduct
from datetime import datetime
from sqlalchemy import func, select
from models import db, Venta, DetalleVenta, LoteProduccion
from models.enums import EstadoVenta

# Configuración de logs 
logging.basicConfig(
    filename='auditoria_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def registrar_log_modificacion(usuario_id, galleta_id, descripcion, cantidad, subtotal, accion):
    log_message = f"Usuario: {usuario_id}, Galleta: {galleta_id}, Descripción: {descripcion}, Cantidad: {cantidad}, Subotal: {subtotal}, Acción: {accion}"
    logging.info(log_message)

def log_error(error_message):
    logging.error(f"Error: {error_message}")

# Recuperar datos de la galleta, calculando la cantidad de unidades y costo de cada paquete
def consulta_precios():
    galletas = Galleta.query.all()
    resultados = []

    for galleta in galletas:
        peso_galleta = galleta.peso
        precio_galleta = galleta.precio

        unidades_completas_1000 = int(1000 // peso_galleta)
        unidades_completas_700 = int(700 // peso_galleta)

        precio_paquete_1000g = unidades_completas_1000 * precio_galleta
        precio_paquete_700g = unidades_completas_700 * precio_galleta

        resultados.append({
            'id': galleta.id,
            'nombre': galleta.nombre,
            'gramaje': galleta.peso,
            'unidad': galleta.precio,
            'precio_1000g': precio_paquete_1000g,
            'unidades_1000g': unidades_completas_1000,
            'precio_700g': precio_paquete_700g,
            'unidades_700g': unidades_completas_700
        })

    return resultados

def verificar_existencias(galleta_id): 
    # Usamos filter en lugar de filter_by
    existencias = db.session.query(
        LoteProduccion.cantidad_disponible,
        Galleta.nombre.label('galleta_nombre'),
        Galleta.id
    ).join(
        Receta, LoteProduccion.receta_id == Receta.id
    ).join(
        Galleta, Receta.galleta_id == Galleta.id
    ).filter(
        Galleta.id == galleta_id  
    ).first()

    return existencias
    
def calcular_detalles_venta(modalidad, cantidad, galleta_id):
    # Buscar la galleta en la base de datos
    galleta = Galleta.query.get(galleta_id)
    if not galleta:
        log_error(f"Galleta con ID {galleta_id} no encontrada en la base de datos.")
        return None, "Galleta no encontrada"

    # Definir tipo de venta, presentación y unidades por presentación 
    if modalidad == 'Unidad':
        tipo_venta = 'UNIDAD'
        presentacion = f'{cantidad} unidad(es)'
        cantidad_unidades = int(cantidad)
    elif modalidad == 'Paquete1':
        tipo_venta = 'PAQUETE1'
        presentacion = f'{cantidad} paquete(s) de 1 kg'
        unidades_por_paquete = 1000 // galleta.peso
        cantidad_unidades = cantidad * unidades_por_paquete
    elif modalidad == 'Paquete2':
        tipo_venta = 'PAQUETE2'
        presentacion = f'{cantidad} paquete(s) de 700 g'
        unidades_por_paquete = 700 // galleta.peso
        cantidad_unidades = cantidad * unidades_por_paquete
    elif modalidad == 'Gramos':
        tipo_venta = 'GRAMAJE'
        presentacion = f'{cantidad} gramos'
        cantidad_unidades = int(cantidad) // galleta.peso
    else:
        return "Modalidad no válida", 400
    
    # Verificar existencias antes de proceder con la venta
    existencia = verificar_existencias(galleta_id)
    if existencia.cantidad_disponible < cantidad_unidades:
        return None, 'No hay suficiente stock disponible'

    # Calcular subtotal
    subtotal = int(cantidad_unidades) * galleta.precio

    # Crear el producto a agregar
    producto = {
        'id_galleta': galleta.id,
        'nombre': galleta.nombre,
        'precio': galleta.precio,
        'presentacion': presentacion,
        'modalidad': modalidad,
        'tipo_venta': tipo_venta,
        'cantidad': cantidad,
        'cantidades_unidades': cantidad_unidades,
        'subtotal': subtotal
    }

    return producto, None

@ventas_bp.route('/', methods=['GET'])
@login_required
@require_role(['ADMIN','VENDEDOR'])
def index():
    create_form = SelectProduct(request.form)
    resultados = consulta_precios()
    carrito = session.get('carrito', [])
    total_pendientes = Venta.query.filter_by(estado='PENDIENTE').count()
    total = sum(float(item['subtotal']) for item in carrito)
    return render_template('ventas.html', resultados=resultados, form=create_form, total = total, total_pendientes = total_pendientes)


@ventas_bp.route('/add_product', methods=['POST']) 
@require_role(['ADMIN','VENDEDOR'])
@login_required
def add_product(): 
    form = SelectProduct()
    if form.validate() and request.method == 'POST':  
        modalidad = form.modalidad.data
        cantidad = int(form.cantidad.data)
        id_galleta = request.form.get('id_galleta')

        # Calcular detalles de la venta
        producto, error = calcular_detalles_venta(modalidad, cantidad, id_galleta)
        
        if error == 'No hay suficiente stock disponible':
            log_error(f"Stock insuficiente para el producto con ID {id_galleta}.")
            flash('No hay suficiente stock disponible.', 'danger')  
            return redirect(url_for('venta.index'))
        
        # Verificar si la cantidad total del producto en el carrito supera la cantidad existente en inventario
        total_cantidad = producto['cantidades_unidades']
        
        carrito = session.get('carrito', [])
        
        # Buscar la cantidad total del producto en el carrito
        for item in carrito:
            if item['id_galleta'] == producto['id_galleta'] and item['tipo_venta'] == producto['tipo_venta']:
                total_cantidad += item['cantidades_unidades']
        
        # Verificar si la cantidad total supera las existencias
        existencias = verificar_existencias(producto['id_galleta'])
        if total_cantidad > existencias.cantidad_disponible:
            log_error(f"Stock insuficiente para el producto con ID {id_galleta}.")
            flash('No hay suficiente stock disponible para la cantidad solicitada.', 'danger')  
            return redirect(url_for('venta.index'))
        
        # Si no hay error, agregar el producto al carrito
        session.setdefault('carrito', [])
                
        # Verificar si el producto ya existe en el carrito
        producto_existente = False
        for item in session['carrito']:
            if item['id_galleta'] == producto['id_galleta'] and item['tipo_venta'] == producto['tipo_venta']:
                item['cantidad'] = cantidad
                item['subtotal'] = producto['subtotal']
                producto_existente = True
                break

        if not producto_existente:
            session['carrito'].append(producto)

        session.modified = True

        # Redirigir a la página de ventas con el carrito actualizado
        return redirect(url_for('venta.index'))

    flash("Error en el formulario. Verifica los campos.", "danger")
    return redirect(url_for('venta.index'))


@ventas_bp.route('/update_product/<string:id_galleta>/<string:modalidad>/<string:cantidad>', methods=['POST'])
@login_required
@require_role(['ADMIN','VENDEDOR'])
def update_product(id_galleta, modalidad, cantidad):

    # Calcular detalles de la venta y verificar existencias
    producto, error = calcular_detalles_venta(modalidad, int(cantidad), int(id_galleta))
    
    print(error)

    if error == 'No hay suficiente stock disponible':
        print('Sin stock al actualizar')
        log_error(f"Stock insuficiente para el producto con ID {id_galleta}.")
        flash('No hay suficiente stock disponible.', 'danger')  
        return redirect(url_for('venta.index'))
    else:
        # Si el producto ya está en el carrito, actualizar su cantidad y subtotal
        carrito = session.get('carrito', [])
        producto_existente = False

        for item in carrito:
            if item['id_galleta'] == producto['id_galleta'] and item['tipo_venta'] == producto['tipo_venta']:
                item['cantidad'] = cantidad
                item['subtotal'] = producto['subtotal']
                item['presentacion'] = producto['presentacion']
                producto_existente = True
                break



        # Si el producto no estaba en el carrito, lo agregamos
        if not producto_existente:
            carrito.append(producto)
            
        # Guardar los cambios en el carrito
        session['carrito'] = carrito
        session.modified = True

        # Redirigir a la página de ventas con el carrito actualizado
        return redirect(url_for('venta.index'))


@ventas_bp.route('/delete_product/<int:id_product>/<string:presentacion>', methods=['POST'])
@login_required
@require_role(['ADMIN','VENDEDOR'])
def delete_product(id_product,presentacion):
    # Aquí se elimina el producto del carrito
    carrito = session.get('carrito', [])
    session['carrito'] = [item for item in carrito if not (item['id_galleta'] == id_product and item['presentacion'] == presentacion)]
    session.modified = True  
    
    print("Carrito actualizado después de eliminar el producto:", session['carrito'])
    flash('Producto eliminado','warning')
    return redirect(url_for('venta.index'))  


@ventas_bp.route('/add_venta', methods=['POST'])
@login_required
@require_role(['ADMIN','VENDEDOR'])
def add_venta():

    print("Carrito vaciado:", session['carrito'])
    
    carrito = session.get('carrito', [])
    total = sum(float(item['subtotal']) for item in carrito)

    # Crear la venta
    nueva_venta = Venta(
        fecha_registro=datetime.now(),
        fecha_entrega=datetime.now(),  
        estado=EstadoVenta.ENTREGADO,
        vendedor_id= current_user.id,
        cliente_id=None  
    )

    print(current_user.id)
    # Guardar venta
    db.session.add(nueva_venta)
    db.session.commit()

    # Registrar detalles de la venta y descontar del inventario
    for item in carrito:
        cantidad_a_vender = item['cantidades_unidades']

        # Registrar el detalle de la venta en el log
        registrar_log_modificacion(
            usuario_id=current_user.id,
            galleta_id=item['id_galleta'],
            descripcion=f"Producto vendido: {item['nombre']}",
            cantidad=item['cantidades_unidades'],
            subtotal=item['subtotal'],
            accion="Venta completada"
        )

        # Recuperar id de receta
        receta = Receta.query.filter_by(galleta_id=item['id_galleta']).first()
        receta_id = receta.id
        
        # Buscar lotes disponibles de esta galleta ordenados por fecha de producción
        lotes = LoteProduccion.query.filter_by(receta_id=receta_id).order_by(LoteProduccion.fecha_produccion).all()
        
        for lote in lotes:
            if cantidad_a_vender <= 0:
                break
            
            if lote.cantidad_disponible >= cantidad_a_vender:
                lote.cantidad_disponible -= cantidad_a_vender
                cantidad_a_vender = 0  
            else:
                cantidad_a_vender -= lote.cantidad_disponible
                lote.cantidad_disponible = 0  

            db.session.add(lote)  

        # Guardar detalle de la venta
        detalle = DetalleVenta(
            venta_id=nueva_venta.id,
            galleta_id= item['id_galleta'],
            cantidad_unidades=item['cantidades_unidades'],
            cantidad_presentacion=item['cantidad'],
            precio_unitario=float(item['precio']),
            tipo_venta = item['tipo_venta'],
        )
        db.session.add(detalle)

    # Guardar cambios finales en la BD
    db.session.commit()

    flash(f"Pedido registrado correctamente. Total a pagar: ${total}", "success")

    session['carrito'] = []  
    session.modified = True  

    return redirect(url_for('venta.index'))  
    
    