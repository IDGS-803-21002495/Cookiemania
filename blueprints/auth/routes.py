import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message

from models import db
from models.usuario import Usuario  
from .forms import LoginForm, VerifyCodeForm
from config import mail 

from . import auth_bp

ARCHIVO_TEMP = "tokentemporal.txt"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    if request.method == 'POST':
        if form_login.validate_on_submit():
            username = form_login.username.data
            password = form_login.password.data

            # Buscamos el usuario en la base de datos
            user = Usuario.query.filter_by(username=username).first()

            # Validamos credenciales 
            if user and user.password == password:
                # Generar código aleatorio de 6 dígitos
                code = random.randint(100000, 999999)

                # Guardamos el token en un archivo temporal
                with open(ARCHIVO_TEMP, "w", encoding="utf-8") as f:
                    f.write(str(code))

                # Enviar el correo con el token
                msg = Message(
                    "Código de Verificación - Cookiemania",
                    recipients=[user.email]
                )
                msg.body = f"Tu código de verificación es: {code}"
                try:
                    mail.send(msg)
                    flash("Se envió un código a tu correo. Verifícalo por favor.", "info")
                except Exception as e:
                    flash(f"Error al enviar correo: {e}", "danger")
                    return redirect(url_for('auth.login'))

                # Guardamos el id en la sesion
                session['temp_user_id'] = user.id

                # solicitamos el token enviado
                return redirect(url_for('auth.verify_code'))
            else:
                flash("Usuario o contraseña incorrectos.", "danger")
                return redirect(url_for('auth.login'))

    
    return render_template('login.html', form=form_login)

@auth_bp.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    # Verificamo si hay un usuario en la sesión
    if 'temp_user_id' not in session:
        return redirect(url_for('auth.login'))

    form_verify = VerifyCodeForm()
    if request.method == 'POST':
        if form_verify.validate_on_submit():
            user_code = form_verify.code.data

            try:
                with open(ARCHIVO_TEMP, "r", encoding="utf-8") as f:
                    stored_code = f.read().strip()
            except FileNotFoundError:
                flash("No se encontró el token temporal. Reintenta iniciar sesión.", "warning")
                return redirect(url_for('auth.login'))

            # Comparar validamos ambos codigos
            if user_code == stored_code:
                user = Usuario.query.get(session['temp_user_id'])
                if user:
                    login_user(user)

                    session['user_id'] = user.id
                    session['rol'] = user.rol
                    session.pop('temp_user_id', None)

                    flash("Verificación exitosa. ¡Bienvenido!", "success")
                    return redirect(url_for('index'))
                else:
                    flash("Usuario no encontrado.", "danger")
                    return redirect(url_for('auth.login'))
            else:
                flash("Código de verificación inválido.", "danger")
                return redirect(url_for('auth.verify_code'))

    return render_template('verify_code.html', form=form_verify)

@auth_bp.route('/logout')
def logout():
    logout_user()       
    session.clear()     
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('auth.login'))
