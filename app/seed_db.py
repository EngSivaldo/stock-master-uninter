import os
from app import create_app, db
from app.models import User, Category, Supplier, Product

# Define o ambiente
env = os.environ.get('FLASK_CONFIG') or 'production'
app = create_app(env)

def seed():
    with app.app_context():
        print(f"DEBUG: Iniciando Sincronização Sênior para Sivaldo no ambiente: {env}")

        # 1. CRIANDO SEU USUÁRIO ADMINISTRADOR
        # Usando seu nome conforme os registros acadêmicos
        admin_email = "sivaldo@teste.com"
        if User.query.filter_by(username="sivaldo").first() is None:
            print(f"👤 Criando administrador mestre: Sivaldo Vieira de Almeida")
            user_sivaldo = User(
                username="sivaldo",
                role="admin"
            )
            user_sivaldo.set_password("sivaldo@2026")
            db.session.add(user_sivaldo)
        
        # 2. POPULANDO CATEGORIAS
        categorias_iniciais = ["Bebidas", "Alimentos", "Limpeza", "Higiene"]
        for cat_name in categorias_iniciais:
            if Category.query.filter_by(name=cat_name).first() is None:
                print(f"📦 Criando categoria: {cat_name}")
                db.session.add(Category(name=cat_name))

        # 3. POPULANDO FORNECEDORES (Com o novo campo logo)
        if Supplier.query.filter_by(name="Ambev").first() is None:
            print(f"🏢 Criando fornecedor: Ambev")
            ambev = Supplier(
                name="Ambev",
                cnpj="02.210.410/0001-01",
                email="contato@ambev.com.br",
                logo="ambev_logo.png" # Certifique-se de ter este arquivo na pasta assets
            )
            db.session.add(ambev)

        # 4. COMMIT FINAL
        try:
            db.session.commit()
            print("✨ Bootstrap Concluído! O sistema do Sivaldo está online e seguro.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro crítico no Bootstrap: {e}")

if __name__ == "__main__":
    seed()