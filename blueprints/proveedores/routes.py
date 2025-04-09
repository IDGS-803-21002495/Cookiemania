from . import proveedores_bp
from models import Proveedor, LoteInsumo, Insumo, PagoProveedor
from flask import render_template, request, redirect, url_for, flash
from models import db
from flask import jsonify
import datetime
from models.enums import UserStatus
from . import forms
from flask import flash
from blueprints.proveedores.forms import ProveedorForm
from flask_wtf.csrf import CSRFProtect
from roles import require_role
from flask_login import login_required

@proveedores_bp.route('/')
@login_required
@require_role(['ADMIN'])
def lista_proveedores():
    create_form=forms.ProveedorForm2(request.form)
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html',form=create_form,proveedores=proveedores)

@proveedores_bp.route('/agregarProveedor', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN'])
def agregar_proveedor():
    create_form = forms.ProveedorForm(request.form)
    proveedores = Proveedor.query.all()
 
    if request.method == 'POST'  and create_form.validate():
        nuevo_proveedor = Proveedor(
            nombre=create_form.nombre.data,
            numero_telefonico=create_form.numero_telefonico.data,
            correo=create_form.correo.data,
            direccion=create_form.direccion.data
        )
        db.session.add(nuevo_proveedor)
        db.session.commit()
        flash("Proveedor agregado correctamente", "success")
        return redirect(url_for('proveedores.lista_proveedores'))
    return render_template('proveedores.html', form=create_form,proveedores=proveedores)

@proveedores_bp.route('/editarProveedor', methods=['POST'])
@login_required
@require_role(['ADMIN'])
def editar_proveedor():
    form = ProveedorForm(request.form)
    if request.method == 'POST' and form.validate():
        proveedor = Proveedor.query.get(request.form['id'])
        if proveedor:
            proveedor.nombre = form.nombre.data
            proveedor.numero_telefonico = form.numero_telefonico.data
            proveedor.correo = form.correo.data
            proveedor.direccion = form.direccion.data
            
            db.session.commit()
            flash("Proveedor actualizado correctamente", "success")
        else:
            flash("Proveedor no encontrado", "danger")

    return redirect(url_for('proveedores.lista_proveedores'))

@proveedores_bp.route('/eliminarProveedor/<int:id>', methods=['POST'])
@login_required
@require_role(['ADMIN'])
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get(id)
    if proveedor:
        proveedor.estado = UserStatus.INACTIVO  # Cambia el estado a INACTIVO
        db.session.commit()
        flash("Proveedor marcado como INACTIVO", "success")
    else:
        flash("Proveedor no encontrado", "danger")

    return redirect(url_for('proveedores.lista_proveedores'))

@proveedores_bp.route('/actualizarEstado/<int:id>', methods=['POST'])
@login_required
@require_role(['ADMIN'])
def actualizar_estado(id):
    proveedor = Proveedor.query.get(id)
    if not proveedor:
        flash("Proveedor no encontrado", "danger")
        return redirect(url_for('proveedores.lista_proveedores'))
    
    data = request.get_json()
    nuevo_estado = data.get("estado")

    if nuevo_estado not in ["ACTIVO", "INACTIVO"]:
        flash("Estado inválido", "warning")
        return redirect(url_for('proveedores.lista_proveedores'))

    try:
        proveedor.estado = nuevo_estado
        db.session.commit()
        return jsonify({"success": True})
        flash("Estado actualizado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error al actualizar el estado", "danger")

    return redirect(url_for('proveedores.lista_proveedores'))
