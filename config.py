import os
from dotenv import load_dotenv

# 1. Pega o caminho da pasta onde o config.py está (a raiz)
basedir = os.path.abspath(os.path.dirname(__file__))

# Carrega o .env
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ONDE VAMOS SALVAR AS FOTOS:
    # Cria o caminho: app/static/uploads
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Limite de 16MB por arquivo
    
    # 2. O SEGREDO ESTÁ AQUI:
    # Ao usar os.path.join(basedir, 'stock.db'), forçamos o arquivo a ficar na raiz.
    # Se usássemos apenas 'sqlite:///stock.db', ele jogaria para a pasta instance.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'stock.db')