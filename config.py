import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///journal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
