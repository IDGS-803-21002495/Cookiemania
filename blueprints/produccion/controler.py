from datetime import datetime, timedelta
from models.loteproduccion import LoteProduccion
from models.loteinsumo import LoteInsumo
from models.receta import Receta
from models.galleta import Galleta
from models.detallereceta import DetalleReceta
from models.produccioninsumo import ProduccionInsumo
from models.insumo import Insumo
from models.enums import EstadoLote
from models.mermaproducto import MermaProducto

from models import db
from sqlalchemy import func, case
from flask import flash
from sqlalchemy.orm import aliased


# Función para consultar la cantidad de galletas (Inventario)
def getGalleta():
    galletas = (db.session.query(
        Galleta.id,
        Galleta.nombre,
        func.coalesce(func.sum(LoteProduccion.cantidad_disponible),
                      0).label("cantidad_total"),
        func.group_concat(LoteProduccion.estado_lote).label(
            "estatus_lotes")  # Concatenar estados
    )
        .outerjoin(Receta, Receta.galleta_id == Galleta.id)
        .outerjoin(LoteProduccion, LoteProduccion.receta_id == Receta.id)
        .group_by(Galleta.id, Galleta.nombre)
        .all())

    return galletas

# funcion para consultar la fecha de produccion y caducidad


def getFechaCaducidas():
    # consulta la produccion de galletas que este a dos dias de su fecha de caducidad
    fecha_actual = datetime.now().date()
    fecha_limite = fecha_actual + timedelta(days=2)

    lotes_caducando = (db.session.query(
        Galleta.id,
        Galleta.nombre,
        LoteProduccion.id.label("lote_id"),
        LoteProduccion.cantidad_disponible,
        func.min(LoteProduccion.fecha_caducidad).label(
            "fecha_caducidad_proxima"),
        func.sum(LoteProduccion.cantidad_disponible).label("cantidad_total")
    )
        .join(Receta, Receta.id == LoteProduccion.receta_id)
        .join(Galleta, Galleta.id == Receta.galleta_id)
        .filter(LoteProduccion.fecha_caducidad <= fecha_limite)
        .group_by(Galleta.id, Galleta.nombre, LoteProduccion.id, LoteProduccion.cantidad_disponible)
        .all())

    return lotes_caducando

#  Función para procesar la producción de galletas


def procesarproduccion(id):
    # Consulta para traer los ingredientes de la receta
    productosReceta = (db.session.query(
        DetalleReceta.cantidad_insumo,
        Insumo.nombre,
        Insumo.id.label("insumo_id"),
        Receta.cantidad_lote,
    )
        .join(Receta, Receta.id == DetalleReceta.receta_id)
        .join(Insumo, Insumo.id == DetalleReceta.insumo_id)
        .filter(Receta.id == id)
        .all())

    if not productosReceta:
        return {"mensaje": "No se encontraron ingredientes para la receta"}

    # Insertar el nuevo lote de producción
    fecha_produccion = datetime.now()
    fecha_caducidad = fecha_produccion + timedelta(days=15)

    try:
        nuevo_lote = LoteProduccion(
            fecha_produccion=fecha_produccion,
            fecha_caducidad=fecha_caducidad,
            cantidad_disponible=productosReceta[0].cantidad_lote,
            estado_lote="SOLICITADO",
            receta_id=id
        )

        db.session.add(nuevo_lote)
        db.session.commit()

        return {"mensaje": "Lote de producción registrado correctamente (estado: SOLICITADO)"}

    except Exception as e:
        db.session.rollback()
        return {"mensaje": f"Error al registrar el lote: {str(e)}"}


