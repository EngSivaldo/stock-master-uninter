import os
from dotenv import load_dotenv

# 1. Pega o caminho da pasta onde o config.py está (a raiz)
basedir = os.path.abspath(os.path.dirname(__file__))

# Carrega o .env (apenas para uso local)
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Segurança
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gerenciamento de Arquivos
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16MB
    
    # --- AJUSTE SÊNIOR PARA O RENDER ---
    # Capturamos a URL do ambiente
    _db_url = os.environ.get('DATABASE_URL')
    
    # Se a URL existir e começar com 'postgres://', corrigimos para 'postgresql://'
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    
    # Define a URI final (Nuvem ou SQLite local)
    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///' + os.path.join(basedir, 'stock.db')