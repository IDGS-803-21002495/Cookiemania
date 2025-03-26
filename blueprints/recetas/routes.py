from . import recetas_bp

@recetas_bp.route('/')
def recetas():
    return 'Módulo de recetas'