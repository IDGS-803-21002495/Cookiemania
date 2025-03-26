from sqlalchemy import Enum

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