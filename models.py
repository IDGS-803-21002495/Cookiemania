from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # se sugiere almacenar encriptado
    email = db.Column(db.String(100), unique=True, nullable=False)
    rol = db.Column(
        db.Enum('ADMIN', 'VENDEDOR', 'CLIENTE', name='rol_enum'),
        nullable=False
    )
    estado = db.Column(
        db.Enum('ACTIVO', 'INACTIVO', name='usuario_estado_enum'),
        default='ACTIVO',
        nullable=False
    )
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    ultimo_inicio_sesion = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Usuario {self.username}>'


class Insumo(db.Model):
    __tablename__ = 'Insumo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    unidad_medida = db.Column(db.String(50), nullable=False)


class Proveedor(db.Model):
    __tablename__ = 'Proveedor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    numero_telefonico = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    estado = db.Column(
        db.Enum('ACTIVO', 'INACTIVO', name='proveedor_estado_enum'),
        default='ACTIVO',
        nullable=False
    )


class Compra(db.Model):
    __tablename__ = 'Compra'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_compra = db.Column(db.Date, nullable=False, default=datetime.now)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('Usuario.id'),
        nullable=True
    )
    # Relación opcional si quieres acceder desde la entidad Usuario
    # usuario = db.relationship('Usuario', backref='compras')


class PresentacionInsumo(db.Model):
    __tablename__ = 'PresentacionInsumo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('Insumo.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad_base = db.Column(db.Numeric(10,2), nullable=False)
    unidad_base = db.Column(
        db.Enum('GRAMOS', 'MILILITROS', 'UNIDADES', name='unidad_base_enum')
    )
    # Relación opcional
    # insumo = db.relationship('Insumo', backref='presentaciones')


class LoteInsumo(db.Model):
    __tablename__ = 'LoteInsumo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('Compra.id'), nullable=False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('Insumo.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('Proveedor.id'), nullable=False)
    presentacion_id = db.Column(db.Integer, db.ForeignKey('PresentacionInsumo.id'), nullable=False)
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)
    cantidad = db.Column(db.Numeric(10,2), nullable=False)
    cantidad_disponible = db.Column(db.Numeric(10,2), nullable=False)
    fecha_caducidad = db.Column(db.Date, nullable=False)

    # Relación opcional con las tablas referenciadas
    # compra = db.relationship('Compra', backref='lotes_insumo')
    # insumo = db.relationship('Insumo', backref='lotes_insumo')
    # proveedor = db.relationship('Proveedor', backref='lotes_insumo')
    # presentacion = db.relationship('PresentacionInsumo', backref='lotes_insumo')


class Galleta(db.Model):
    __tablename__ = 'Galleta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    estado_disponibilidad = db.Column(
        db.Enum('SUFICIENTE', 'POR_TERMINAR', 'BAJO_INVENTARIO', name='estado_disponibilidad_enum'),
        nullable=False
    )


class Receta(db.Model):
    __tablename__ = 'Receta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    galleta_id = db.Column(db.Integer, db.ForeignKey('Galleta.id'), nullable=False)
    cantidad_lote = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)  # LONGTEXT en MySQL puede ser db.Text en SQLAlchemy

    # Relación opcional
    # galleta = db.relationship('Galleta', backref='recetas')


class DetalleReceta(db.Model):
    __tablename__ = 'DetalleReceta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('Receta.id'), nullable=False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('Insumo.id'), nullable=False)
    cantidad_insumo = db.Column(db.Numeric(10,2), nullable=False)


class LoteProduccion(db.Model):
    __tablename__ = 'LoteProduccion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('Receta.id'), nullable=False)
    fecha_produccion = db.Column(db.Date, nullable=False, default=datetime.now)
    fecha_caducidad = db.Column(db.Date, nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)
    estado = db.Column(
        db.Enum('SOLICITADO', 'MEZCLANDO','HORNEANDO','ENFRIADO', 'TERMINADO', 'CANCELADO', name='estado_produccion_enum')
    )
    # receta = db.relationship('Receta', backref='lotes_produccion')


class ProduccionInsumo(db.Model):
    __tablename__ = 'ProduccionInsumo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lote_produccion_id = db.Column(db.Integer, db.ForeignKey('LoteProduccion.id'), nullable=False)
    lote_insumo_id = db.Column(db.Integer, db.ForeignKey('LoteInsumo.id'), nullable=False)
    cantidad_usada = db.Column(db.Numeric(10,2), nullable=False)


class Venta(db.Model):
    __tablename__ = 'Venta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_registro = db.Column(db.Date, nullable=False, default=datetime.now)
    fecha_entrega = db.Column(db.Date)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    estado = db.Column(
        db.Enum('PENDIENTE', 'PRODUCCION', 'ENTREGADO', 'CANCELADO', name='venta_estado_enum'),
        default='PENDIENTE',
        nullable=False
    )


class DetalleVenta(db.Model):
    __tablename__ = 'DetalleVenta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('Venta.id'), nullable=False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('Galleta.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10,2))
    tipo_venta = db.Column(
        db.Enum('UNIDAD', 'GRAMAJE', 'PAQUETE', 'DINERO', name='tipo_venta_enum'),
        nullable=False
    )


class MermaInsumo(db.Model):
    __tablename__ = 'MermaInsumo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('Insumo.id'), nullable=False)
    cantidad_merma = db.Column(db.Numeric(10,2), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.now)
    tipo = db.Column(
        db.Enum('INSUMO_CADUCO', 'INSUMO_DESPERDICIADO', name='tipo_merma_insumo_enum')
    )


class MermaProducto(db.Model):
    __tablename__ = 'MermaProducto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lote_produccion_id = db.Column(db.Integer, db.ForeignKey('LoteProduccion.id'), nullable=False)
    cantidad_merma = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.now)
    tipo = db.Column(
        db.Enum('PRODUCTO_DANADO','PRODUCTO_CADUCO', name='tipo_merma_producto_enum')
    )


class PagoProveedor(db.Model):
    __tablename__ = 'PagoProveedor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('Proveedor.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.now)
    monto = db.Column(db.Numeric(10,2), nullable=False)
    lote_insumo_id = db.Column(db.Integer, db.ForeignKey('LoteInsumo.id'), nullable=False)
