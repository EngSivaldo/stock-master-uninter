import os
from app import create_app, db
from app.models import User, Category, Supplier, Product

app = create_app()

def seed():
    with app.app_context():
        print("🚀 [PASSO 1/5] Iniciando Provisionamento de Infraestrutura...")
        
        # GARANTIA SÊNIOR: Cria as tabelas no PostgreSQL do Render
        try:
            db.drop_all() # Isso apaga as tabelas antigas (limite 128)
            db.create_all()
            print("✅ Banco de Dados: Tabelas verificadas/criadas.")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return

        # 1. CRIANDO ADMINISTRADOR (Dados de seed_db.py)
        print("👤 [PASSO 2/5] Configurando Acesso Administrativo...")
        if User.query.filter_by(username="sivaldo").first() is None:
            user_sivaldo = User(username="sivaldo", role="admin")
            user_sivaldo.set_password("sivaldo@2026")
            db.session.add(user_sivaldo)
            print("✨ Administrador 'sivaldo' pronto para criação.")

        # 2. CRIANDO CATEGORIAS (Dados de seed_data.py)
        print("📦 [PASSO 3/5] Povoando Categorias...")
        categories_list = ['Bebidas', 'Alimentos', 'Eletrônicos', 'Limpeza', 'Higiene', 'Bazar']
        cats = {}
        for name in categories_list:
            cat = Category.query.filter_by(name=name).first()
            if not cat:
                cat = Category(name=name)
                db.session.add(cat)
            cats[name] = cat
        db.session.commit() # Commit parcial para gerar IDs de categoria

        # 3. CRIANDO FORNECEDORES (Dados de seed_data.py)
        print("🚚 [PASSO 4/5] Mapeando Fornecedores...")
        suppliers_data = [
            {'name': 'Ambev S.A.', 'cnpj': '00.111.222/0001-01', 'city': 'São Paulo'},
            {'name': 'Coca-Cola FEMSA', 'cnpj': '00.333.444/0001-02', 'city': 'Jundiaí'},
            {'name': 'Samsung Eletrônica', 'cnpj': '00.555.666/0001-03', 'city': 'Manaus'},
            {'name': 'Nestlé Brasil', 'cnpj': '00.777.888/0001-04', 'city': 'São Paulo'},
            {'name': 'Unilever Brasil', 'cnpj': '00.999.000/0001-05', 'city': 'Rio de Janeiro'},
        ]
        sups = {}
        for s_data in suppliers_data:
            sup = Supplier.query.filter_by(cnpj=s_data['cnpj']).first()
            if not sup:
                sup = Supplier(name=s_data['name'], cnpj=s_data['cnpj'], city=s_data['city'], 
                               state='SP', contact_name='Gerente Comercial', phone='(11) 9999-9999')
                db.session.add(sup)
            sups[s_data['name']] = sup
        db.session.commit() # Commit parcial para gerar IDs de fornecedor

        # 4. CRIANDO PRODUTOS (Dados de seed_data.py)
        print("🛒 [PASSO 5/5] Carregando Inventário Inicial...")
        products_data = [
            {'name': 'Cerveja Skol Lata 350ml', 'sku': 'BEB-001', 'cat': 'Bebidas', 'sup': 'Ambev S.A.', 'cost': 2.50, 'price': 4.50, 'qty': 200},
            {'name': 'Smartphone Galaxy S23', 'sku': 'ELE-001', 'cat': 'Eletrônicos', 'sup': 'Samsung Eletrônica', 'cost': 3000.00, 'price': 4500.00, 'qty': 10},
            {'name': 'Chocolate KitKat 41g', 'sku': 'ALI-001', 'cat': 'Alimentos', 'sup': 'Nestlé Brasil', 'cost': 2.00, 'price': 4.00, 'qty': 500},
            {'name': 'Sabão em Pó OMO 1kg', 'sku': 'LIM-001', 'cat': 'Limpeza', 'sup': 'Unilever Brasil', 'cost': 10.00, 'price': 16.00, 'qty': 80}
            # ... Você pode adicionar os outros produtos aqui seguindo o mesmo padrão
        ]
        
        prod_count = 0
        for p_data in products_data:
            if not Product.query.filter_by(sku=p_data['sku']).first():
                cat_obj = cats.get(p_data['cat']) or Category.query.filter_by(name=p_data['cat']).first()
                sup_obj = sups.get(p_data['sup']) or Supplier.query.filter_by(name=p_data['sup']).first()
                
                new_prod = Product(
                    name=p_data['name'], sku=p_data['sku'], cost=p_data['cost'], 
                    price=p_data['price'], quantity=p_data['qty'], min_level=10,
                    category=cat_obj, supplier=sup_obj
                )
                db.session.add(new_prod)
                prod_count += 1

        # COMMIT FINAL
        try:
            db.session.commit()
            print(f"\n✨ SUCESSO: {prod_count} produtos cadastrados!")
            print("🚀 O sistema de Sivaldo Vieira está pronto para produção.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro crítico no salvamento: {e}")

if __name__ == "__main__":
    seed()