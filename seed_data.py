from app import create_app
from app.extensions import db
from app.models import User, Supplier, Category, Product

app = create_app()

def seed_everything():
    with app.app_context():
        print("🌱 Iniciando o povoamento do banco de dados...")

        # 1. CRIAR CATEGORIAS
        print("📦 Criando Categorias...")
        categories_list = ['Bebidas', 'Alimentos', 'Eletrônicos', 'Limpeza', 'Higiene', 'Bazar']
        cats = {} # Dicionário para guardar as categorias criadas e usar depois
        
        for name in categories_list:
            cat = Category.query.filter_by(name=name).first()
            if not cat:
                cat = Category(name=name)
                db.session.add(cat)
            cats[name] = cat # Guarda o objeto para usar nos produtos
        
        db.session.commit() # Salva categorias para gerar os IDs

        # 2. CRIAR FORNECEDORES
        print("🚚 Criando Fornecedores...")
        suppliers_data = [
            {'name': 'Ambev S.A.', 'cnpj': '00.111.222/0001-01', 'city': 'São Paulo'},
            {'name': 'Coca-Cola FEMSA', 'cnpj': '00.333.444/0001-02', 'city': 'Jundiaí'},
            {'name': 'Samsung Eletrônica', 'cnpj': '00.555.666/0001-03', 'city': 'Manaus'},
            {'name': 'Nestlé Brasil', 'cnpj': '00.777.888/0001-04', 'city': 'São Paulo'},
            {'name': 'Unilever Brasil', 'cnpj': '00.999.000/0001-05', 'city': 'Rio de Janeiro'},
        ]
        
        sups = {} # Dicionário para guardar os fornecedores
        
        for s_data in suppliers_data:
            sup = Supplier.query.filter_by(cnpj=s_data['cnpj']).first()
            if not sup:
                sup = Supplier(
                    name=s_data['name'],
                    cnpj=s_data['cnpj'],
                    city=s_data['city'],
                    state='SP',
                    contact_name='Gerente Comercial',
                    phone='(11) 9999-9999'
                )
                db.session.add(sup)
            sups[s_data['name']] = sup
        
        db.session.commit() # Salva fornecedores

        # 3. CRIAR PRODUTOS (Muitos!)
        print("🛒 Criando Produtos...")
        
        # Lista de produtos para criar
        products_data = [
            # Bebidas (Ambev / Coca)
            {'name': 'Cerveja Skol Lata 350ml', 'sku': 'BEB-001', 'cat': 'Bebidas', 'sup': 'Ambev S.A.', 'cost': 2.50, 'price': 4.50, 'qty': 200},
            {'name': 'Cerveja Brahma Duplo Malte', 'sku': 'BEB-002', 'cat': 'Bebidas', 'sup': 'Ambev S.A.', 'cost': 3.00, 'price': 5.50, 'qty': 150},
            {'name': 'Cerveja Stella Artois Long Neck', 'sku': 'BEB-003', 'cat': 'Bebidas', 'sup': 'Ambev S.A.', 'cost': 4.00, 'price': 7.00, 'qty': 100},
            {'name': 'Refrigerante Coca-Cola 2L', 'sku': 'BEB-004', 'cat': 'Bebidas', 'sup': 'Coca-Cola FEMSA', 'cost': 5.00, 'price': 9.00, 'qty': 120},
            {'name': 'Refrigerante Fanta Laranja 2L', 'sku': 'BEB-005', 'cat': 'Bebidas', 'sup': 'Coca-Cola FEMSA', 'cost': 4.50, 'price': 7.50, 'qty': 80},
            {'name': 'Suco Del Valle Uva 1L', 'sku': 'BEB-006', 'cat': 'Bebidas', 'sup': 'Coca-Cola FEMSA', 'cost': 6.00, 'price': 10.00, 'qty': 50},
            
            # Eletrônicos (Samsung)
            {'name': 'Smartphone Galaxy S23', 'sku': 'ELE-001', 'cat': 'Eletrônicos', 'sup': 'Samsung Eletrônica', 'cost': 3000.00, 'price': 4500.00, 'qty': 10},
            {'name': 'Smart TV 55 4K Crystal', 'sku': 'ELE-002', 'cat': 'Eletrônicos', 'sup': 'Samsung Eletrônica', 'cost': 2200.00, 'price': 3100.00, 'qty': 5},
            {'name': 'Monitor Gamer Odyssey 24', 'sku': 'ELE-003', 'cat': 'Eletrônicos', 'sup': 'Samsung Eletrônica', 'cost': 1200.00, 'price': 1800.00, 'qty': 8},
            {'name': 'Fones Galaxy Buds 2', 'sku': 'ELE-004', 'cat': 'Eletrônicos', 'sup': 'Samsung Eletrônica', 'cost': 400.00, 'price': 700.00, 'qty': 20},

            # Alimentos (Nestlé)
            {'name': 'Chocolate KitKat 41g', 'sku': 'ALI-001', 'cat': 'Alimentos', 'sup': 'Nestlé Brasil', 'cost': 2.00, 'price': 4.00, 'qty': 500},
            {'name': 'Leite Condensado Moça', 'sku': 'ALI-002', 'cat': 'Alimentos', 'sup': 'Nestlé Brasil', 'cost': 6.00, 'price': 9.50, 'qty': 100},
            {'name': 'Café Nescafé Tradição', 'sku': 'ALI-003', 'cat': 'Alimentos', 'sup': 'Nestlé Brasil', 'cost': 15.00, 'price': 25.00, 'qty': 60},
            {'name': 'Biscoito Bono Recheado', 'sku': 'ALI-004', 'cat': 'Alimentos', 'sup': 'Nestlé Brasil', 'cost': 2.50, 'price': 4.50, 'qty': 150},

            # Limpeza (Unilever)
            {'name': 'Sabão em Pó OMO 1kg', 'sku': 'LIM-001', 'cat': 'Limpeza', 'sup': 'Unilever Brasil', 'cost': 10.00, 'price': 16.00, 'qty': 80},
            {'name': 'Amaciante Comfort 500ml', 'sku': 'LIM-002', 'cat': 'Limpeza', 'sup': 'Unilever Brasil', 'cost': 8.00, 'price': 14.00, 'qty': 60},
            {'name': 'Desodorante Dove Aero', 'sku': 'HIG-001', 'cat': 'Higiene', 'sup': 'Unilever Brasil', 'cost': 12.00, 'price': 19.90, 'qty': 100},
            {'name': 'Shampoo Seda Ceramidas', 'sku': 'HIG-002', 'cat': 'Higiene', 'sup': 'Unilever Brasil', 'cost': 9.00, 'price': 15.00, 'qty': 90},
        ]

        count = 0
        for p_data in products_data:
            # Verifica se produto já existe pelo SKU
            if not Product.query.filter_by(sku=p_data['sku']).first():
                # Busca os objetos de categoria e fornecedor que criamos antes
                cat_obj = cats.get(p_data['cat']) # Pega do dicionário cats
                sup_obj = sups.get(p_data['sup']) # Pega do dicionário sups
                
                # Se não achou no dicionário (caso rode o script 2 vezes), busca no banco
                if not cat_obj: cat_obj = Category.query.filter_by(name=p_data['cat']).first()
                if not sup_obj: sup_obj = Supplier.query.filter_by(name=p_data['sup']).first()

                new_prod = Product(
                    name=p_data['name'],
                    sku=p_data['sku'],
                    cost=p_data['cost'],
                    price=p_data['price'],
                    quantity=p_data['qty'],
                    min_level=10,
                    category=cat_obj,   # SQLAlchemy lida com a relação aqui
                    supplier=sup_obj    # SQLAlchemy lida com a relação aqui
                )
                db.session.add(new_prod)
                count += 1
        
        db.session.commit()
        print(f"✅ Sucesso! {count} novos produtos cadastrados.")
        print("🚀 Pode rodar o sistema agora!")

if __name__ == '__main__':
    seed_everything()