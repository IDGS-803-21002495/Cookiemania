from flask import flash, render_template, redirect, request, url_for, session, jsonify, get_flashed_messages, abort
from flask_login import login_required, current_user
from models import db, LoteProduccion, Receta, Galleta
from . import clientes_bp
from .forms import SelectProduct
from datetime import datetime
from models import db, Venta, DetalleVenta, Receta, LoteProduccion, Galleta, Usuario
from models.enums import EstadoVenta, TipoVenta
from sqlalchemy import func
from roles import require_role

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
            'imagen':galleta.imagen,
            'precio_1000g': precio_paquete_1000g,
            'unidades_1000g': unidades_completas_1000,
            'precio_700g': precio_paquete_700g,
            'unidades_700g': unidades_completas_700
        })

    return resultados

def verificar_existencias(galleta_id): 
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
        return None, "Galleta no encontrada"

    # Definir tipo de venta, presentación y unidades por presentación 
    if modalidad == 'Unidad':
        tipo_venta = 'UNIDAD'
        presentacion = f'{cantidad} unidad(es)'
        cantidad_unidades = int(cantidad)
    elif modalidad == 'Paquete1':
        tipo_venta = 'PAQUETE2'
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



@clientes_bp.route('/', methods=['GET'])
def index():
    create_form = SelectProduct(request.form)
    resultados = consulta_precios()
    carrito = session.get('carrito', [])
    total = sum(float(item['subtotal']) for item in carrito)
    return render_template('clientes.html', resultados=resultados, form=create_form, total = total)


@clientes_bp.route('/add_product', methods=['POST']) 
@login_required
@require_role(['CLIENTE'])
def add_product(): 
    form = SelectProduct()
    if form.validate() and request.method == 'POST':  
        modalidad = form.modalidad.data
        cantidad = int(form.cantidad.data)
        id_galleta = request.form.get('id_galleta')

        # Calcular detalles de la venta
        producto, error = calcular_detalles_venta(modalidad, cantidad, id_galleta)
        
        if error == 'No hay suficiente stock disponible':
            print('Sin stock')
            flash('No hay suficiente stock disponible.', 'danger')  
            return redirect(url_for('clientes.index'))
        
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
            flash('No hay suficiente stock disponible para la cantidad solicitada.', 'danger')  
            return redirect(url_for('clientes.index'))
        
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
        return redirect(url_for('clientes.index'))

    flash("Error en el formulario. Verifica los campos.", "danger")
    return redirect(url_for('clientes.index'))


@clientes_bp.route('/update_product/<string:id_galleta>/<string:modalidad>/<string:cantidad>', methods=['POST'])
@login_required
@require_role(['CLIENTE'])
def update_product(id_galleta, modalidad, cantidad):
    # Calcular detalles de la venta y verificar existencias
    producto, error = calcular_detalles_venta(modalidad, int(cantidad), int(id_galleta))
    
    if error == 'No hay suficiente stock disponible':
        flash('No hay suficiente stock disponible.', 'danger')
        return redirect(url_for('clientes.index'))
    else:
        carrito = session.get('carrito', [])
        producto_existente = False

        for item in carrito:
            # Coinciden galleta y tipo_venta
            if item['id_galleta'] == producto['id_galleta'] and item['tipo_venta'] == producto['tipo_venta']:
                # Se actualizan TODOS los campos relevantes
                item['cantidad'] = cantidad  # Cantidad de paquetes o unidades según la modalidad
                item['cantidades_unidades'] = producto['cantidades_unidades']  # Total de galletas resultantes
                item['subtotal'] = producto['subtotal']  # Subtotal recalculado
                item['presentacion'] = producto['presentacion']  # Texto tipo "2 paquete(s) de 1kg"
                # item['precio'] = producto['precio']  # Si llegara a variar el precio unitario
                producto_existente = True
                break

        if not producto_existente:
            # Si no se encontró en el carrito, se añade
            carrito.append(producto)
            
        session['carrito'] = carrito
        session.modified = True
        
        return redirect(url_for('clientes.index'))



@clientes_bp.route('/delete_product/<int:id_product>/<string:presentacion>', methods=['POST'])
@login_required
@require_role(['CLIENTE'])
def delete_product(id_product,presentacion):
    # Aquí se elimina el producto del carrito
    carrito = session.get('carrito', [])
    session['carrito'] = [item for item in carrito if not (item['id_galleta'] == id_product and item['presentacion'] == presentacion)]
    session.modified = True  
    
    print("Carrito actualizado después de eliminar el producto:", session['carrito'])
    flash('Producto eliminado','warning')
    return redirect(url_for('clientes.index'))  


