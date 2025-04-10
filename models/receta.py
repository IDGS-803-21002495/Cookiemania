from models import db

# Tabla de receta
class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_lote = db.Column(db.Integer, nullable = False)
    descripcion = db.Column(db.Text, nullable = False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galleta.id'), nullable = False)