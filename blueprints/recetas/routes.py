import os
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import recetas_bp  
from .forms import RecetaCompletaForm  
from models import db
from models.galleta import Galleta
from models.receta import Receta
from models.detallereceta import DetalleReceta
from models.insumo import Insumo
from roles import require_role


def log_form_errors(form):
    for field_name, error_messages in form.errors.items():
        for error in error_messages:
            print(f"Error in {field_name}: {error}")

def asignar_relaciones(recetas):
    from models.loteinsumo import LoteInsumo
    from models.presentacioninsumo import PresentacionInsumo
    
    
    for r in recetas:
        # Asignar la galleta
        r.galleta = Galleta.query.get(r.galleta_id)
        
        # Obtener todos los detalles de la receta
        detalles = DetalleReceta.query.filter_by(receta_id=r.id).all()
        total_cost_insumos = 0.0
        
        for d in detalles:
            # Vincular el insumo
            d.insumo = Insumo.query.get(d.insumo_id)
            
            # Tomar el último lote de ese insumo 
            lote_insumo = (LoteInsumo.query
                           .filter_by(insumo_id=d.insumo_id)
                           .order_by(LoteInsumo.id.desc())
                           .first())
            if lote_insumo:
                # Opción 2: Consultar la presentación manualmente
                presentacion = PresentacionInsumo.query.get(lote_insumo.presentacion_id)
                
                if presentacion and presentacion.cantidad_base:
                    # 1. Costo por unidad base
                    cost_unit_base = float(lote_insumo.precio_unitario) / float(presentacion.cantidad_base)
                    # 2. Multiplicar por la cantidad de insumo que requiere la receta
                    cost_insumo = cost_unit_base * float(d.cantidad_insumo)
                else:
                    # En caso de no tener presentación/cantidad_base, asume lógica previa
                    cost_insumo = float(lote_insumo.precio_unitario) * float(d.cantidad_insumo)
                
                total_cost_insumos += cost_insumo
        
        # Vincular la lista de detalles a la receta
        r.detallereceta = detalles
        
        # Calcular costo de producción POR GALLETA si tiene cantidad_lote > 0
        if r.cantidad_lote and float(r.cantidad_lote) > 0:
            r.costo_produccion = total_cost_insumos / float(r.cantidad_lote)
        else:
            r.costo_produccion = 0.0
    
    return recetas



