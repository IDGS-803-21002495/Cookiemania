import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from models import db
from models.usuario import Usuario  
from .forms import LoginForm, VerifyCodeForm, RegistroForm
from config import mail 
import requests
from functools import wraps
from datetime import datetime, timedelta, timezone
from flask import g

from . import auth_bp

ARCHIVO_TEMP = "tokentemporal.txt"


RECAPTCHA_SECRET_KEY = '6Lcn7gQrAAAAAKdU0DzIzxEd7-gqWEdvEUolUB1V'
RECAPTCHA_SITE_KEY = '6Lcn7gQrAAAAAPLf8pGCITzYP4JJPEQ0yUy_0c8L'

# Lista de contraseñas comunes (puedes ampliarla según sea necesario)
contraseñas_comunes = [
    '123456', 'password', '123456789', '12345', '1234', 'qwerty', 'abc123',
    'password1', '123123', 'admin', 'welcome', 'letmein', '0987654', 'admin123'
]

@auth_bp.route('/crear_usuario', methods=['POST'])
def create_user():
    form = RegistroForm()
    form_login = LoginForm()
    if request.method == 'POST' and form.validate():
        # Obtener los datos del formulario
        nombre = form.nombre.data
        username = form.nombre_usuario.data
        email = form.correo.data
        password = form.password.data
        # Asignar rol automáticamente como "Cliente"
        rol = 'CLIENTE'

        print(password)

        # Validar que no exista un usuario con ese nombre de usuario o correo electrónico
        existing_user = Usuario.query.filter((Usuario.username == username) | (Usuario.email == email)).first()
        if existing_user:
            flash('El nombre de usuario o correo electrónico ya está registrado', 'error')
            return redirect(url_for('auth.login')) 
        
        # Valirdar que la contraseña no sea comun 
        if password in contraseñas_comunes: 
            flash('Contraseña invalida, por favor, intente con otra.', 'error')
            return redirect(url_for('auth.login')) 

        # Crear una nueva instancia del usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            username=username,
            email=email,
            password=password,  
            rol=rol
        )

        # Guardar el nuevo usuario en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Redirigir a una página de éxito o al login
        flash('Usuario creado con éxito!', 'success')
        return redirect(url_for('auth.login'))
    
    # En coso que falle la valudación del formulario
    return render_template('login.html', form=form_login, form_registro=form)

def verify_recaptcha(recaptcha_response):
    secret_key = "6Lcn7gQrAAAAAKdU0DzIzxEd7-gqWEdvEUolUB1V"
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    return result.get('success', False)

@auth_bp.before_request
def before_request():
    if 'user_id' in session:
        # Verificar si la sesión ha expirado
        if not session.get('last_activity'):
            session['last_activity'] = datetime.now(timezone.utc)
        else:
            now = datetime.now(timezone.utc)
            if (now - session['last_activity']) > timedelta(minutes=10):
                flash("Tu sesión ha expirado. Por favor, inicia sesión nuevamente.", "warning")
                session.clear()  # Limpiar la sesión
                return redirect(url_for('auth.login'))
        session['last_activity'] = datetime.now(timezone.utc)  # Actualizar la última actividad

def role_required(rol):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.rol != rol:
                flash("No tienes permiso para acceder a esta página.", "danger")
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    form_registro = RegistroForm()
    
    # Inicializar contador de intentos fallidos y tiempo de bloqueo
    if 'intentos_fallidos' not in session:
        session['intentos_fallidos'] = 0
        session['bloqueo_hasta'] = None

    # Obtener la hora actual con zona horaria consciente
    now = datetime.now(timezone.utc)

    # Verificar si el usuario está bloqueado
    if session['bloqueo_hasta']:
        bloqueo_hasta = datetime.fromisoformat(session['bloqueo_hasta'])

        if now < bloqueo_hasta:
            tiempo_restante = (bloqueo_hasta - now).seconds
            flash(f"Acceso bloqueado. Intenta de nuevo en {tiempo_restante} segundos.", "danger")
            return render_template('login.html', form=form_login)

    if request.method == 'POST':
        if form_login.validate_on_submit():
            recaptcha_response = request.form.get('g-recaptcha-response')

            if not recaptcha_response or not verify_recaptcha(recaptcha_response):
                flash('Verificación de reCAPTCHA fallida. Intenta nuevamente.', 'danger')
                return redirect(url_for("auth.login"))

            username = form_login.username.data
            password = form_login.password.data

            user = Usuario.query.filter_by(username=username).first()

            # Validar credenciales
            if user and user.check_password(password):
                session['intentos_fallidos'] = 0  # Reiniciar contador
                code = random.randint(100000, 999999)

                with open(ARCHIVO_TEMP, "w", encoding="utf-8") as f:
                    f.write(str(code))

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

                session['temp_user_id'] = user.id
                return redirect(url_for('auth.verify_code'))
            else:
                # Incrementar intentos fallidos
                session['intentos_fallidos'] += 1

                if session['intentos_fallidos'] >= 3:
                    # Bloquear por 5 minutos (almacenar como string ISO 8601)
                    session['bloqueo_hasta'] = (now + timedelta(minutes=5)).isoformat()
                    session['intentos_fallidos'] = 0  # Reiniciar intentos
                    flash("Demasiados intentos fallidos. Intenta en 5 minutos.", "danger")
                else:
                    intentos_restantes = 3 - session['intentos_fallidos']
                    flash(f"Intento fallido. Te quedan {intentos_restantes} intento(s).", "warning")

                return redirect(url_for('auth.login'))

    return render_template('login.html', form=form_login, form_registro = form_registro)

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

                    if current_user.rol == 'CLIENTE':
                        return redirect(url_for('cookiemania'))
                    else:
                        return redirect(url_for('index'))
                    
                else:
                    flash("Usuario no encontrado.", "danger")
                    return redirect(url_for('auth.login'))
            else:
                flash("Código de verificación inválido.", "danger")
                return redirect(url_for('auth.verify_code'))

    return render_template('verify_code.html', form=form_verify)


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    if request.method == 'POST':
        if current_user.is_authenticated:
            # Obtener el usuario actual
            user = Usuario.query.get(current_user.id)

            if user:
                # Actualizar el campo ultimo_inicio_sesion
                user.ultimo_inicio_sesion = datetime.now()
                db.session.commit()  # Guardar los cambios en la base de datos

    logout_user()       
    session.clear()     
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('auth.login'))
