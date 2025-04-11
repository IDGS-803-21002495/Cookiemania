import os 
from sqlalchemy import create_engine
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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@127.0.0.1/cookiemania'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