@clientes_bp.route('/add_pedido', methods=['POST'])
@login_required
@require_role(['CLIENTE'])
def add_pedido():
    carrito = session.get('carrito', [])
    if not carrito:
        flash('No hay productos en el carrito.', 'warning')
        return redirect(url_for('clientes.index'))

    fecha_entrega_str = request.form.get('fecha_entrega')
    if not fecha_entrega_str:
        flash("Por favor selecciona una fecha de entrega.", "danger")
        return redirect(url_for('clientes.index'))

    # Validar la fecha de entrega
    try:
        fecha_entrega_date = datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()
        if fecha_entrega_date < datetime.now().date():
            flash("La fecha de entrega no puede ser anterior a hoy.", "danger")
            return redirect(url_for('clientes.index'))
    except ValueError:
        flash("Fecha de entrega inválida.", "danger")
        return redirect(url_for('clientes.index'))

    total = sum(float(item['subtotal']) for item in carrito)

    # Crear la venta con estado PENDIENTE y cliente_id del usuario logueado
    nueva_venta = Venta(
        fecha_registro=datetime.now(),
        fecha_entrega=datetime.combine(fecha_entrega_date, datetime.min.time()),
        estado=EstadoVenta.PENDIENTE,
        vendedor_id=None,
        cliente_id=current_user.id
    )
    db.session.add(nueva_venta)
    db.session.commit()

    for item in carrito:
        if item['modalidad'] == 'Unidad':
            tipo_venta = TipoVenta.UNIDAD
            cantidad_presentacion = item['cantidad']
            cantidad_unidades = item['cantidades_unidades']

        elif item['modalidad'] == 'Gramos':
            tipo_venta = TipoVenta.GRAMAJE
            cantidad_presentacion = item['cantidad']
            cantidad_unidades = item['cantidades_unidades']

        elif item['modalidad'] == 'Paquete1':
            # Paquete de 1kg
            tipo_venta = TipoVenta.PAQUETE1
            cantidad_presentacion = item['cantidad']
            cantidad_unidades = item['cantidades_unidades']

        elif item['modalidad'] == 'Paquete2':
            # Paquete de 700g
            tipo_venta = TipoVenta.PAQUETE2
            cantidad_presentacion = item['cantidad']
            cantidad_unidades = item['cantidades_unidades']
        else:
            flash("Modalidad de venta no válida.", "danger")
            return redirect(url_for('clientes.index'))

        # Crear el detalle de venta c
        detalle = DetalleVenta(
            cantidad_unidades=cantidad_unidades,
            cantidad_presentacion=cantidad_presentacion,
            precio_unitario=float(item['precio']),
            tipo_venta=tipo_venta,
            venta_id=nueva_venta.id,
            galleta_id=item['id_galleta']
        )
        db.session.add(detalle)

    db.session.commit()

    flash(f"Pedido registrado correctamente. Total: ${total}.", "success")
    session['carrito'] = []
    session.modified = True

    return redirect(url_for('clientes.index'))

