import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'emmanuelibok-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///emmanuelibok_shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False