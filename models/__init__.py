from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.compra import Compra
from models.detallereceta import DetalleReceta
from models.detalleventa import DetalleVenta
from models.galleta import Galleta
from models.insumo import Insumo
from models.presentacioninsumo import PresentacionInsumo
from models.loteinsumo import LoteInsumo
from models.loteproduccion import LoteProduccion
from models.mermainsumo import MermaInsumo
from models.mermaproducto import MermaProducto
from models.pagoproveedor import PagoProveedor
from models.produccioninsumo import ProduccionInsumo
from models.proveedor import Proveedor
from models.receta import Receta
from models.usuario import Usuario
from models.venta import Venta
from models.corteventa import CorteVenta
