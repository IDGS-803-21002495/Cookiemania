from . import pedidos_bp

@pedidos_bp.route('/')
def pedidos():
    return 'Módulo de pedidos'