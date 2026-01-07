from app import create_app
from app.extensions import db
from app.models import User, Supplier

app = create_app()

# --- BLOCO DE AUTOMAÇÃO (SEED) ---
def seed_database():
    """Cria dados iniciais se o banco estiver vazio"""
    with app.app_context():
        # Garante que as tabelas existem (caso o migrate falhe ou não tenha sido rodado)
        db.create_all()

        # 1. Verifica e Cria o ADMIN
        if not User.query.filter_by(username='admin').first():
            print("⚠️ Admin não encontrado. Criando automaticamente...")
            admin = User(username='admin', role='admin')
            admin.set_password('123456') # Senha Padrão de Desenvolvimento
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário 'admin' criado! (Senha: 123456)")
        
        # ... (início do arquivo igual) ...

        # 2. Verifica e Cria FORNECEDORES Padrão
        if not Supplier.query.first():
            print("⚠️ Nenhum fornecedor encontrado. Criando padrões...")
            
            # Criando com a NOVA estrutura
            s1 = Supplier(
                name='Fornecedor Padrão', 
                cnpj='00.000.000/0001-00',
                contact_name='Gerente de Contas',
                email='contato@padrao.com.br',
                phone='(11) 99999-9999',
                city='São Paulo',
                state='SP'
            )
            
            db.session.add(s1)
            db.session.commit()
            print("✅ Fornecedores de teste criados!")

# ... (final do arquivo igual) ...

# Executa a verificação sempre que o script rodar
seed_database()
# ---------------------------------

if __name__ == '__main__':
    app.run(debug=True)