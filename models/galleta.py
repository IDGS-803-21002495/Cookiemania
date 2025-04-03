from models import db
from models.enums import EstadoDisponibilidad

# Tabla de galleta
class Galleta(db.Model):
    _tablename_ = 'galleta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    estado_disponibilidad = db.Column(db.Enum(EstadoDisponibilidad.SUFICIENTE,EstadoDisponibilidad.POR_TERMINAR,EstadoDisponibilidad.BAJO_INVENTARIO),nullable=False)
    imagen = db.Column(db.String(255), nullable=True)