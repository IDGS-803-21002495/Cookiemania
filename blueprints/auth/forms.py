from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Regexp, Email

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres."),
        Regexp(
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            message="La contraseña debe incluir al menos una mayúscula, una minúscula, un número y un carácter especial."
        )
    ])
    submit = SubmitField('Ingresar')

class VerifyCodeForm(FlaskForm):
    code = StringField('Código de Verificación', validators=[DataRequired(message='Campo requerido')])
    submit = SubmitField('Verificar')

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='El nombre es obligatorio')])
    nombre_usuario = StringField('Nombre de Usuario', validators=[DataRequired(message='El nombre de usuario es obligatorio')])
    correo = EmailField('Correo Electrónico', validators=[DataRequired(message='El correo es obligatorio'), Email(message='Correo inválido')])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres."),
        Regexp(
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            message="La contraseña debe incluir al menos una mayúscula, una minúscula, un número y un carácter especial."
        )
    ])    