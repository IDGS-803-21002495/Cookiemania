from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import InputRequired, NumberRange

class SelectProduct(FlaskForm):
    modalidad = SelectField(
        'Modalidad de venta',
        choices=[('Unidad', 'Unidad'), ('Paquete1', 'Paquete de 1 kilogramo'), ('Paquete2', 'Paquete de 700 gramos'), ('Gramos', 'Gramos')],
        validators=[InputRequired(message="Por favor, selecciona una modalidad.")]
    )
    
    cantidad = IntegerField(
        'Cantidad',
        validators=[InputRequired(message="Por favor, ingresa una cantidad."), 
                    NumberRange(min=1, message="La cantidad debe ser al menos 1."), 
                    DataRequired(message="Por favor, ingresa una cantidad.")]
    )

