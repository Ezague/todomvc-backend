import os

class Config(object):
    JWT_SECRET_KEY="secret"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DB_HOST=os.environ.get('DB_HOST')
    DB_USER=os.environ.get('DB_USER')
    DB_PASSWORD=os.environ.get('DB_PASSWORD')
    DB_NAME=os.environ.get('DB_NAME')
    DB_PORT=os.environ.get('DB_PORT')
    SQLALCHEMY_DATABASE_URI=f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'