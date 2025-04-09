from . import usuarios_bp
from flask import render_template, request, flash, session, redirect, url_for
from blueprints.usuarios.controler import registrarUsuario, getUsuario, getUsuarioById, actualizarUsuario
from blueprints.usuarios.forms import usuarioForm, usuarioForm2
from models.usuario import Usuario
from models import db
from flask_login import login_required, current_user
from roles import require_role


@usuarios_bp.route('/')
@login_required
@require_role(['ADMIN'])
def usuarios():
    usuario_class = usuarioForm(request.form)
    usuarios = getUsuario()

    return render_template("usuarios.html", form=usuario_class, usuarios=usuarios)


@usuarios_bp.route('/registros', methods=["GET", "POST"])
@login_required
@require_role(['ADMIN'])
def registros():
    registrar_class = usuarioForm2(request.form)

    if request.method == 'POST' and registrar_class.validate():
        nombre = registrar_class.nombre.data
        username = registrar_class.username.data
        password = registrar_class.password.data
        email = registrar_class.email.data
        rol = registrar_class.rol.data

        registrarUsuario(nombre, username, email, rol, password)
        return redirect(url_for('usuarios.usuarios'))

    return render_template("insertarUsuario.html", form=registrar_class)


@usuarios_bp.route('/actualizar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN'])
def actualizar(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    registrar_class = usuarioForm(request.form)

    if request.method == 'POST' and registrar_class.validate():
        usuario.nombre = registrar_class.nombre.data
        usuario.username = registrar_class.username.data
        usuario.email = registrar_class.email.data
        usuario.rol = registrar_class.rol.data
        db.session.commit()
        flash(f"Usuario actualizado correctamente", "success")
        return redirect(url_for('usuarios.usuarios'))

    registrar_class.nombre.data = usuario.nombre
    registrar_class.username.data = usuario.username
    registrar_class.email.data = usuario.email
    registrar_class.rol.data = usuario.rol

    return render_template("verdetalle_usuario.html", form=registrar_class, usuario=usuario)


@usuarios_bp.route('/eliminar/<int:usuario_id>', methods=["GET", "POST"])
@login_required
@require_role(['ADMIN'])
def eliminar(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.estado = "INACTIVO"

    db.session.commit()
    flash(f"Usuario {usuario.nombre} eliminado correctamente.", "success")

    return redirect(url_for('usuarios.usuarios'))
