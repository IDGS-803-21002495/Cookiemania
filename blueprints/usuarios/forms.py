from wtforms import Form, StringField, SelectField, EmailField, validators, ValidationError
import re


def validate_username(form, field):
    if not re.match(r'^[A-Za-z0-9_.]+$', field.data):
        raise ValidationError(
            'El nombre de usuario solo puede contener letras, números, puntos y guiones bajos.')

# para la contraseña


def validate_password(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            'La contraseña debe contener al menos una letra mayúscula.')
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            'La contraseña debe contener al menos una letra minúscula.')
    if not re.search(r'[0-9]', password):
        raise ValidationError(
            'La contraseña debe contener al menos un número.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(
            'La contraseña debe contener al menos un carácter especial.')
    if len(password) < 8:
        raise ValidationError(
            'La contraseña debe tener al menos 8 caracteres.')


def validate_nombre(form, field):
    # Validar que no tenga caracteres especiales
    if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', field.data):
        raise ValidationError(
            'El nombre solo puede contener letras y espacios.')


class usuarioForm(Form):
    nombre = StringField('nombre', [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=70, message='Ingrese un nombre válido'),
        validate_nombre  # Agregar validación personalizada
    ])

    username = StringField('username', [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=15, message='Ingrese un username válido'),
        validate_username
    ])
    email = EmailField('email', [
        validators.DataRequired(message='Campo requerido'),
        # Valida que sea un correo válido
        validators.Email(message='Ingrese un correo electrónico válido'),

        validators.Length(
            min=15, max=70, message='Ingrese un correo electrónico válido')
    ])

    rol = SelectField(
        'rol',
        validators=[validators.DataRequired(
            message="Debe seleccionar un rol.")],
        choices=[
            ('VENDEDOR', 'Vendedor'),
            ('PRODUCCION', 'Producción'),
            ('CLIENTE', 'Cliente')]
    )


class usuarioForm2(Form):
    nombre = StringField('nombre', [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=70, message='Ingrese un nombre válido'),
        validate_nombre  # Agregar validación personalizada
    ])

    username = StringField('username', [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=15, message='Ingrese un username válido'),
        validate_username
    ])

    password = StringField('password', [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(
            min=8, max=20, message='Ingrese una contraseña válida'),
        validate_password  # Agregar validación personalizada
    ])
    email = EmailField('email', [
        validators.DataRequired(message='Campo requerido'),
        # Valida que sea un correo válido
        validators.Email(message='Ingrese un correo electrónico válido'),

        validators.Length(
            min=15, max=70, message='Ingrese un correo electrónico válido')
    ])

    rol = SelectField(
        'rol',
        validators=[validators.DataRequired(
            message="Debe seleccionar un rol.")],
        choices=[('VENDEDOR', 'Vendedor'),
                 ('PRODUCCION', 'Producción'),
                 ('CLIENTE', 'Cliente')]
    )
