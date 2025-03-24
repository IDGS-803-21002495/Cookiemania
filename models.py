from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import datetime

db = SQLAlchemy()

# Definir ENUM para el rol del usuario 
class UserRole(Enum):
    ADMIN = 'ADMIN'
    VENDEDOR = 'VENDEDOR'
    PRODUCCION = 'PRODUCCION'
    CLIENTE = 'CLIENTE'

# Definir ENUM para el estado del usuario
class UserStatus(Enum):
    ACTIVO = 'ACTIVO'
    INACTIVO = 'INACTIVO'

# Definir ENUM para la unidad base de un insumo 
class UnidadBase(Enum):
    GRAMOS = 'GRAMOS'
    MILILITROS = 'MILILITROS'
    UNIDADES = 'UNIDADES'

# Definir ENUM para el estado de disponibilidad de una galleta
class EstadoDisponibilidad(Enum):
    SUFICIENTE = 'SUFICIENTE'
    POR_TERMINAR = 'POR_TERMINAR'
    BAJO_INVENTARIO = 'BAJO_INVENTARIO'

# Definir ENUM para el estado en que se encuentra un lote de galletas
class EstadoLote(Enum):
    SOLICITADO = 'SOLICITADO'
    MEZCLANDO = 'MEZCLANDO'
    HORNEANDO = 'HORNEANDO'
    ENFRIANDO = 'ENFRIANDO'
    TERMINADO = 'TERMINADO'
    CANCELADO = 'CANCELADO'

# Definir ENUM para el estado en que se encuentra una venta 
class EstadoVenta(Enum):
    PENDIENTE = 'PENDIENTE'
    PRODUCCION = 'PRODUCCION'
    ENTREGADO = 'ENTREGADO'
    CANCELADO = 'CANCELADO'

# Definir ENUM para el tipo de venta 
class TipoVenta(Enum):
    UNIDAD = 'UNIDAD'
    GRAMAJE = 'GRAMAJE'
    PAQUETE = 'PAQUETE'

# Definir ENUM para el tipo de merma que se registra
class TipoMerma(Enum):
    CADUCIDAD = 'CADUCIDAD'
    DESPERDICIO = 'DESPERDICIO'

# Tabla de Usuarios 
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    rol = db.Column(db.Enum(UserRole.ADMIN, UserRole.VENDEDOR, UserRole.PRODUCCION, UserRole.CLIENTE), nullable=False)
    estado = db.Column(db.Enum(UserStatus.ACTIVO, UserStatus.INACTIVO), nullable=False, default=UserStatus.ACTIVO)
    fecha_registro = db.Column(db.DateTime, default = datetime.datetime.now, nullable = False)
    ultimo_inicio_sesion = db.Column(db.DateTime)

# Tabla de Insumo 
class Insumo(db.Model):
    __tablename__ = 'insumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(255), nullable = False)
    unidad_medida = db.Column(db.String(50), nullable = False)

# Tabla de proveedor
class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(255), nullable = False)
    numero_telefonico = db.Column(db.String(20), nullable = False)
    correo = db.Column(db.String(100), nullable = False)
    direccion = db.Column(db.String(255), nullable = False)
    fecha_registro = db.Column(db.DateTime, default = datetime.datetime.now, nullable = False)
    estado = db.Column(db.Enum(UserStatus.ACTIVO, UserStatus.INACTIVO), nullable=False, default=UserStatus.ACTIVO)

# Tabla de compra
class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha_compra = db.Column(db.DateTime, nullable = False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)

# Tabla de presentación de insumo
# Define las diferentes presentaciones que podria tener un insumo y su conversión a unidad base
class PresentacionInsumo(db.Model):
    __tablename__ = 'presentacioninsumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(100), nullable = False)
    cantidad_base = db.Column(db.Numeric(10,2), nullable = False)
    unidad_base = db.Column(db.Enum(UnidadBase.MILILITROS, UnidadBase.GRAMOS, UnidadBase.UNIDADES))  
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable = False)

# Tabla de lote de insumo 
class LoteInsumo(db.Model):
    __tablename__ = 'loteinsumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    precio_unitario = db.Column(db.Numeric(10,2), nullable = False)
    cantidad = db.Column(db.Numeric(10,2), nullable = False)
    cantidad_disponible = db.Column(db.Numeric(10,2), nullable = False)
    fecha_caducidad = db.Column(db.DateTime, nullable = False)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable = False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable = False)
    presentacion_id = db.Column(db.Integer, db.ForeignKey('presentacioninsumo.id'), nullable = False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable = False)

