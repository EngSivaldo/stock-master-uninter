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

    # --- CORREÇÃO DE IMPORTAÇÃO (Padrão Sênior) ---
    # Importamos do pacote (pasta), pois os __init__.py lá dentro já expõem o blueprint
    
    # Auth: Importa da pasta auth (graças ao fix que fizemos antes)
    from app.blueprints.auth import auth_bp 
    
    # Inventory: Importa do routes (supondo que inventory ainda usa o método antigo)
    from app.blueprints.inventory.routes import inventory_bp
    
    # Main: Importa do routes
    from app.blueprints.main.routes import main_bp 
    # -----------------------------------------------

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(inventory_bp) 
    app.register_blueprint(main_bp)
    
    return app