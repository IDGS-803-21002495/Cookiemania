from flask_login import UserMixin
from models import db
import datetime

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    rol = db.Column(db.String(50), nullable=False)      
    estado = db.Column(db.String(50), nullable=False, default='ACTIVO') 
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.now)
    ultimo_inicio_sesion = db.Column(db.DateTime)

    def is_active(self):
        return self.estado == 'ACTIVO'

    def __repr__(self):
        return f'<Usuario {self.username}>'
