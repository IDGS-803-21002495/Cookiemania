from models import db

# Tabla de Insumo 
class Insumo(db.Model):
    __tablename__ = 'insumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(255), nullable = False)
    unidad_medida = db.Column(db.String(50), nullable = False)