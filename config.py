import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #MAIL_SERVER = 'smtp.gmail.com'
    #MAIL_PORT = 465
    #MAIL_USE_TLS = False
    #MAIL_USE_SSL = True
    #MAIL_USERNAME = os.environ.get('MAIL_USER')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USER')
    SECRET_KEY = os.environ.get('SECRET_KEY')
