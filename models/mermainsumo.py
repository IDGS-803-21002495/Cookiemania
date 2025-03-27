from models import db
from models.enums import TipoMerma

# Tabla de merma de insumo 
class MermaInsumo(db.Model):
    __tablename__ = 'mermainsumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_merma = db.Column(db.Numeric(10,2), nullable = False)
    fecha = db.Column(db.DateTime, nullable = False)
    tipo = db.Column(db.Enum(TipoMerma.CADUCIDAD, TipoMerma.DESPERDICIO), nullable = False)  # Se cambió 'name' por 'TipoMerma'
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable = False)
