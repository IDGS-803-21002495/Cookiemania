import datetime
from models import db
from models.enums import UserRole, UserStatus

# Tabla de Usuarios 
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    rol = db.Column(db.Enum(UserRole.ADMIN, UserRole.VENDEDOR, UserRole.PRODUCCION, UserRole.CLIENTE), nullable=False)
    estado = db.Column(db.Enum(UserStatus.ACTIVO, UserStatus.INACTIVO), nullable=False, default=UserStatus.ACTIVO)
    fecha_registro = db.Column(db.DateTime, default = datetime.datetime.now, nullable = False)
    ultimo_inicio_sesion = db.Column(db.DateTime)
