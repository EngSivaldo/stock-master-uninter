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

    # --- IMPORTAÇÕES DE BLUEPRINTS ---
    from app.blueprints.auth import auth_bp 
    from app.blueprints.inventory.routes import inventory_bp
    from app.blueprints.main.routes import main_bp 

    # --- REGISTRO DOS BLUEPRINTS ---
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(inventory_bp) 
    app.register_blueprint(main_bp, url_prefix='/reports')

    # --- REGISTRO DE COMANDOS CLI (PROFISSIONAL) ---
    # Importamos aqui para evitar imports circulares
    from app.commands import register_commands
    register_commands(app)
    
    return app