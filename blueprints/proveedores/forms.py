from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ProveedorForm(Form):
    nombre = StringField("Nombre", validators=[
        DataRequired(message="El campo nombre es requerido"),
        Length(min=4, max=50, message="Ingresa un nombre válido")
    ])
    numero_telefonico = StringField("Número Telefónico", validators=[
        DataRequired(message="El número telefónico es requerido"),
        Length(min=8, max=15, message="Número inválido")
    ])
    correo = StringField("Correo Electrónico", validators=[
        DataRequired(message="El correo es obligatorio"),
        Email(message="Ingresa un correo válido")
    ])
    direccion = StringField("Dirección", validators=[
        DataRequired(message="La dirección es obligatoria"),
        Length(max=200, message="La dirección es muy larga")
    ])
    submit = SubmitField("Agregar Proveedor")


class ProveedorForm2(Form):
    nombre = StringField("Nombre", validators=[
        DataRequired(message="El campo nombre es requerido"),
        Length(min=4, max=50, message="Ingresa un nombre válido")
    ])
    numero_telefonico = StringField("Número Telefónico", validators=[
        DataRequired(message="El número telefónico es requerido"),
        Length(min=8, max=15, message="Número inválido")
    ])
    correo = StringField("Correo Electrónico", validators=[
        DataRequired(message="El correo es obligatorio"),
        Email(message="Ingresa un correo válido")
    ])
    direccion = StringField("Dirección", validators=[
        DataRequired(message="La dirección es obligatoria"),
        Length(max=200, message="La dirección es muy larga")
    ])


