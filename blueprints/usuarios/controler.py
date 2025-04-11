from datetime import datetime
from models.usuario import Usuario
from models import db
from flask import flash
from sqlalchemy import or_
import logging

# para regustrar Usuario


def registrarUsuario(nombre, username, email, rol, password):
    # Verificar si ya existe un usuario con el mismo nombre de usuario
    usuario_existente = Usuario.query.filter_by(username=username).first()
    if usuario_existente:
        flash(
            f"El nombre de usuario '{username}' ya está en uso. Por favor, elija otro.", "error")
        return False

    ultimo_inicio_sesion = datetime.now()

    # Crear el nuevo usuario
    nuevo_Usuario = Usuario(
        nombre=nombre,
        username=username,
        email=email,
        rol=rol,
        password=password
    )

 # Usar el método set_password para guardar la contraseña de forma segura
    nuevo_Usuario.set_password(password)

    # Guardar el nuevo usuario en la base de datos
    db.session.add(nuevo_Usuario)
    db.session.commit()

    flash(f"Usuario registrado correctamente {nombre}", "success")
    return True


def getUsuario():
    usuarios = Usuario.query.filter(
        Usuario.estado == 'ACTIVO',
        or_(Usuario.rol == 'VENDEDOR', Usuario.rol == 'PRODUCCION')
    ).all()  # Asegúrate de llamar a .all() para obtener los resultados

    print(usuarios)
    return usuarios


def getUsuarioById(usuario_id):
    # Buscar el usuario por ID
    usuario = Usuario.query.get(usuario_id)

    if usuario:
        return usuario
    else:
        flash("Usuario no encontrado.", "danger")
        return None


def actualizarUsuario(usuario_id, nombre, username, email, rol):
    # Buscar el usuario por ID
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return False

    # Verificar si el nombre de usuario ya está en uso por otro usuario
    usuario_existente = Usuario.query.filter_by(username=username).first()
    if usuario_existente and usuario_existente.id != usuario_id:
        flash(
            f"El nombre de usuario '{username}' ya está en uso. Por favor, elija otro.", "error")
        return False

    # Actualizar los atributos del usuario
    usuario.nombre = nombre
    usuario.username = username
    usuario.email = email
    usuario.rol = rol

    # Guardar los cambios en la base de datos
    db.session.commit()

    flash(f"Usuario {nombre} actualizado correctamente", "success")
    return True
