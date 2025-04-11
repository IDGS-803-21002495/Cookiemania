from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    IntegerField,
    FieldList,
    FormField,
    FileField,
    SubmitField,
    HiddenField,
    DecimalField
)
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed
from wtforms import ValidationError
from decimal import Decimal
from PIL import Image
from werkzeug.utils import secure_filename

from models.enums import EstadoDisponibilidad

ESTADOS_DISPONIBILIDAD = [
    ('SUFICIENTE', 'Suficiente'),
    ('POR_TERMINAR', 'Por terminar'),
    ('BAJO_INVENTARIO', 'Bajo Inventario')
]

class DetalleRecetaForm(FlaskForm):
    insumo_id = SelectField("Insumo", coerce=int, validators=[DataRequired()])
    cantidad_insumo = DecimalField(
        "Cantidad",
        validators=[DataRequired(), NumberRange(min=Decimal('0.01'))],
        places=2
    )

class RecetaCompletaForm(FlaskForm):
    receta_id = HiddenField()
    nombre_galleta = StringField("Nombre Galleta", validators=[DataRequired()])
    peso_galleta = DecimalField("Peso (gr)", validators=[DataRequired()], places=2)  # Puedes usar DecimalField si se requiere fraccional.
    # Se elimina el campo "precio_galleta" para que el precio se calcule automáticamente.
    descripcion_galleta = StringField("Descripción Galleta", validators=[DataRequired()])
    estado_disponibilidad = SelectField("Estado Disponibilidad",
        choices=ESTADOS_DISPONIBILIDAD, validators=[DataRequired()], default='SUFICIENTE')
    imagen_galleta = FileField("Imagen", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Sólo imágenes válidas')])
    
    def validate_imagen_galleta(self, field):
        # En modo creación (sin receta_id) la imagen es obligatoria.
        if not field.data and not self.receta_id.data:
            raise ValidationError("La imagen es obligatoria.")
        if field.data:
            try:
                field.data.stream.seek(0)
                img = Image.open(field.data.stream)
                img.verify()  # Lanza excepción si no es imagen.
                field.data.stream.seek(0)
            except Exception:
                raise ValidationError("El archivo subido no es una imagen válida.")

    cantidad_lote = IntegerField("Cantidad de Lote", validators=[DataRequired(), NumberRange(min=1)])
    descripcion_receta = TextAreaField("Descripción Receta", validators=[DataRequired()])

    detalles = FieldList(FormField(DetalleRecetaForm), min_entries=1)

    submit = SubmitField("Guardar Receta")
