from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def require_role(required_roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para acceder a esta página", "warning")
                return redirect(url_for('auth.login'))

            if current_user.rol not in required_roles:
                flash("No tienes permisos para acceder a esta página", "danger")
                return redirect(url_for('auth.login'))  

            return f(*args, **kwargs)
        return wrapped
    return decorator