# Tabla de galleta
class Galleta(db.Model):
    __tablename__ = 'galleta'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(255), nullable = False)
    peso = db.Column(db.Float, nullable = False)
    precio = db.Column(db.Numeric(10,2), nullable = False)
    descripcion = db.Column(db.String(255), nullable = False)
    estado_disponibilidad = db.Column(db.Enum(EstadoDisponibilidad.SUFICIENTE, EstadoDisponibilidad.POR_TERMINAR, EstadoDisponibilidad.BAJO_INVENTARIO), nullable=False)

# Tabla de receta
class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_lote = db.Column(db.Integer, nullable = False)
    descripcion = db.Column(db.Text, nullable = False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galleta.id'), nullable = False)

# Tabla de detalle receta
class DetalleReceta(db.Model):
    __tablename__ = 'detallereceta'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_insumo = db.Column(db.Numeric(10,2), nullable = False)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable = False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable = False)

# Tabla de lote de producción 
class LoteProduccion(db.Model):
    __tablename__ = 'loteproduccion'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha_produccion = db.Column(db.DateTime, nullable = False)
    fecha_caducidad = db.Column(db.DateTime, nullable = False)
    cantidad_disponible = db.Column(db.Integer, nullable = False)
    estado_lote = db.Column(db.Enum(EstadoLote.SOLICITADO, EstadoLote.MEZCLANDO, EstadoLote.HORNEANDO, EstadoLote.ENFRIANDO, EstadoLote.TERMINADO, EstadoLote.CANCELADO), nullable=False)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable = False)

# Tabla de producción insumo 
class ProduccionInsumo(db.Model):
    __tablename__ = 'produccioninsumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_usada = db.Column(db.Numeric(10,2), nullable = False)
    lote_produccion_id = db.Column(db.Integer, db.ForeignKey('loteproduccion.id'), nullable = False)
    lote_insumo_id = db.Column(db.Integer, db.ForeignKey('loteinsumo.id'), nullable = False)

# Tabla de venta 
class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha_registro = db.Column(db.DateTime, nullable = False)
    fecha_entrega = db.Column(db.DateTime, nullable = False)
    estado = db.Column(db.Enum(EstadoVenta.PENDIENTE, EstadoVenta.CANCELADO, EstadoVenta.PRODUCCION, EstadoVenta.ENTREGADO), default = EstadoVenta.PENDIENTE)  # Se cambió 'name' por 'EstadoVenta'
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = True)

# Tabla de detalle de venta 
class DetalleVenta(db.Model):
    __tablename__ = 'detalleventa'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad = db.Column(db.Integer, nullable = False)
    precio_unitario = db.Column(db.Numeric(10,2), nullable = False)
    tipo_venta = db.Column(db.Enum(TipoVenta.GRAMAJE, TipoVenta.UNIDAD, TipoVenta.PAQUETE), nullable = False)  # Se cambió 'name' por 'TipoVenta'
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable = False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galleta.id'), nullable = False)

# Tabla de merma de insumo 
class MermaInsumo(db.Model):
    __tablename__ = 'mermainsumo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_merma = db.Column(db.Numeric(10,2), nullable = False)
    fecha = db.Column(db.DateTime, nullable = False)
    tipo = db.Column(db.Enum(TipoMerma.CADUCIDAD, TipoMerma.DESPERDICIO), nullable = False)  # Se cambió 'name' por 'TipoMerma'
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable = False)

# Tabla de merma de productos 
class Mermaproducto(db.Model):
    __tablename__ = 'mermaproducto'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cantidad_merma = db.Column(db.Integer, nullable = False)
    fecha = db.Column(db.DateTime, nullable = False)
    tipo = db.Column(db.Enum(TipoMerma.CADUCIDAD, TipoMerma.DESPERDICIO), nullable = False)  # Se cambió 'name' por 'TipoMerma'
    lote_produccion_id = db.Column(db.Integer, db.ForeignKey('loteproduccion.id'), nullable = False)

# Tabla de pago a proveedor
class PagoProveedor(db.Model):
    __tablename__ = 'pagoproveedor'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha = db.Column(db.DateTime, nullable = False)
    monto = db.Column(db.Numeric(10,2), nullable = False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable = False)
    lote_insumo_id = db.Column(db.Integer, db.ForeignKey('loteinsumo.id'), nullable = False)
