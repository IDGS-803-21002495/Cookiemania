from models import db
from models.enums import EstadoLote

# Tabla de lote de producción 
class LoteProduccion(db.Model):
    __tablename__ = 'loteproduccion'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha_produccion = db.Column(db.DateTime, nullable = False)
    fecha_caducidad = db.Column(db.DateTime, nullable = False)
    cantidad_disponible = db.Column(db.Integer, nullable = False)
    estado_lote = db.Column(db.Enum(EstadoLote.SOLICITADO, EstadoLote.MEZCLANDO, EstadoLote.HORNEANDO, EstadoLote.ENFRIANDO, EstadoLote.TERMINADO, EstadoLote.CANCELADO), nullable=False)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable = False)