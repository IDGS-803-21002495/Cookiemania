from models import db
from models.enums import EstadoVenta

# Tabla de venta 
class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha_registro = db.Column(db.DateTime, nullable = False)
    fecha_entrega = db.Column(db.DateTime, nullable = False)
    estado = db.Column(db.Enum(EstadoVenta.PENDIENTE, EstadoVenta.CANCELADO, EstadoVenta.PRODUCCION, EstadoVenta.ENTREGADO), default = EstadoVenta.PENDIENTE)  # Se cambió 'name' por 'EstadoVenta'
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = True)