def actualizar_estado_lote(lote_id):
    try:
        # Obtener el lote de producción
        lote = db.session.query(LoteProduccion).filter_by(id=lote_id).first()

        if not lote:
            return {"success": False, "mensaje": "Lote no encontrado"}

        # Definir el orden de los estados
        orden_estados = [
            EstadoLote.SOLICITADO,
            EstadoLote.MEZCLANDO,
            EstadoLote.HORNEANDO,
            EstadoLote.ENFRIANDO,
            EstadoLote.TERMINADO
        ]

        # Encontrar el índice del estado actual
        try:
            indice_actual = orden_estados.index(lote.estado_lote)
        except ValueError:
            return {"success": False, "mensaje": "Estado actual no válido"}

        # Determinar el siguiente estado
        if indice_actual + 1 < len(orden_estados):
            nuevo_estado = orden_estados[indice_actual + 1]
        else:
            return {"success": False, "mensaje": "El lote ya está en su estado final"}

        # Solo consumir insumos cuando cambiamos de SOLICITADO a MEZCLANDO
        if lote.estado_lote == EstadoLote.SOLICITADO and nuevo_estado == EstadoLote.MEZCLANDO:
            # Obtener los ingredientes de la receta
            productosReceta = (db.session.query(
                DetalleReceta.cantidad_insumo,
                Insumo.nombre,
                Insumo.id.label("insumo_id")
            )
                .join(Receta, Receta.id == DetalleReceta.receta_id)
                .join(Insumo, Insumo.id == DetalleReceta.insumo_id)
                .filter(Receta.id == lote.receta_id)
                .all())

            for producto in productosReceta:
                cantidad_requerida = producto.cantidad_insumo
                lotes_insumo = db.session.query(LoteInsumo).filter(
                    LoteInsumo.insumo_id == producto.insumo_id,
                    LoteInsumo.cantidad_disponible > 0
                ).order_by(LoteInsumo.fecha_caducidad.asc()).all()

                if not lotes_insumo:
                    db.session.rollback()
                    return {"success": False, "mensaje": f"No hay suficiente stock del insumo {producto.nombre}"}

                for lote_insumo in lotes_insumo:
                    if cantidad_requerida <= 0:
                        break

                    cantidad_a_usar = min(
                        cantidad_requerida, lote_insumo.cantidad_disponible)
                    lote_insumo.cantidad_disponible -= cantidad_a_usar
                    cantidad_requerida -= cantidad_a_usar

                    # Registrar en ProduccionInsumo
                    registro_insumo = ProduccionInsumo(
                        cantidad_usada=cantidad_a_usar,
                        lote_produccion_id=lote.id,
                        lote_insumo_id=lote_insumo.id
                    )
                    db.session.add(registro_insumo)

                if cantidad_requerida > 0:
                    db.session.rollback()
                    return {"success": False, "mensaje": f"No hay suficiente stock del insumo {producto.nombre}"}

        # Actualizar el estado
        lote.estado_lote = nuevo_estado
        db.session.commit()

        return {
            "success": True,
            "mensaje": f"Estado actualizado a {nuevo_estado.value}",
            "nuevo_estado": nuevo_estado.value
        }

    except Exception as e:
        db.session.rollback()
       # return {"success": False, "mensaje": f"Error al actualizar el estado: {str(e)}"}

# muetra los lotes con su estatus


def estatusGalleta():
    galletas = (db.session.query(

        Galleta.nombre,
        LoteProduccion.cantidad_disponible,
        LoteProduccion.id,
        func.sum(LoteProduccion.cantidad_disponible).label("cantidad_total"),
        LoteProduccion.estado_lote.label("estado_lote")  # Añadir esta línea
    )
        .outerjoin(Receta, Receta.galleta_id == Galleta.id)
        .outerjoin(LoteProduccion, LoteProduccion.receta_id == Receta.id)
        .filter(LoteProduccion.estado_lote != 'TERMINADO')
        # Añadir estado_lote al group_by
        .group_by(Galleta.nombre, LoteProduccion.estado_lote, LoteProduccion.cantidad_disponible, LoteProduccion.id)
        .all())

    return galletas


