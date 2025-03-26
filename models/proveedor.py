import datetime
from models import db
from models.enums import UserStatus

# Tabla de proveedor
class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(255), nullable = False)
    numero_telefonico = db.Column(db.String(20), nullable = False)
    correo = db.Column(db.String(100), nullable = False)
    direccion = db.Column(db.String(255), nullable = False)
    fecha_registro = db.Column(db.DateTime, default = datetime.datetime.now, nullable = False)
    estado = db.Column(db.Enum(UserStatus.ACTIVO, UserStatus.INACTIVO), nullable=False, default=UserStatus.ACTIVO)