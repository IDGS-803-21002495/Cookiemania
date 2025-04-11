from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SurtirInsumoForm(FlaskForm):
    insumo_id = SelectField("Insumo", coerce=int, validators=[DataRequired()])
    cantidad = DecimalField("Cantidad", validators=[
        DataRequired(message="La cantidad es requerida"),
        NumberRange(min=0, message="La cantidad no puede ser negativa")
    ])
    presentacion_id = SelectField("Presentación", coerce=int, validators=[DataRequired()])
    precio_unitario = DecimalField("Precio Unitario", validators=[DataRequired()])
    proveedor_id = SelectField("Proveedor", coerce=int, validators=[DataRequired()])
    fecha_caducidad = DateField("Fecha de Caducidad", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Surtir Insumo")