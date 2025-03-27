<<<<<<< Updated upstream
import os 
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY='IDGS803'
    SESION_COOKIE_SECURE=False

class DevelopmentConfig(Config):
        DEBUG=True
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:270901@127.0.0.1:3306/cookiemania'
        SQLALCHEMY_TRACK_MODIFICATIONS=False
=======
import os
import urllib
from flask_mail import Mail

# Instancia de Flask-Mail
mail = Mail()

class Config(object):
    SECRET_KEY = 'CookiemaniaSecret'
    SESSION_COOKIE_SECURE = False

    # Configuracion  Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'luisrosasbocanegra@gmail.com'
    MAIL_PASSWORD = 'mzoj owgd eqvm zgai'

    MAIL_DEFAULT_SENDER = ('Galletamaniaco', 'luisrosasbocanegra@gmail.com')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:270901@127.0.0.1/cookiemania'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
>>>>>>> Stashed changes