def actualizarEstatus(lote_id, nuevo_estatus):
    try:
        # Obtener el lote
        lote = db.session.query(LoteProduccion).filter_by(id=lote_id).first()

        if not lote:
            flash("Lote no encontrado", "danger")
            return False

        # Verificar si el cambio es de SOLICITADO a MEZCLANDO
        if lote.estado_lote == EstadoLote.SOLICITADO and nuevo_estatus == EstadoLote.MEZCLANDO:
            # Aquí va la lógica para consumir insumos
            productosReceta = (db.session.query(
                DetalleReceta.cantidad_insumo,
                Insumo.nombre,
                Insumo.id.label("insumo_id")
            )
                .join(Receta, Receta.id == DetalleReceta.receta_id)
                .join(Insumo, Insumo.id == DetalleReceta.insumo_id)
                .filter(Receta.id == lote.receta_id)
                .all())

            for producto in productosReceta:
                cantidad_requerida = producto.cantidad_insumo
                lotes_insumo = db.session.query(LoteInsumo).filter(
                    LoteInsumo.insumo_id == producto.insumo_id,
                    LoteInsumo.cantidad_disponible > 0
                ).order_by(LoteInsumo.fecha_caducidad.asc()).all()

                if not lotes_insumo:
                    db.session.rollback()
                    flash(
                        f"No hay suficiente stock del insumo {producto.nombre}", "danger")
                    return False

                for lote_insumo in lotes_insumo:
                    if cantidad_requerida <= 0:
                        break

                    cantidad_a_usar = min(
                        cantidad_requerida, lote_insumo.cantidad_disponible)
                    lote_insumo.cantidad_disponible -= cantidad_a_usar
                    cantidad_requerida -= cantidad_a_usar

                    registro_insumo = ProduccionInsumo(
                        cantidad_usada=cantidad_a_usar,
                        lote_produccion_id=lote.id,
                        lote_insumo_id=lote_insumo.id
                    )
                    db.session.add(registro_insumo)

                if cantidad_requerida > 0:
                    db.session.rollback()
                    flash(
                        f"No hay suficiente stock del insumo {producto.nombre}", "danger")
                    return False

        # Actualizar el estado
        lote.estado_lote = nuevo_estatus
        db.session.commit()

        flash(f"Estado actualizado a {nuevo_estatus.value}", "success")
        return True

    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar el estatus del lote: {str(e)}", "danger")
        return False

# funcion para traer los lotes y poder registrar merma


def getlotes():
    lotes = (db.session.query(
        LoteProduccion.id,
        Galleta.nombre.label('nombre_galleta'),
        LoteProduccion.cantidad_disponible,
        LoteProduccion.fecha_caducidad.label(
            'fecha_caducidad')
    ).join(Receta, Receta.id == LoteProduccion.receta_id
           ).join(Galleta, Galleta.id == Receta.galleta_id
                  ).filter(
        LoteProduccion.cantidad_disponible > 0,
        LoteProduccion.estado_lote == 'TERMINADO'
    ).order_by(
        Galleta.nombre,
        LoteProduccion.fecha_caducidad
    ).all())
    return lotes


def registromerma(id, cantidad, motivo):

    try:
        # 1. Obtener el lote (ya validado que existe por el formulario)
        lote = LoteProduccion.query.get(id)

        # 2. Verificar stock disponible (validación adicional)
        if cantidad > lote.cantidad_disponible:
            return False, f"No hay suficiente stock. Disponible: {lote.cantidad_disponible}"

        # 3. Registrar la merma
        nueva_merma = MermaProducto(
            cantidad_merma=cantidad,
            fecha=datetime.now(),
            tipo=motivo,
            lote_produccion_id=id
        )

        # 4. Actualizar stock del lote
        lote.cantidad_disponible -= cantidad

        # 5. Guardar en base de datos
        db.session.add(nueva_merma)
        db.session.commit()

        return True, "Merma registrada correctamente"

    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar merma: {str(e)}")
        return False, f"Error al registrar merma: {str(e)}"
