import os
from app import create_app, db
from app.models import User, Category, Supplier, Product

# Inicializa a aplicação
app = create_app()

def seed():
    with app.app_context():
        print("🚀 [PASSO 1/4] Iniciando Provisionamento de Banco de Dados...")
        
        # O PULO DO GATO: Cria todas as tabelas no PostgreSQL do Render se elas não existirem
        try:
            db.create_all()
            print("✅ Tabelas verificadas/criadas com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return

        # 1. CRIANDO SEU USUÁRIO ADMINISTRADOR
        print("👤 [PASSO 2/4] Verificando Administrador Mestre...")
        if User.query.filter_by(username="sivaldo").first() is None:
            user_sivaldo = User(
                username="sivaldo",
                role="admin"
            )
            user_sivaldo.set_password("sivaldo@2026")
            db.session.add(user_sivaldo)
            print("✨ Usuário 'sivaldo' adicionado para criação.")
        
        # 2. POPULANDO CATEGORIAS
        print("📦 [PASSO 3/4] Verificando Categorias...")
        categorias_iniciais = ["Bebidas", "Alimentos", "Limpeza", "Higiene"]
        for cat_name in categorias_iniciais:
            if Category.query.filter_by(name=cat_name).first() is None:
                db.session.add(Category(name=cat_name))
                print(f"   + Categoria: {cat_name}")

        # 3. POPULANDO FORNECEDORES
        print("🏢 [PASSO 4/4] Verificando Fornecedores...")
        if Supplier.query.filter_by(name="Ambev").first() is None:
            ambev = Supplier(
                name="Ambev",
                cnpj="02.210.410/0001-01",
                email="contato@ambev.com.br",
                logo="ambev_logo.png" 
            )
            db.session.add(ambev)
            print("   + Fornecedor: Ambev")

        # 4. COMMIT FINAL
        try:
            db.session.commit()
            print("\n✨ BOOTSTRAP CONCLUÍDO COM SUCESSO!")
            print("🔗 O sistema do Sivaldo está online e pronto para o acesso.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro crítico no Commit: {e}")

if __name__ == "__main__":
    seed()