@recetas_bp.route('/', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN','VENDEDOR'])
def listar_o_crear_recetas():
    insumos = Insumo.query.all()
    insumos_choices = [(i.id, i.nombre) for i in insumos]
    form = RecetaCompletaForm()
    # En modo creación forzamos la disponibilidad "SUFICIENTE"
    form.estado_disponibilidad.data = "SUFICIENTE"
    for detalle_form in form.detalles:
        detalle_form.insumo_id.choices = insumos_choices

    if request.method == 'GET':
        recetas = Receta.query.all()
        recetas = asignar_relaciones(recetas)
        return render_template(
            'recetas.html',
            recetas=recetas,
            form=form,
            insumos=insumos,
            receta=None
        )

    if form.validate_on_submit():
        # 1. Crear la Galleta
        nueva_galleta = Galleta(
            nombre=form.nombre_galleta.data,
            peso=form.peso_galleta.data,
            precio=0,  # Se actualizará después
            descripcion=form.descripcion_galleta.data,
            estado_disponibilidad="SUFICIENTE",
            imagen=None
        )
        db.session.add(nueva_galleta)
        db.session.flush()

        # 2. Guardar la imagen, si existe
        imagen_file = form.imagen_galleta.data
        if imagen_file:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            imagen_file.stream.seek(0)
            nombre_imagen = secure_filename(imagen_file.filename)
            ruta_imagen = os.path.join(upload_folder, nombre_imagen)
            imagen_file.save(ruta_imagen)
            nueva_galleta.imagen = nombre_imagen

        # 3. Crear la Receta asociada a esa galleta
        nueva_receta = Receta(
            galleta_id=nueva_galleta.id,
            cantidad_lote=form.cantidad_lote.data,
            descripcion=form.descripcion_receta.data
        )
        db.session.add(nueva_receta)
        db.session.flush()

        # 4. Insertar Detalles de la receta y calcular costo total de insumos
        from models.loteinsumo import LoteInsumo
        from models.presentacioninsumo import PresentacionInsumo  # Para la Opción 2

        total_cost_insumos = 0.0

        for d_form in form.detalles.entries:
            # Guardar cada detalle
            nuevo_detalle = DetalleReceta(
                receta_id=nueva_receta.id,
                insumo_id=d_form.insumo_id.data,
                cantidad_insumo=d_form.cantidad_insumo.data
            )
            db.session.add(nuevo_detalle)

            # Buscar el último lote de ese insumo 
            lote_insumo = LoteInsumo.query \
                                    .filter_by(insumo_id=d_form.insumo_id.data) \
                                    .order_by(LoteInsumo.id.desc()) \
                                    .first()

            if lote_insumo:
                # Obtener la presentación asociada mediante su presentacion_id
                presentacion = PresentacionInsumo.query.get(lote_insumo.presentacion_id)

                # Si existe y tiene cantidad_base, ajustamos el costo al uso real
                if presentacion and presentacion.cantidad_base:
                    cost_unit_base = float(lote_insumo.precio_unitario) / float(presentacion.cantidad_base)
                    cost_insumo = cost_unit_base * float(d_form.cantidad_insumo.data)
                else:
                    # Si no hay presentacion o cantidad_base, fallback a lógica anterior
                    cost_insumo = float(lote_insumo.precio_unitario) * float(d_form.cantidad_insumo.data)

                total_cost_insumos += cost_insumo

        # 5. Calcular costo de producción y precio de venta
        if form.cantidad_lote.data > 0:
            costo_por_galleta = total_cost_insumos / float(form.cantidad_lote.data)
            precio_venta = (costo_por_galleta + 5) * 1.10
            nueva_galleta.precio = precio_venta

        db.session.commit()
        flash("Receta creada con éxito.", "success")
        return redirect(url_for('recetas.listar_o_crear_recetas'))
    else:
        flash("Errores en el formulario. Por favor, revise los datos.", "danger")
        log_form_errors(form)

    # Si no es GET ni es válido el formulario, recargamos
    recetas = Receta.query.all()
    recetas = asignar_relaciones(recetas)
    return render_template(
        'recetas.html',
        recetas=recetas,
        form=form,
        insumos=insumos,
        receta=None
    )

@recetas_bp.route('/editar/<int:receta_id>', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN'])
def editar_receta(receta_id):
    receta = Receta.query.get_or_404(receta_id)
    galleta = Galleta.query.get_or_404(receta.galleta_id)
    detalles = DetalleReceta.query.filter_by(receta_id=receta.id).all()

    insumos = Insumo.query.all()
    insumos_choices = [(i.id, i.nombre) for i in insumos]
    form = RecetaCompletaForm()

    # Ajustar las opciones de insumo en el form
    for detalle_form in form.detalles:
        detalle_form.insumo_id.choices = insumos_choices

    if request.method == 'GET':
        # Pre-llenar campos del formulario
        form.receta_id.data = receta.id
        form.nombre_galleta.data = galleta.nombre
        form.peso_galleta.data = galleta.peso
        form.descripcion_galleta.data = galleta.descripcion
        form.estado_disponibilidad.data = galleta.estado_disponibilidad
        form.cantidad_lote.data = receta.cantidad_lote
        form.descripcion_receta.data = receta.descripcion

        # Limpiar entradas de detalles y rellenar con lo existente
        form.detalles.entries = []
        for d in detalles:
            form.detalles.append_entry({
                "insumo_id": d.insumo_id,
                "cantidad_insumo": d.cantidad_insumo
            })
            form.detalles[-1].insumo_id.choices = insumos_choices

        return render_template(
            'editar_receta.html',
            form=form,
            galleta=galleta
        )

    if form.validate_on_submit():
        # 1. Actualizar datos de galleta
        galleta.nombre = form.nombre_galleta.data
        galleta.peso = form.peso_galleta.data
        galleta.descripcion = form.descripcion_galleta.data
        galleta.estado_disponibilidad = form.estado_disponibilidad.data

        # 2. Manejar imagen, si se subió
        imagen_file = form.imagen_galleta.data
        if imagen_file:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            imagen_file.stream.seek(0)
            nuevo_nombre = secure_filename(imagen_file.filename)
            ruta_img = os.path.join(upload_folder, nuevo_nombre)
            imagen_file.save(ruta_img)
            galleta.imagen = nuevo_nombre

        # 3. Actualizar datos de la Receta
        receta.cantidad_lote = form.cantidad_lote.data
        receta.descripcion = form.descripcion_receta.data

        # 4. Eliminar detalles previos y recalcular costos
        DetalleReceta.query.filter_by(receta_id=receta.id).delete()

        from models.loteinsumo import LoteInsumo
        from models.presentacioninsumo import PresentacionInsumo

        total_cost_insumos = 0.0
        for d_form in form.detalles.entries:
            # Guardar cada nuevo detalle
            nuevo_detalle = DetalleReceta(
                receta_id=receta.id,
                insumo_id=d_form.insumo_id.data,
                cantidad_insumo=d_form.cantidad_insumo.data
            )
            db.session.add(nuevo_detalle)

            # Tomar el lote de insumo más reciente 
            lote_insumo = (LoteInsumo.query
                           .filter_by(insumo_id=d_form.insumo_id.data)
                           .order_by(LoteInsumo.id.desc())
                           .first())
            if lote_insumo:
                # Obtener la presentación a través de presentacion_id
                presentacion = PresentacionInsumo.query.get(lote_insumo.presentacion_id)
                if presentacion and presentacion.cantidad_base:
                    cost_unit_base = float(lote_insumo.precio_unitario) / float(presentacion.cantidad_base)
                    cost_insumo = cost_unit_base * float(d_form.cantidad_insumo.data)
                else:
                    # Fallback si no hay presentacion o cantidad_base
                    cost_insumo = float(lote_insumo.precio_unitario) * float(d_form.cantidad_insumo.data)

                total_cost_insumos += cost_insumo

        # 5. Calcular costo de producción y precio de galleta
        if form.cantidad_lote.data > 0:
            costo_por_galleta = total_cost_insumos / float(form.cantidad_lote.data)
            receta.costo_produccion = costo_por_galleta  # Nuevo costo de producción
            precio_venta = (costo_por_galleta + 5) * 1.10
            galleta.precio = precio_venta
        else:
            receta.costo_produccion = 0.0
            galleta.precio = 0.0

        db.session.commit()
        flash("Receta actualizada correctamente.", "success")
        return redirect(url_for('recetas.listar_o_crear_recetas'))

    # Si no es válido el form
    for field, errors in form.errors.items():
        for error in errors:
            print(f"Error in {field}: {error}")
    flash("Errores en el formulario. Por favor, revise los datos.", "danger")
    return render_template('editar_receta.html', form=form, galleta=galleta)


@recetas_bp.route('/eliminar/<int:receta_id>', methods=['POST'])
@login_required
@require_role(['ADMIN'])
def eliminar_receta(receta_id):
    receta = Receta.query.get_or_404(receta_id)
    galleta = Galleta.query.get_or_404(receta.galleta_id)
    DetalleReceta.query.filter_by(receta_id=receta.id).delete()
    db.session.delete(receta)
    db.session.flush()
    db.session.delete(galleta)
    db.session.commit()
    flash("Receta eliminada correctamente.", "success")
    return redirect(url_for('recetas.listar_o_crear_recetas'))

