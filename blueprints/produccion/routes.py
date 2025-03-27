from .import produccion_bp

@produccion_bp.route('/')
def produccion():
    return 'Módulo de producción'