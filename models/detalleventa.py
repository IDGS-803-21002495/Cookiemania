from models import db
from models.enums import TipoVenta

# Tabla de detalle de venta 
class DetalleVenta(db.Model):
    __tablename__ = 'detalleventa'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_unidades = db.Column(db.Integer, nullable = False)
    cantidad_presentacion = db.Column(db.Integer, nullable = False)
    precio_unitario = db.Column(db.Numeric(10,2), nullable = False)
    tipo_venta = db.Column(db.Enum(TipoVenta.GRAMAJE, TipoVenta.UNIDAD, TipoVenta.PAQUETE1, TipoVenta.PAQUETE2), nullable = False)  # Se cambió 'name' por 'TipoVenta'
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable = False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galleta.id'), nullable = False)