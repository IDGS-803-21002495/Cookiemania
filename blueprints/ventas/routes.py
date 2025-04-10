from flask import flash, render_template, redirect, request, url_for, session
from flask_login import login_required, current_user
from models import db, LoteProduccion, Receta, Galleta, Venta, PagoProveedor, Insumo, LoteInsumo, PresentacionInsumo, MermaInsumo, MermaProducto
from . import ventas_bp
from roles import require_role
import logging
from .forms import SelectProduct
from datetime import datetime
from sqlalchemy import desc, func, select
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
        precio_galleta = galleta.precio
        peso_galleta = galleta.peso

        # Cálculo de unidades por paquete
        unidades_completas_1000 = int(1000 // peso_galleta)
        unidades_completas_700 = int(700 // peso_galleta)

        precio_paquete_1000g = unidades_completas_1000 * precio_galleta
        precio_paquete_700g = unidades_completas_700 * precio_galleta

        # Consulta para obtener la suma de existencias de todos los lotes de esta galleta
        existencias = verificar_existencias(galleta.id)

        total_existencias = existencias.cantidad_disponible if existencias.cantidad_disponible else 0

        # Agregar la información del producto y su existencias al resultado
        resultados.append({
            'id': galleta.id,
            'nombre': galleta.nombre,
            'gramaje': galleta.peso,
            'unidad': galleta.precio,
            'imagen': galleta.imagen,
            'precio_1000g': precio_paquete_1000g,
            'unidades_1000g': unidades_completas_1000,
            'precio_700g': precio_paquete_700g,
            'unidades_700g': unidades_completas_700,
            'existencias_totales': total_existencias  
        })

    return resultados


def verificar_existencias(galleta_id): 
    # Usamos filter en lugar de filter_by
    existencias = db.session.query(
        func.sum(LoteProduccion.cantidad_disponible).label('cantidad_disponible'),
        Galleta.nombre.label('galleta_nombre'),
        Galleta.id
    ).join(
        Receta, LoteProduccion.receta_id == Receta.id
    ).join(
        Galleta, Receta.galleta_id == Galleta.id
    ).filter(
        Galleta.id == galleta_id
    ).filter(
        LoteProduccion.estado_lote == 'TERMINADO'
    ).group_by(
        Galleta.id
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
        
        # Sumar todas las unidades solicitadas de la misma galleta (sin importar la presentación)
        for item in carrito:
            if item['id_galleta'] == producto['id_galleta']:
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
    cantidad = int(cantidad)
    
    # Calcular detalles de la venta y verificar existencias
    producto, error = calcular_detalles_venta(modalidad, cantidad, int(id_galleta))
    if error:
        flash(error, 'danger')
        return redirect(url_for('venta.index'))

    carrito = session.get('carrito', [])

    # Inicializar la cantidad total con la nueva cantidad
    total_cantidad = producto['cantidades_unidades']

    # Sumar todas las unidades del mismo producto en otras presentaciones
    for item in carrito:
        if item['id_galleta'] == producto['id_galleta'] and item['tipo_venta'] != producto['tipo_venta']:
            total_cantidad += item['cantidades_unidades']

    # Verificar si la cantidad total supera las existencias
    existencias = verificar_existencias(producto['id_galleta'])
    if total_cantidad > existencias.cantidad_disponible:
        log_error(f"Stock insuficiente para el producto con ID {id_galleta}.")
        flash('No hay suficiente stock disponible para la cantidad solicitada.', 'danger')  
        return redirect(url_for('venta.index'))

    # Actualizar o agregar el producto en el carrito
    producto_existente = False
    for item in carrito:
        if item['id_galleta'] == producto['id_galleta'] and item['tipo_venta'] == producto['tipo_venta']:
            item['cantidad'] = cantidad
            item['cantidades_unidades'] = producto['cantidades_unidades']
            item['subtotal'] = producto['subtotal']
            item['presentacion'] = producto['presentacion']
            producto_existente = True
            break

    if not producto_existente:
        carrito.append(producto)

    # Guardar el carrito actualizado
    session['carrito'] = carrito
    session.modified = True

    flash("Producto actualizado correctamente", "success")
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

# Función para obtener todas las salidas de efectivo 
def obtener_salidas_efectivo_proveedores():
    hoy = datetime.today().date()

    pagos = (
        db.session.query(
            PagoProveedor.fecha,
            LoteInsumo.cantidad,
            PresentacionInsumo.nombre.label('presentacion'),
            Insumo.nombre.label('insumo'),
            PagoProveedor.monto
        )
        .join(LoteInsumo, PagoProveedor.lote_insumo_id == LoteInsumo.id)
        .join(Insumo, LoteInsumo.insumo_id == Insumo.id)
        .join(PresentacionInsumo, LoteInsumo.presentacion_id == PresentacionInsumo.id)
        .filter(func.date(PagoProveedor.fecha) == hoy)
        .all()
    )

    resultados = []
    for pago in pagos:
        motivo = f"Compra de {int(pago.cantidad)} {pago.presentacion.lower()} de {pago.insumo.lower()}"
        resultados.append({
            'fecha': pago.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'motivo': motivo,
            'cantidad': float(pago.cantidad),
            'total': float(pago.monto)
        })

    return resultados

# Función para obtener la merma de insumos 
def obtener_merma_insumo():
    hoy = datetime.today().date()

    mermas = (
        db.session.query(
            MermaInsumo.fecha,
            Insumo.nombre.label('insumo'),
            MermaInsumo.cantidad_merma
        )
        .join(Insumo, MermaInsumo.insumo_id == Insumo.id)
        .filter(func.date(MermaInsumo.fecha) == hoy)
        .all()
    )

    resultados = []
    for merma in mermas:
        # Obtener último lote para precio estimado
        ultimo_lote = (
            db.session.query(LoteInsumo.precio_unitario)
            .filter(LoteInsumo.insumo_id == merma.insumo_id)
            .order_by(desc(LoteInsumo.id))
            .first()
        )
        precio_unitario = float(ultimo_lote.precio_unitario) if ultimo_lote else 0
        total_perdido = float(merma.cantidad_merma) * precio_unitario

        resultados.append({
            'hora': merma.fecha.strftime('%H:%M:%S'),
            'producto_insumo': merma.insumo,
            'cantidad': float(merma.cantidad_merma),
            'total_perdido': round(total_perdido, 2)
        })

    return resultados
    
# Función para obtener todas las ventas hechas en el dia
def obtener_detalles_ventas_hoy():
    hoy = datetime.today().date()

    detalles = (
        db.session.query(
            Venta.fecha_registro,
            Galleta.nombre.label('nombre_galleta'),
            DetalleVenta.tipo_venta,
            DetalleVenta.cantidad_presentacion.label('cantidad_presentacion'),
            (DetalleVenta.precio_unitario * DetalleVenta.cantidad_unidades).label('subtotal')
        )
        .join(DetalleVenta, Venta.id == DetalleVenta.venta_id)
        .join(Galleta, Galleta.id == DetalleVenta.galleta_id)
        .filter(func.date(Venta.fecha_registro) == hoy)
        .filter(Venta.estado.in_(['LISTO', 'ENTREGADO', 'PENDIENTE']))
        .all()
    )

    resultados = []
    for detalle in detalles:

        producto = ''

        if detalle.tipo_venta == 'UNIDAD':
            producto = f'{detalle.cantidad_presentacion} unidad(es) de {detalle.nombre_galleta}'
        elif detalle.tipo_venta == 'PAQUETE1':
            producto = f'{detalle.cantidad_presentacion} paquete(s) de 1 kg de {detalle.nombre_galleta}'
        elif detalle.tipo_venta == 'PAQUETE2':
            producto = f'{detalle.cantidad_presentacion} paquete(s) de 700 gr de {detalle.nombre_galleta}'
        elif detalle.tipo_venta == 'GRAMOS':
            producto = f'{detalle.cantidad_presentacion} gramos de {detalle.nombre_galleta}'

        resultados.append({
            'fecha_hora': detalle.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
            'producto': producto,
            'cantidad': int(detalle.cantidad_presentacion),
            'subtotal': float(detalle.subtotal)
        })

    return resultados
    

@ventas_bp.route('/corte_venta', methods = ['GET', 'POST'])
def corte_venta():
    egresos = obtener_salidas_efectivo_proveedores()
    ventas = obtener_detalles_ventas_hoy()
    total_ventas = sum(float(item['subtotal']) for item in ventas)
    total_egresos = sum(float(item['total']) for item in egresos)
    total_esperado = (float(total_ventas) - (float(total_egresos)))
    return render_template('corte_venta.html', ventas = ventas, egresos = egresos, total_esperado = total_esperado)