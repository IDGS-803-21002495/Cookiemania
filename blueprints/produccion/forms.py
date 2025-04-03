from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, DateField, RadioField, SelectMultipleField, SelectField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange, AnyOf, InputRequired


class soliForm(FlaskForm):
    product = SelectField('product', choices=[], coerce=int, validators=[
                          DataRequired(message="Por favor seleccione un producto")])


class estatusForm(Form):
    lote_id = IntegerField('Lote ID', [validators.InputRequired(
        message="El ID del lote es obligatorio.")])
    estatus = StringField('Estatus', [
        validators.InputRequired(message="El estatus es obligatorio."),
        validators.AnyOf(
            values=["SOLICITADO", "MEZCLANDO",
                    "HORNEANDO", "ENFRIANDO", "TERMINADO"],
            message="Selecciona un estatus válido."
        )
    ])


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
