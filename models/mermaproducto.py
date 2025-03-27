from models import db
from models.enums import TipoMerma

# Tabla de merma de productos 
class MermaProducto(db.Model):
    __tablename__ = 'mermaproducto'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_merma = db.Column(db.Integer, nullable = False)
    fecha = db.Column(db.DateTime, nullable = False)
    tipo = db.Column(db.Enum(TipoMerma.CADUCIDAD, TipoMerma.DESPERDICIO), nullable = False)  # Se cambió 'name' por 'TipoMerma'
    lote_produccion_id = db.Column(db.Integer, db.ForeignKey('loteproduccion.id'), nullable = False)