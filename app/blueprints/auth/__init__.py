from flask import Blueprint

# 1. Definimos o Blueprint aqui
auth_bp = Blueprint('auth', __name__)

# 2. Importamos as rotas AQUI, logo abaixo da definição.
# Isso evita o "Erro Circular" e garante que o Flask leia as rotas.
from . import routes