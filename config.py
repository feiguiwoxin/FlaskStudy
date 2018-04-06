import os

class myconfig():
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:mysql@localhost/study'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'study'
    DEBUG = True
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")