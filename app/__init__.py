from flask import Flask
from app.extensions import db, migrate, login_manager
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar Extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # --- IMPORTAÇÕES ---
    # Auth: Importa do pacote (Recomendado)
    from app.blueprints.auth import auth_bp 
    
    # Inventory: Pode manter assim se funcionar, ou mudar para 'from app.blueprints.inventory import inventory_bp'
    from app.blueprints.inventory.routes import inventory_bp
    
    # Main: Importa do pacote (ajuste se você mudou o __init__ do main)
    # Se der erro aqui, tente: from app.blueprints.main import main_bp
    from app.blueprints.main.routes import main_bp 
    # -------------------

    # --- REGISTRO DOS BLUEPRINTS ---
    
    # 1. Auth: Tudo começa com /auth (ex: /auth/login)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # 2. Inventory: É o nosso "Dono da Casa". Ele fica na raiz (/)
    # Por isso o Dashboard abre quando entra no site.
    app.register_blueprint(inventory_bp) 
    
    # 3. Main (Relatórios): PRECISA DE UM PREFIXO! <--- O PULO DO GATO 😺
    # Antes estava sem nada, por isso conflitava com o Inventory.
    # Agora, as rotas dele serão /reports/
    app.register_blueprint(main_bp, url_prefix='/reports')
    
    return app