from . import inventario_bp

@inventario_bp.route('/')
def inventario():
    return 'Módulo de inventario'