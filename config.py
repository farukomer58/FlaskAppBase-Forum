import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')           # Configure Flask App SecretKey
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'       # Configure Flask App database connect url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configs for MAIL SERVER
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')     #Toegang door minder goed beveiligde apps - SHOULD BE ON