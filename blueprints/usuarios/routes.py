from . import usuarios_bp

@usuarios_bp.route('/')
def usuarios():
    return 'Módulo de usuarios'