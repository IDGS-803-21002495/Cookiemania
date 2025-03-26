from models import db

# Tabla de detalle receta
class DetalleReceta(db.Model):
    __tablename__ = 'detallereceta'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_insumo = db.Column(db.Numeric(10,2), nullable = False)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable = False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable = False)

