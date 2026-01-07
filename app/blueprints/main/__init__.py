from flask import Blueprint

# 1. Criamos o Blueprint 'main'
main_bp = Blueprint('main', __name__)

# 2. Importamos as rotas para registrá-las no Blueprint
# Isso precisa ser AQUI em baixo para evitar erro circular
from . import routes