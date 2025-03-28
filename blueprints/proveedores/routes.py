from . import proveedores_bp

@proveedores_bp.route('/')
def proveedores():
    return 'Módulo de proveedores'