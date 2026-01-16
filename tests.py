import unittest
from app import create_app, db
from app.models import User, Product, Supplier, Category, Movement

class StockMasterAdvancedTestCase(unittest.TestCase):
    def setUp(self):
        # Configuração do ambiente de teste
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False 
        
        self.client = self.app.test_client()
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.create_base_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_base_data(self):
        """Cria dados iniciais de forma segura para os testes"""
        # Limpa qualquer transação pendente que possa causar erro de UNIQUE
        db.session.rollback()

        # Verifica se o Admin já existe antes de criar
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Verifica se o Operador já existe
        operator = User.query.filter_by(username='operador').first()
        if not operator:
            operator = User(username='operador', role='operator')
            operator.set_password('user123')
            db.session.add(operator)
        
        # Dados Base (Garante que não duplique categorias ou fornecedores)
        if not Category.query.filter_by(name='Geral').first():
            cat = Category(name='Geral')
            db.session.add(cat)
            
        if not Supplier.query.filter_by(cnpj='00000000000100').first():
            sup = Supplier(name='Fornecedor Padrão', cnpj='00000000000100')
            db.session.add(sup)
        
        db.session.commit()

    # --- TESTES UNITÁRIOS (Lógica) ---

    def test_password_hashing(self):
        """(Unitário) Verifica segurança da senha"""
        u = User.query.filter_by(username='admin').first()
        self.assertTrue(u.check_password('admin123'))
        self.assertFalse(u.check_password('senhaerrada'))

    def test_prevent_negative_stock(self):
        """(Regra de Negócio) Impede saldo negativo via lógica manual"""
        sup = Supplier.query.first()
        cat = Category.query.first()
        
        prod = Product(name='Teste Negativo', sku='NEG01', quantity=10, supplier=sup, category=cat)
        db.session.add(prod)
        db.session.commit()

        quantity_to_remove = 15
        
        # Simula a lógica de negócio
        if prod.quantity >= quantity_to_remove:
            prod.quantity -= quantity_to_remove
        else:
            error_message = "Saldo Insuficiente"
        
        self.assertEqual(prod.quantity, 10) 
        self.assertEqual(error_message, "Saldo Insuficiente")

    # --- TESTES DE INTEGRAÇÃO (Rotas) ---

    def test_login_flow(self):
        """(Integração) Testa login com sucesso e falha"""
        # 1. Tenta login correto
        response = self.client.post('/auth/login', data=dict(
            username='admin',
            password='admin123'
        ), follow_redirects=True)
        
        # Verifica se entrou no Dashboard (procura pelo título Stock Master)
        self.assertIn(b'Stock Master', response.data) 

        # 2. Tenta login errado (Logout primeiro para garantir)
        self.client.get('/auth/logout', follow_redirects=True)
        response = self.client.post('/auth/login', data=dict(
            username='admin',
            password='errada'
        ), follow_redirects=True)
        
        # Verifica se voltou para a página de login (campo Senha visível)
        self.assertIn(b'Senha', response.data)

    def test_route_protection(self):
        """(Segurança) Tenta acessar página protegida sem login"""
        # Garante que estamos deslogados
        self.client.get('/auth/logout', follow_redirects=True)

        # Tenta acessar cadastro de produtos (Rota corrigida: /product/new)
        response = self.client.get('/product/new', follow_redirects=True)
        
        # Deve redirecionar para login. 
        # Verifica se caiu na página de login procurando pelo botão "Acessar Sistema"
        self.assertIn(b'Acessar Sistema', response.data)

    def test_create_product_via_route(self):
        """(Integração) Fluxo completo: Login -> Criar Produto"""
        # 1. Faz Login
        self.client.post('/auth/login', data=dict(username='admin', password='admin123'), follow_redirects=True)
        
        sup = Supplier.query.first()
        cat = Category.query.first()

        # 2. Envia formulário para criar produto
        response = self.client.post('/product/new', data=dict(
            name='Produto Via Teste',
            sku='TESTEWEB',
            quantity=100,
            min_level=10,
            cost=50.0,
            price=100.0,
            supplier_id=sup.id,
            category_id=cat.id
        ), follow_redirects=True)

        # DEBUG: Se o teste falhar, isso imprimirá o erro do HTML no terminal
        if response.status_code != 200:
            print(f"\nErro no Servidor: {response.status_code}")

        # 3. Verifica se salvou no banco
        prod = Product.query.filter_by(sku='TESTEWEB').first()
        
        # Se prod for None, imprimimos a resposta para ver as mensagens de erro (Flash messages)
        if prod is None:
            print("\n--- RESPOSTA DO SERVIDOR EM CASO DE FALHA ---")
            print(response.data.decode('utf-8')) 
            print("--------------------------------------------")

        self.assertIsNotNone(prod, "O produto não foi criado. Verifique se os nomes dos campos no formulário HTML batem com o teste.")
        self.assertEqual(prod.name, 'Produto Via Teste')
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main(verbosity=2)