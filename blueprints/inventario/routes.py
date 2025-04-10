from . import inventario_bp

from flask import render_template, request, redirect, url_for, flash
from models import db
from flask import jsonify
from flask import session
import datetime
from models import db, LoteInsumo, Insumo, PresentacionInsumo
from . import forms
from decimal import Decimal, InvalidOperation
from flask import flash
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect
from models import db, Compra, LoteInsumo, Insumo, PresentacionInsumo, Proveedor , PagoProveedor

@inventario_bp.route('/')
@login_required 
def mostrar_insumos():
    print(f"ID del usuario autenticado: {current_user.id}")  
    insumos = (
        db.session.query(
            Insumo.id.label("insumo_id"),
            Insumo.nombre.label("nombre_insumo"),
            db.func.sum(LoteInsumo.cantidad_disponible).label("total_cantidad_disponible"),
            db.func.min(LoteInsumo.fecha_caducidad).label("fecha_caducidad_proxima"),
            Insumo.unidad_medida.label("unidadMedida")
        )
        .join(Insumo, LoteInsumo.insumo_id == Insumo.id)
        .join(PresentacionInsumo, LoteInsumo.presentacion_id == PresentacionInsumo.id)
        .filter(LoteInsumo.cantidad_disponible > 0)  # Filtra solo lotes con cantidad disponible
        .group_by(Insumo.id, PresentacionInsumo.id, LoteInsumo.presentacion_id, PresentacionInsumo.nombre)
        .all()
    ) 
    carrito = session.get('carrito', [])
    proveedores = db.session.query(Proveedor).all()
    presentaciones = db.session.query(PresentacionInsumo).all()

    return render_template('inventario.html', insumos=insumos, proveedores=proveedores, presentaciones=presentaciones)

@inventario_bp.route('/surtir', methods=['GET', 'POST'])
@login_required
def surtir_inventario():
    if request.method == 'POST':
        insumo_id = request.form['insumo_id']
        proveedor_id = request.form['proveedor_id']
        presentacion_id = request.form['presentacion_id']
        cantidad = float(request.form['cantidad'])
        precio_unitario=float(request.form['precio_unitario'])
        fecha_caducidad = datetime.datetime.strptime(request.form['fecha_caducidad'], "%Y-%m-%d")

        # Obtener la presentación del insumo
        presentacion = db.session.query(PresentacionInsumo).filter_by(id=presentacion_id).first()
        cantidad_base = presentacion.cantidad_base

        # Calcular la cantidad total a ingresar en LoteInsumo
        cantidad_total = Decimal(cantidad) * Decimal(cantidad_base)


        flash("Insumo agregado al carrito", "success")
        return redirect(url_for('inventario.mostrar_insumos'))

    # Obtener todos los proveedores, presentaciones e insumos para cargar en el modal
    insumos = db.session.query(Insumo).all()
    proveedores = db.session.query(Proveedor).all()
    presentaciones = db.session.query(PresentacionInsumo).all()

    # Imprimir en consola para verificar
    print("Proveedores:")
    for proveedor in proveedores:
        print(f"ID: {proveedor.id}, Nombre: {proveedor.nombre}")

    print("Presentaciones de insumos:")
    for presentacion in presentaciones:
        print(f"ID: {presentacion.id}, Nombre: {presentacion.nombre}")

    return render_template('inventario.html', insumos=insumos, proveedores=proveedores, presentaciones=presentaciones)

@inventario_bp.route('/agregar_al_carrito', methods=['POST'])
@login_required
def agregar_al_carrito():
    insumo_id = request.form['insumo_id']
    cantidad = request.form['cantidad']
    precio_unitario = request.form['precio_unitario']
    proveedor_id = request.form['proveedor_id']
    fecha_caducidad = request.form['fecha_caducidad']

    # Validaciones básicas
    if not insumo_id or not cantidad or not precio_unitario or not proveedor_id or not fecha_caducidad:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for('inventario.mostrar_insumos'))

    # Convertir valores
    try:
        cantidad = Decimal(cantidad)
        precio_unitario = Decimal(precio_unitario)
        fecha_caducidad = datetime.datetime.strptime(fecha_caducidad, '%Y-%m-%d').date()
    except (ValueError, InvalidOperation):
        flash("Error en el formato de los datos.", "danger")
        return redirect(url_for('inventario.mostrar_insumos'))

    # Obtener insumo
    insumo = db.session.query(Insumo).filter_by(id=insumo_id).first()
    if not insumo:
        flash("El insumo no existe", "danger")
        return redirect(url_for('inventario.mostrar_insumos'))

    # Obtener la presentación asociada al insumo
    presentacion = db.session.query(PresentacionInsumo).filter_by(insumo_id=insumo.id).first()
    if not presentacion:
        flash("La presentación del insumo no está disponible", "danger")
        return redirect(url_for('inventario.mostrar_insumos'))

    # Calcular cantidad total
    cantidad_disponible = cantidad * Decimal(presentacion.cantidad_base)

    # Inicializar carrito si no existe
    if 'carrito' not in session:
        session['carrito'] = []

    # Verificar si el insumo ya está en el carrito
    existe = False
    for item in session['carrito']:
        if item['insumo_id'] == insumo_id:
            item['cantidad'] = str(Decimal(item['cantidad']) + cantidad)
            item['cantidad_disponible'] = str(Decimal(item['cantidad_disponible']) + cantidad_disponible)
            item['subtotal'] = str(Decimal(item['cantidad']) * precio_unitario)
            existe = True
            break

    # Si el insumo no está en el carrito, lo agregamos
    if not existe:
        subtotal = cantidad * precio_unitario
        session['carrito'].append({
            'insumo_id': insumo_id,
            'nombre': insumo.nombre,
            'cantidad': str(cantidad),
            'precio_unitario': str(precio_unitario),
            'subtotal': str(subtotal),
            'presentacion_id': presentacion.id,
            'presentacion': presentacion.nombre, 
            'proveedor_id': proveedor_id,
            'cantidad_disponible': str(cantidad_disponible),
            'fecha_caducidad': fecha_caducidad.strftime('%Y-%m-%d')
        })

    flash("Producto agregado al carrito", "success")

    # Calcular total del carrito
    session['total'] = str(sum(Decimal(item['subtotal']) for item in session['carrito']))
    

    return redirect(url_for('inventario.mostrar_insumos'))



