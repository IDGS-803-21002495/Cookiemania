from flask import render_template, request, flash, session, redirect, url_for
from .import produccion_bp
from blueprints.produccion.controler import registromerma, getGalleta, getFechaCaducidas, procesarproduccion, estatusGalleta, actualizarEstatus, getlotes
from blueprints.produccion import forms
from blueprints.produccion.forms import soliForm, estatusForm, MermaForm
from flask_login import login_required, current_user
from roles import require_role


@produccion_bp.route('/')
# @login_required
# @require_role(['ADMIN', 'VENDEDOR', 'PRODUCCION'])
def produccion():

    galletas = getGalleta()
    sol_clase = soliForm()
    cantidadMinima = 49

    for loteproduccion in galletas:
        cantidad = loteproduccion.cantidad_total
        if cantidad <= cantidadMinima:
            flash(
                f"La cantidad de {loteproduccion.nombre} es baja. Solo quedan {cantidad} unidades.", "danger")

    proximaACaducar = getFechaCaducidas()
    for lote in proximaACaducar:
        galleta = lote.nombre
        fecha_caducidad = lote.fecha_caducidad_proxima.strftime("%d/%m/%Y")
        cantidad = lote.cantidad_disponible

        if cantidad > 0:
            flash(
                f"La galleta {galleta} caducará el {fecha_caducidad}. Se perderán {cantidad} unidades.", "warning")

    return render_template("invetarioProduccion.html", galletas=galletas, form=sol_clase)


# Maneja las solicitudes
@produccion_bp.route('/solicitar_produccion', methods=["GET", "POST"])
@login_required
@require_role(['ADMIN', 'VENDEDOR'])
def solicitar():
    galletas = getGalleta()
    sol_clase = soliForm(request.form)
    sol_clase.product.choices = [
        (str(galleta.id), galleta.nombre) for galleta in galletas]

    if request.method == "POST" and sol_clase.validate():
        id = int(sol_clase.product.data)

        resultado = procesarproduccion(id)

        flash(resultado["mensaje"],
              "success" if "registrado" in resultado["mensaje"] else "danger")

        return redirect(url_for("produccion.produccion"))

    return render_template('invetarioProduccion.html', form=sol_clase, galletas=galletas)


# Manejo de estatus
@produccion_bp.route('/estatusProduccion', methods=["GET", "POST"])
# @login_required
# @require_role(['PRODUCCION'])
def estatusProduccion():
    form = estatusForm(request.form)
    estatusLote = estatusGalleta()

    if request.method == "POST" and form.validate():
        lote_id = form.lote_id.data
        nuevo_estatus = form.estatus.data

        if actualizarEstatus(lote_id, nuevo_estatus):

            return redirect(url_for("produccion.estatusProduccion"))

    return render_template("estatus.html", estatusLote=estatusLote, form=form)

# Para registrar la merma


@produccion_bp.route('/merma', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN', 'VENDEDOR', 'PRODUCCION'])
def merma():
    merma_class = MermaForm(request.form)

    # Llenar opciones del select
    lotes = getlotes()
    print("Lotes disponibles:", lotes)  # Debugging
    merma_class.lote_id.choices = [
        (lote.id, f"{lote.nombre_galleta} - Cant: {lote.cantidad_disponible}") for lote in lotes
    ]

    if request.method == 'POST':
        if merma_class.validate():
            success, message = registromerma(
                merma_class.lote_id.data,
                merma_class.cantidad.data,
                merma_class.motivo.data
            )

            if success:
                flash(message, "success")
                return redirect(url_for("produccion.merma"))

            flash(message, "danger")
        else:
            print(merma_class.errors)  # Debugging de errores del formulario
            flash("Formulario inválido", "danger")

        return redirect(url_for("produccion.merma"))

    return render_template("registroMerma.html", form=merma_class, lotes=lotes)
