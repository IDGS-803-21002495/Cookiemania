from . import compras_bp

@compras_bp.route('/')  
def compras():
    return 'Módulo de compras'