@inventario_bp.route('/realizar_compra', methods=['POST'])
@login_required
def realizar_compra():
    carrito = session.get('carrito', [])
    if not carrito:
        flash("El carrito está vacío. Agrega productos antes de comprar.", "danger")
        return redirect(url_for('inventario.mostrar_insumos'))

    print(f"Carrito recuperado de sesión: {carrito}")  # Debugging

    total_compra = Decimal(0)
    lotes_creados = []  # Lista para almacenar los lotes creados

    # Crear un nuevo registro de compra
    nueva_compra = Compra(usuario_id=current_user.id, fecha_compra=datetime.datetime.now().date())
    db.session.add(nueva_compra)
    db.session.commit()

    print(f"Compra creada con ID: {nueva_compra.id}")  # Debugging

    # Procesar cada ítem del carrito
    for item in carrito:
        try:
            insumo_id = item.get('insumo_id')
            cantidad = Decimal(item.get('cantidad'))
            precio_unitario = Decimal(item.get('precio_unitario'))
            proveedor_id = item.get('proveedor_id')
            presentacion_id = item.get('presentacion_id')
            cantidad_disponible = Decimal(item.get('cantidad_disponible'))
            fecha_caducidad = datetime.datetime.strptime(item.get('fecha_caducidad'), '%Y-%m-%d').date()

            # Validar insumo y presentación
            insumo = db.session.query(Insumo).filter_by(id=insumo_id).first()
            presentacion = db.session.query(PresentacionInsumo).filter_by(id=presentacion_id).first()
            if not insumo or not presentacion:
                flash(f"Error: Insumo o presentación no encontrados para el ID {insumo_id}.", "danger")
                continue

            # Insertar en LoteInsumo
            nuevo_lote = LoteInsumo(
                compra_id=nueva_compra.id,
                insumo_id=insumo.id,
                proveedor_id=proveedor_id,
                presentacion_id=presentacion.id,
                precio_unitario=precio_unitario,
                cantidad=cantidad,
                cantidad_disponible=cantidad_disponible,
                fecha_caducidad=fecha_caducidad
            )
            db.session.add(nuevo_lote)
            db.session.commit()  # Se confirma la inserción de cada lote

            print(f"Lote creado: {nuevo_lote.id} para insumo {insumo.nombre}")  # Debugging

            total_compra += precio_unitario * cantidad

            # Guardamos el lote creado para registrar pagos después
            lotes_creados.append(nuevo_lote)

        except Exception as e:
            db.session.rollback()
            print(f"Error al procesar el insumo {item.get('nombre')}: {str(e)}")
            flash(f"Error al registrar el insumo {item.get('nombre')}.", "danger")
            continue

    # Registrar un pago por cada lote creado
    for lote in lotes_creados:
        pago = PagoProveedor(
            proveedor_id=lote.proveedor_id,
            fecha=datetime.datetime.now().date(),
            monto=lote.precio_unitario * lote.cantidad,
            lote_insumo_id=lote.id  # Cada pago se asocia a su lote correspondiente
        )
        db.session.add(pago)
        db.session.commit()
        print(f"Pago registrado: {pago.id} por un monto de {pago.monto} asociado al lote {pago.lote_insumo_id}")  # Debugging

    # Limpiar el carrito después de la compra
    session.pop('carrito', None)
    session['total'] = '0'  # Establecer el total en 0 después de la compra

    flash("Compra realizada exitosamente", "success")
    return redirect(url_for('inventario.mostrar_insumos'))