def recuperar_mis_pedidos(usuario_id):
    consulta = (
        db.session.query(
            Venta.id.label('venta_id'),
            Venta.fecha_entrega.label('fecha_entrega'),
            Usuario.nombre.label('cliente_nombre'),
            Venta.estado.label('venta_estatus'),
            Venta.fecha_registro.label('fecha_registro'),
            func.sum(DetalleVenta.cantidad_unidades * DetalleVenta.precio_unitario).label('subtotal_venta'),
            DetalleVenta.tipo_venta.label('tipo_venta'),
            DetalleVenta.cantidad_presentacion.label('cantidad_presentacion'),
            Galleta.nombre.label('galleta_nombre')
        )
        .join(Usuario, Venta.cliente_id == Usuario.id)
        .join(DetalleVenta, Venta.id == DetalleVenta.venta_id)
        .join(Galleta, DetalleVenta.galleta_id == Galleta.id)
        .filter(Venta.cliente_id == usuario_id)  
        .group_by(
            Venta.id, 
            Venta.fecha_entrega, 
            Usuario.nombre, 
            Venta.estado, 
            Venta.fecha_registro, 
            DetalleVenta.tipo_venta, 
            DetalleVenta.cantidad_presentacion, 
            Galleta.nombre
        )
        .order_by(Venta.fecha_registro.desc())
        .all()
    )

    ventas_dict = {}
    for row in consulta:
        venta_id = row.venta_id
        fecha_entrega = row.fecha_entrega
        cliente_nombre = row.cliente_nombre
        venta_estatus = row.venta_estatus
        fecha_registro = row.fecha_registro
        subtotal_venta = float(row.subtotal_venta)
        tipo_venta = row.tipo_venta
        cantidad_presentacion = row.cantidad_presentacion
        galleta_nombre = row.galleta_nombre

        if venta_estatus == 'PENDIENTE':
            venta_estatus = 'Pendiente'
        elif venta_estatus == 'CANCELADO':
            venta_estatus = 'Cancelado'
        elif venta_estatus == 'ENTREGADO':
            venta_estatus = 'Entregado'

        if venta_id not in ventas_dict:
            ventas_dict[venta_id] = {
                'cliente_nombre': cliente_nombre,
                'venta_estatus': venta_estatus,
                'fecha_registro': fecha_registro,
                'fecha_entrega': fecha_entrega,
                'total_venta': 0.0,
                'detalles': []
            }

        ventas_dict[venta_id]['total_venta'] += subtotal_venta

        if tipo_venta == 'UNIDAD':
            descripcion_presentacion = f"{cantidad_presentacion} unidad(es) de {galleta_nombre}"
        elif tipo_venta == 'PAQUETE1':
            descripcion_presentacion = f"{cantidad_presentacion} paquete(s) de 1 kilogramo de {galleta_nombre}"
        elif tipo_venta == 'PAQUETE2':
            descripcion_presentacion = f"{cantidad_presentacion} paquete(s) de 700 gramos de {galleta_nombre}"
        elif tipo_venta == 'GRAMAJE':
            descripcion_presentacion = f"{cantidad_presentacion} gramo(s) de {galleta_nombre}"
        else:
            descripcion_presentacion = f"{cantidad_presentacion} {tipo_venta}"

        detalle = {
            'tipo_venta': tipo_venta,
            'cantidad_presentacion': cantidad_presentacion,
            'galleta_nombre': galleta_nombre,
            'subtotal_venta': subtotal_venta,
            'descripcion_presentacion': descripcion_presentacion
        }
        ventas_dict[venta_id]['detalles'].append(detalle)

    return ventas_dict

@clientes_bp.route('/misPedidos', methods=['GET'])
@login_required
@require_role(['CLIENTE'])
def misPedidos():
    
    pedidos_venta = recuperar_mis_pedidos(current_user.id)
    return render_template('pedidosclientes.html', pedidos=pedidos_venta)

@clientes_bp.route('/cancelar/<int:venta_id>', methods=['POST'])
@login_required
def cancelar(venta_id):
    
    venta = db.session.get(Venta, venta_id)
    if not venta:
        abort(404)  # Lanza un 404 si no existe
    if venta.cliente_id != current_user.id:
        flash("No puedes cancelar un pedido que no te pertenece.", "danger")
        return redirect(url_for('clientes.misPedidos'))

    if venta.estado == 'PENDIENTE':
        venta.estado = 'CANCELADO'
        db.session.commit()
        flash("Pedido cancelado correctamente.", "warning")
    else:
        flash("No se puede cancelar un pedido que no esté pendiente.", "danger")

    return redirect(url_for('clientes.misPedidos'))

@clientes_bp.route('/cambiar_fecha/<int:venta_id>', methods=['POST'])
@login_required
@require_role(['CLIENTE'])
def cambiar_fecha(venta_id):
    
    venta = db.session.get(Venta, venta_id)
    if not venta:
        abort(404)

    if venta.cliente_id != current_user.id:
        flash("No puedes modificar un pedido que no te pertenece.", "danger")
        return redirect(url_for('clientes.misPedidos'))

    if venta.estado != 'PENDIENTE':
        flash("Solo puedes modificar la fecha de un pedido pendiente.", "danger")
        return redirect(url_for('clientes.misPedidos'))

    nueva_fecha = request.form.get('nueva_fecha_entrega', None)
    if not nueva_fecha:
        flash("Debes seleccionar una fecha de entrega.", "danger")
        return redirect(url_for('clientes.misPedidos'))

    try:
        fecha_entrega_dt = datetime.strptime(nueva_fecha, '%Y-%m-%d').date()
        hoy = datetime.now().date()
        if fecha_entrega_dt < hoy:
            flash("La fecha de entrega no puede ser anterior a hoy.", "danger")
            return redirect(url_for('clientes.misPedidos'))
    except ValueError:
        flash("Formato de fecha inválido.", "danger")
        return redirect(url_for('clientes.misPedidos'))

    venta.fecha_entrega = datetime.combine(fecha_entrega_dt, datetime.min.time())
    db.session.commit()
    flash("Fecha de entrega actualizada correctamente.", "success")

    return redirect(url_for('clientes.misPedidos'))