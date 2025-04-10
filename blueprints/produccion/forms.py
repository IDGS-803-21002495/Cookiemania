from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, DateField, RadioField, SelectMultipleField, SelectField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange, AnyOf, InputRequired


class soliForm(FlaskForm):
    product = SelectField('product', choices=[], coerce=int, validators=[
                          DataRequired(message="Por favor seleccione un producto")])
    cantidad_lote = IntegerField('cantidad_lote', [
        validators.DataRequired(
            message='Ingrese la cantidad de lotes que desea producir'),
        NumberRange(min=1, max=30, message="La cantidad debe ser mayor a 0.")
    ])


class estatusForm(Form):
    lote_id = IntegerField('Lote ID', [validators.InputRequired(
        message="El ID del lote es obligatorio.")])
    estatus = StringField('Estatus', [
        validators.InputRequired(message="El estatus es obligatorio."),
        validators.AnyOf(
            values=["SOLICITADO", "MEZCLANDO",
                    "HORNEANDO", "ENFRIANDO", "TERMINADO", "CANCELADO"],
            message="Selecciona un estatus válido."
        )
    ])

# Form de merma


class MermaForm(Form):
    lote_id = SelectField(
        'Lote',
        validators=[DataRequired(message="Debe seleccionar un lote.")],
        choices=[],  # Se llenará dinámicamente
        coerce=int  # Asegura que el valor sea un entero
    )

    cantidad = IntegerField(
        'Cantidad de Merma',
        validators=[
            DataRequired(message="Debe ingresar una cantidad."),
            NumberRange(min=1, message="La cantidad debe ser mayor a 0.")
        ]
    )

    motivo = SelectField(
        'Motivo',
        validators=[DataRequired(message="Debe seleccionar un motivo.")],
        choices=[('CADUCIDAD', 'Caducidad'),
                 ('DESPERDICIO', 'Daño en producto')]
    )