@inventario_bp.route('/eliminar_del_carrito', methods=['POST'])
@login_required
def eliminar_del_carrito():
    insumo_id = request.form['insumo_id']
    carrito = session.get('carrito', [])

    # Filtramos el carrito para eliminar el insumo
    carrito = [item for item in carrito if item['insumo_id'] != insumo_id]

    # Guardamos el carrito actualizado en la sesión
    session['carrito'] = carrito

    # Si el carrito está vacío, aseguramos que el total de la compra sea 0
    if not carrito:
        session['total'] = '0'
    else:
        session['total'] = str(sum(Decimal(item['cantidad']) * Decimal(item['precio_unitario']) for item in carrito))

    flash("Insumo eliminado del carrito", "success")
    return redirect(url_for('inventario.mostrar_insumos'))


@inventario_bp.route('/mermar_inventario', methods=['POST'])
@login_required
def mermar_inventario():
    insumo_id = request.form['insumo_id']
    presentacion_id = request.form['presentacion_id']
    cantidad = int(request.form['cantidad'])

    # Obtener la presentación del insumo
    presentacion = db.session.query(PresentacionInsumo).filter_by(id=presentacion_id).first()
    if not presentacion:
        flash("La presentación del insumo no está disponible", "danger")
        return redirect(url_for('inventario.mostrar_insumos'))

    # Calcular la cantidad total desperdiciada
    cantidad_base = presentacion.cantidad_base
    cantidad_total_desperdiciada = cantidad * cantidad_base

    # Obtener los lotes del insumo con cantidad disponible mayor a 0
    lotes = db.session.query(LoteInsumo).filter_by(insumo_id=insumo_id).filter(LoteInsumo.cantidad_disponible > 0).order_by(LoteInsumo.fecha_caducidad.asc()).all()

    # Descontar la cantidad desperdiciada de los lotes
    cantidad_restante = cantidad_total_desperdiciada
    for lote in lotes:
        if cantidad_restante > 0:
            cantidad_a_descontar = min(lote.cantidad_disponible, cantidad_restante)
            lote.cantidad_disponible -= cantidad_a_descontar
            cantidad_restante -= cantidad_a_descontar
            db.session.commit()
            print(f"Lote {lote.id} actualizado: cantidad disponible = {lote.cantidad_disponible}")

    if cantidad_restante > 0:
        flash("No se pudo descontar la cantidad total desperdiciada", "danger")
    else:
        flash("Cantidad desperdiciada descontada correctamente", "success")

    return redirect(url_for('inventario.mostrar_insumos'))

@inventario_bp.route('/agregar_insumo', methods=['POST'])
@login_required
def agregar_insumo():
    try:
        
        print("Solicitud recibida:", request.form)
        # Obtener datos del formulario
        nombre_insumo = request.form['nombre_insumo']
        unidad_medida = request.form['unidadMedida']
        presentacion_nombre = request.form['presentacion']
        cantidad_presentacion = Decimal(request.form['cantidad_presentacion'])
        precio_unitario = Decimal(request.form['precio_unitario'])
        cantidad_comprada = Decimal(request.form['cantidad_comprada'])
        fecha_caducidad = datetime.datetime.strptime(request.form['fecha_caducidad_insumo'], "%Y-%m-%d").date()
        proveedor_id = request.form['proveedor_id']

        # Insertar en Insumo
        nuevo_insumo = Insumo(nombre=nombre_insumo, unidad_medida=unidad_medida)
        db.session.add(nuevo_insumo)
        db.session.flush()  # Obtener ID del insumo recién insertado

        # Insertar en PresentacionInsumo
        nueva_presentacion = PresentacionInsumo(
            nombre=presentacion_nombre,
            cantidad_base=cantidad_presentacion,
            unidad_base=unidad_medida,
            insumo_id=nuevo_insumo.id
        )
        db.session.add(nueva_presentacion)
        db.session.flush()  # Obtener ID de la presentación recién insertada

        # Insertar en Compra
        nueva_compra = Compra(fecha_compra=datetime.datetime.now(), usuario_id=current_user.id)
        db.session.add(nueva_compra)
        db.session.flush()  # Obtener ID de la compra recién insertada

        # Calcular cantidad disponible en LoteInsumo
        cantidad_disponible = cantidad_comprada * cantidad_presentacion

        # Insertar en LoteInsumo
        nuevo_lote = LoteInsumo(
            precio_unitario=precio_unitario,
            cantidad=cantidad_comprada,
            cantidad_disponible=cantidad_disponible,
            fecha_caducidad=fecha_caducidad,
            compra_id=nueva_compra.id,
            insumo_id=nuevo_insumo.id,
            presentacion_id=nueva_presentacion.id,
            proveedor_id=proveedor_id
        )
        db.session.add(nuevo_lote)
        db.session.flush() 

        # Calcular monto total de la compra
        monto_total = cantidad_comprada * precio_unitario

        # Insertar en PagoProveedor
        nuevo_pago = PagoProveedor(
            fecha=datetime.datetime.now(),
            monto=monto_total,
            proveedor_id=proveedor_id,
            lote_insumo_id=nuevo_lote.id
        )
        db.session.add(nuevo_pago)

        # Confirmar transacción
        db.session.commit()

        flash("Insumo agregado correctamente.", "success")
        return redirect(url_for('inventario.mostrar_insumos'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al agregar insumo: {str(e)}", "danger")
        return redirect(url_for('inventario.mostrar_insumos'))