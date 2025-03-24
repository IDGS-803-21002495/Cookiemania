import os 
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = 'CookiemaniaSecret'
    SESION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@127.0.0.1/cookiemania'
    SQLALCHEMY_TRACK_MODIFICATIONS = False