import datetime
from models import db
# Tabla de compra
class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha_compra = db.Column(db.DateTime, nullable = False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)