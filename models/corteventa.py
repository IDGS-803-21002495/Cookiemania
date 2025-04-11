from datetime import datetime
from models import db

class CorteVenta(db.Model):
    __tablename__ = 'corteventa'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID único del corte
    total_ventas = db.Column(db.Numeric(12, 2), nullable=False)  # Total de ventas
    total_egresos = db.Column(db.Numeric(12, 2), nullable=False)  # Total de egresos
    total_mermas_insumos = db.Column(db.Numeric(12, 2), nullable=False)  # Total de mermas de insumos
    total_mermas_productos = db.Column(db.Numeric(12, 2), nullable=False)  # Total de mermas de productos
    total_neto = db.Column(db.Numeric(12, 2), nullable=False)  # Total neto (después de egresos y mermas)
    monto_inicial = db.Column(db.Numeric(12, 2), nullable=False)  # Monto inicial en caja
    total_caja = db.Column(db.Numeric(12, 2), nullable=False)  # Total real en caja
    diferencia = db.Column(db.Numeric(12, 2), nullable=False)  # Total real en caja
    fecha_corte = db.Column(db.DateTime, default=datetime.now, nullable=False)  # Fecha y hora del corte
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)

    def __repr__(self):
        return f"<CorteVenta {self.id}, Fecha: {self.fecha_corte}>"
