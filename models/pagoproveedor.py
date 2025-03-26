from models import db

# Tabla de pago a proveedor
class PagoProveedor(db.Model):
    __tablename__ = 'pagoproveedor'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha = db.Column(db.DateTime, nullable = False)
    monto = db.Column(db.Numeric(10,2), nullable = False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable = False)
    lote_insumo_id = db.Column(db.Integer, db.ForeignKey('loteinsumo.id'), nullable = False)