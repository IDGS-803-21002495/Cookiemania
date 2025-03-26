from models import db

# Tabla de producción insumo 
class ProduccionInsumo(db.Model):
    __tablename__ = 'produccioninsumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_usada = db.Column(db.Numeric(10,2), nullable = False)
    lote_produccion_id = db.Column(db.Integer, db.ForeignKey('loteproduccion.id'), nullable = False)
    lote_insumo_id = db.Column(db.Integer, db.ForeignKey('loteinsumo.id'), nullable = False)