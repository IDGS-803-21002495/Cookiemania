from models import db

# Tabla de lote de insumo 
class LoteInsumo(db.Model):
    __tablename__ = 'loteinsumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    precio_unitario = db.Column(db.Numeric(10,2), nullable = False)
    cantidad = db.Column(db.Numeric(10,2), nullable = False)
    cantidad_disponible = db.Column(db.Numeric(10,2), nullable = False)
    fecha_caducidad = db.Column(db.DateTime, nullable = True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable = False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable = False)
    presentacion_id = db.Column(db.Integer, db.ForeignKey('presentacioninsumo.id'), nullable = False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable = False)