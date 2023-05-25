import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'kiwi.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class DevelopmentConfig(Config):
    ENV = 'development'

class ProducationConfig(Config):
    ENV = "production"
    DEBUG = False