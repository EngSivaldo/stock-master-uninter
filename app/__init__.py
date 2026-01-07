from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar Extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Registrar Blueprints (Vamos criar os arquivos em breve)
    # Importamos aqui dentro para evitar "Circular Import"
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.inventory.routes import inventory_bp
    # from app.blueprints.main.routes import main_bp (Futuro)
    # from app.blueprints.admin.routes import admin_bp (Futuro)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(inventory_bp) # Sem prefixo ou '/inventory'
    
    return app