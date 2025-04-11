from models import db
from models.enums import UnidadBase

# Tabla de presentación de insumo
# Define las diferentes presentaciones que podria tener un insumo y su conversión a unidad base
class PresentacionInsumo(db.Model):
    __tablename__ = 'presentacioninsumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(100), nullable = False)
    cantidad_base = db.Column(db.Numeric(10,5), nullable = False)
    unidad_base = db.Column(db.Enum(UnidadBase.LITROS , UnidadBase.KILOGRAMOS, UnidadBase.UNIDADES))  
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable = False)