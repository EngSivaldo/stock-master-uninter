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
    # ... (seus campos existentes)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), unique=True)
    contact_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    
    # --- NOVO CAMPO PARA A IMAGEM ---
    logo = db.Column(db.String(150), nullable=True) 
    # --------------------------------

    products = db.relationship('Product', backref='supplier', lazy=True)
    orders = db.relationship('PurchaseOrder', backref='supplier', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
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
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    image_file = db.Column(db.String(100), nullable=True, default='default.jpg')
    active = db.Column(db.Boolean, default=True, server_default="1", nullable=False)
    
    movements = db.relationship('Movement', backref='product', lazy=True)
    # Relacionamento com Itens de Pedido (Novo)
    order_items = db.relationship('PurchaseOrderItem', backref='product', lazy=True)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False) 
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    user = db.relationship('User', backref='movements')


# --- NOVAS TABELAS PARA CONFERÊNCIA DE RECEBIMENTO ---

class PurchaseOrder(db.Model):
    """
    Representa o Cabeçalho da Nota Fiscal ou Pedido.
    Ex: NF 1234 da Ambev, status 'Pendente'.
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # Identificação
    invoice_number = db.Column(db.String(50)) # Número da Nota Fiscal
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    # Status do Processo
    # 'pending' = Criado pelo Admin, aguardando caminhão.
    # 'completed' = Conferido pelo funcionário e estoque atualizado.
    status = db.Column(db.String(20), default='pending', nullable=False)
    
    # Datas e Responsáveis
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    
    # Quem criou (Admin)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Itens deste pedido
    items = db.relationship('PurchaseOrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

class PurchaseOrderItem(db.Model):
    """
    Representa cada linha do pedido.
    Ex: Skol Lata - Esperado: 500 - Recebido: 500
    """
    id = db.Column(db.Integer, primary_key=True)
    
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    # O Pulo do Gato da Conferência:
    quantity_expected = db.Column(db.Integer, nullable=False) # Quanto o Admin digitou (Nota Fiscal)
    quantity_received = db.Column(db.Integer, default=0)      # Quanto o funcionário contou no caminhão
    
    # Custo unitário nesta nota específica (pode variar da tabela de produtos)
    unit_cost = db.Column(db.Float, default=0.0)