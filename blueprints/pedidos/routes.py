import datetime
from . import pedidos_bp
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from roles import require_role
import logging
from models import db, Venta, DetalleVenta, Galleta, Usuario, LoteProduccion, Receta
from sqlalchemy import func


# Configuración de logs 
logging.basicConfig(
    filename='auditoria_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def registrar_log_modificacion(usuario_id, venta_id, descripcion, cantidad, subtotal, accion):
    log_message = f"Usuario: {usuario_id}, Venta: {venta_id}, Descripción: {descripcion}, Cantidad: {cantidad}, Subtotal: {subtotal}, Acción: {accion}"
    logging.info(log_message)

def log_error(error_message):
    logging.error(f"Error: {error_message}")

def recuperar_pedidos():
    consulta = (
        db.session.query(
            Venta.id.label('venta_id'),
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
        .group_by(Venta.id, Usuario.nombre, Venta.estado, Venta.fecha_registro, DetalleVenta.tipo_venta, DetalleVenta.cantidad_presentacion, Galleta.nombre)
        .all()  
    )



    # Transformar la consulta en un diccionario anidado
    ventas_dict = {}

    for row in consulta:
        venta_id = row.venta_id
        cliente_nombre = row.cliente_nombre
        venta_estatus = row.venta_estatus
        fecha_registro = row.fecha_registro
        subtotal_venta = row.subtotal_venta
        tipo_venta = row.tipo_venta
        cantidad_presentacion = row.cantidad_presentacion
        galleta_nombre = row.galleta_nombre

        if venta_estatus == 'PENDIENTE':
            venta_estatus = 'Pendiente'
        elif venta_estatus == 'CANCELADO':
            venta_estatus = 'Cancelado'
        elif venta_estatus == 'ENTREGADO':
            venta_estatus = 'Entregado'
        

        # Agregar venta si no esta ya en el diccionario
        if venta_id not in ventas_dict:
            ventas_dict[venta_id] = {
                'cliente_nombre': cliente_nombre,
                'venta_estatus': venta_estatus,
                'fecha_registro': fecha_registro,
                'total_venta': 0,
                'detalles': []  
            }

        # Calcular total 
        ventas_dict[venta_id]['total_venta'] += subtotal_venta

        # Descripción personalizada para la cantidad y tipo de presentación
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

        # Detalle de venta
        detalle = {
            'tipo_venta': tipo_venta,
            'cantidad_presentacion': cantidad_presentacion,
            'galleta_nombre': galleta_nombre,
            'subtotal_venta': subtotal_venta,
            'descripcion_presentacion': descripcion_presentacion
        }
        ventas_dict[venta_id]['detalles'].append(detalle)
    
    return ventas_dict
    
# Mostrar todos los pedidos 
@pedidos_bp.route('/', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN','VENDEDOR'])
def index():
    # Recuperar todos los pedidos
    pedidos_venta = recuperar_pedidos()
    # Mostrar pantalla inicial
    return render_template('pedidos.html', pedidos = pedidos_venta)

# Cancelar un pedido (su estatus pasa a CANCELADO)
@pedidos_bp.route('/cancelar/<int:venta_id>', methods = ['POST'])
@login_required
@require_role(['ADMIN','VENDEDOR'])
def cancelar(venta_id):
    # Obtener venta con el id
    venta = Venta.query.get_or_404(venta_id)

    # Registrar log de cancelación
    registrar_log_modificacion(
        usuario_id=current_user.id,
        venta_id=venta_id,  
        descripcion=f"Pedido cancelado por el usuario {current_user.nombre}.",
        cantidad=0,  
        subtotal=0,  
        accion="Cancelación"
    )

    # Actualizar estatus 
    venta.estado = 'CANCELADO'
    db.session.commit()

    # Mostrar mensaje flash 
    flash(f"Pedido cancelado", "warning")

    return redirect(url_for('pedidos.index'))

@pedidos_bp.route('/atender/<int:venta_id>', methods=['POST'])
@require_role(['ADMIN','VENDEDOR'])
@login_required
def atender(venta_id):
    # Obtener los detalles de la venta y sumar las unidades por cada galleta
    detalles_venta = db.session.query(
        Galleta.id.label('galleta_id'),
        Galleta.nombre.label('galleta_nombre'),
        Receta.id.label('receta_id'),
        func.sum(DetalleVenta.cantidad_unidades).label('unidades_totales'),
        func.sum(DetalleVenta.precio_unitario * DetalleVenta.cantidad_unidades).label('total_venta'),
        LoteProduccion.cantidad_disponible.label('unidades_disponibles')
    ).join(
        DetalleVenta, DetalleVenta.galleta_id == Galleta.id
    ).join(
        Receta, Galleta.id == Receta.galleta_id
    ).join(
        LoteProduccion, LoteProduccion.receta_id == Receta.id
    ).filter(
        DetalleVenta.venta_id == venta_id
    ).group_by(
        Galleta.id, Galleta.nombre, LoteProduccion.cantidad_disponible, Receta.id
    ).all()


    # Comprobar si hay suficiente stock para cada lote de cada galleta
    for detalle in detalles_venta:
        if detalle.unidades_totales > detalle.unidades_disponibles:
            log_error(f"Stock insuficiente para el producto {detalle.galleta_nombre}.")
            flash(f'Stock insuficiente para completar el pedido de {detalle.galleta_nombre}.', 'error')
            return redirect(url_for('pedidos.index'))

    # Descontar las unidades vendidas de los lotes
    for detalle in detalles_venta:
        # Obtener los lotes disponibles de la galleta
        lotes = LoteProduccion.query.filter_by(receta_id=detalle.receta_id).order_by(LoteProduccion.fecha_produccion).all()

        # Unidades que se van a vender en total
        unidades_restantes = detalle.unidades_totales  

        for lote in lotes:
            if unidades_restantes <= 0:
                # Si ya se descontaron todas las unidades se termina con el descuento a los lotes
                break  

            if lote.cantidad_disponible > 0:
                unidades_a_descuento = min(lote.cantidad_disponible, unidades_restantes)  
                # Descontar unidades del lote
                lote.cantidad_disponible -= unidades_a_descuento  
                # Restar las unidades descontadas
                unidades_restantes -= unidades_a_descuento  

                db.session.commit()  

    # Registrar log de cancelación (ahora iteramos sobre cada detalle de la venta)
    for detalle in detalles_venta:
        registrar_log_modificacion(
            usuario_id=current_user.id,
            venta_id=venta_id,  
            descripcion=f"Pedido atendido por el usuario {current_user.nombre}.",
            cantidad=detalle.unidades_totales,  
            subtotal=detalle.total_venta,  
            accion="Pedido entregado"
        )

    # Si todo está bien, cambiar el estatus de la venta a "ENTREGADO"
    venta = Venta.query.get(venta_id)
    venta.estado = 'ENTREGADO'
    venta.vendedor_id = current_user.id
    db.session.commit()

    flash('Pedido atendido correctamente', 'success')
    return redirect(url_for('pedidos.index'))