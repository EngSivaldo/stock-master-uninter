from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='operator') 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Dados Principais
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), unique=True)
    
    # Contato
    contact_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    # Endereço
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    
    products = db.relationship('Product', backref='supplier', lazy=True)

# CLASSE CATEGORIA (Movida para cima para evitar erro de referência, se necessário)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relacionamento
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    min_level = db.Column(db.Integer, default=5)
    cost = db.Column(db.Float, default=0.0)
    price = db.Column(db.Float, default=0.0)
    
    # --- CORREÇÃO AQUI (Sem a vírgula no final) ---
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    # ----------------------------------------------
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    movements = db.relationship('Movement', backref='product', lazy=True)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False) 
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    user = db.relationship('User', backref='movements')