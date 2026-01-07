from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Product, Movement, Supplier, Category, User 
from app.decorators import admin_required
from datetime import datetime  
from app.extensions import db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
@login_required
def index():
    # 1. Captura termo de busca e número da página da URL
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int) # Padrão é página 1
    per_page = 10 # Produtos por página (mude para testar, ex: 2)
    
    # 2. Monta a Query BASE (sem executar ainda)
    query = Product.query

    # 3. Aplica filtro de busca se existir
    if search_query:
        query = query.filter(
            (Product.name.contains(search_query)) | 
            (Product.sku.contains(search_query))
        )
    
    # 4. A MÁGICA: .paginate() em vez de .all()
    # Isso executa a query no banco com LIMIT e OFFSET automaticamente
    products_pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    formatted_date = datetime.now().strftime('%d/%m/%Y')
    
    return render_template('inventory/index.html', 
                         products=products_pagination, # Passamos o objeto paginador
                         now=formatted_date,
                         search_query=search_query)

@inventory_bp.route('/movement/new', methods=['GET', 'POST'])
@login_required
def new_movement():
    products = Product.query.all()
    
    # --- MELHORIA SÊNIOR: Buscando o histórico recente ---
    # Pegamos as últimas 10 movimentações para exibir na tela (Feedback visual)
    recent_movements = Movement.query.order_by(Movement.date.desc()).limit(10).all()
    # -----------------------------------------------------

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        mov_type = request.form.get('type') # 'IN' ou 'OUT'
        quantity = int(request.form.get('quantity'))
        
        product = Product.query.get(product_id)
        
        if not product:
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('inventory.new_movement'))

        try:
            if mov_type == 'OUT':
                if product.quantity < quantity:
                    flash(f'Erro: Saldo insuficiente! Estoque atual: {product.quantity}', 'danger')
                    return redirect(url_for('inventory.new_movement'))
                
                product.quantity -= quantity
                
            elif mov_type == 'IN':
                product.quantity += quantity
            
            # Registra quem fez (current_user.id) e quando (data automática do banco)
            movement = Movement(
                type=mov_type, 
                quantity=quantity, 
                product_id=product.id,
                user_id=current_user.id
            )
            
            db.session.add(movement)
            db.session.commit()
            flash('Movimentação realizada com sucesso!', 'success')
            
            # Mantemos na mesma tela para facilitar lançamentos contínuos
            return redirect(url_for('inventory.new_movement'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao processar movimentação: {str(e)}', 'danger')
            
    # Passamos a lista 'recent_movements' para o HTML
    return render_template('inventory/movement_form.html', products=products, movements=recent_movements)



@inventory_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
@admin_required   # <--- BLOQUEIA OPERADORES AQUI
def add_product():
    # 1. Buscamos todos os fornecedores para preencher o <select> no formulário
    suppliers = Supplier.query.all()
    categories = Category.query.all() 
    
    if request.method == 'POST':
        name = request.form.get('name')
        sku = request.form.get('sku')
        supplier_id = request.form.get('supplier_id')
        category_id = request.form.get('category_id') # <--- Captura do form
        min_level = int(request.form.get('min_level'))
        # Lendo os dois preços
        cost = float(request.form.get('cost'))   
        price = float(request.form.get('price'))
        
        # Validação: Verifica se o SKU já existe para evitar duplicidade
        existing_product = Product.query.filter_by(sku=sku).first()
        if existing_product:
            flash(f'Erro: O SKU {sku} já está cadastrado.', 'danger')
            return redirect(url_for('inventory.add_product'))
            
        # Criação do Objeto Produto
        # Nota: Começamos com quantity=0. O correto é dar entrada via Movimentação depois.
        new_product = Product(
            name=name,
            sku=sku,
            supplier_id=supplier_id,
            category_id=category_id, # <--- Salva no banco
            min_level=min_level,
            cost=cost,   
            price=price,
            quantity=0 
        )
        
        try:
            db.session.add(new_product)
            db.session.commit()
            flash(f'Produto "{name}" cadastrado com sucesso!', 'success')
            return redirect(url_for('inventory.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar: {str(e)}', 'danger')
            
    return render_template('inventory/product_form.html', suppliers=suppliers)


# ... (códigos anteriores)

@inventory_bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required   # <--- E AQUI TAMBÉM
def edit_product(id):
    # Busca o produto pelo ID ou retorna erro 404 se não existir
    product = Product.query.get_or_404(id)
    suppliers = Supplier.query.all()
    categories = Category.query.all() # <--- Busca categorias
    
    if request.method == 'POST':
        # Atualiza os campos com o que veio do formulário
        product.name = request.form.get('name')
        # product.sku = request.form.get('sku') # Geralmente não permitimos mudar SKU (Regra de Negócio)
        product.supplier_id = request.form.get('supplier_id')
        product.category_id = request.form.get('category_id') # <--- Atualiza
        product.min_level = int(request.form.get('min_level'))
        product.cost = float(request.form.get('cost'))
        product.price = float(request.form.get('price'))
        
        # Nota Sênior: Não alteramos a 'quantity' aqui! 
        # Estoque só se mexe via Movimentação (Entrada/Saída). Isso garante rastreabilidade.
        
        try:
            db.session.commit() # Apenas salvamos o objeto que já existia
            flash(f'Produto "{product.name}" atualizado com sucesso!', 'success')
            return redirect(url_for('inventory.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar: {str(e)}', 'danger')
            
    # Renderizamos o MESMO formulário de criação, mas passando o objeto 'product' para preencher os campos
    return render_template('inventory/product_form.html', suppliers=suppliers, product=product)

# No topo do arquivo, garanta que Movement está importado
# from app.models import Product, Movement, Supplier

@inventory_bp.route('/product/<int:id>')
@login_required
def product_details(id):
    product = Product.query.get_or_404(id)
    
    # Buscamos as movimentações APENAS deste produto, ordenadas pela data
    movements = Movement.query.filter_by(product_id=id).order_by(Movement.date.desc()).all()
    
    return render_template('inventory/product_details.html', product=product, movements=movements)



# --- GESTÃO DE FORNECEDORES ---

@inventory_bp.route('/suppliers')
@login_required
def suppliers_list():
    suppliers = Supplier.query.all()
    return render_template('inventory/suppliers_list.html', suppliers=suppliers)

@inventory_bp.route('/suppliers/new', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        # Captura todos os campos do form completo
        data = {
            'name': request.form.get('name'),
            'cnpj': request.form.get('cnpj'),
            'contact_name': request.form.get('contact_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'state': request.form.get('state')
        }
        
        # Cria o objeto desempacotando o dicionário (**data)
        supplier = Supplier(**data)
        
        try:
            db.session.add(supplier)
            db.session.commit()
            flash(f'Fornecedor {data["name"]} cadastrado!', 'success')
            return redirect(url_for('inventory.suppliers_list'))
        except:
            db.session.rollback()
            flash('Erro: CNPJ já cadastrado ou dados inválidos.', 'danger')
        
    return render_template('inventory/supplier_form.html', supplier=None)

@inventory_bp.route('/suppliers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    
    if request.method == 'POST':
        supplier.name = request.form.get('name')
        supplier.cnpj = request.form.get('cnpj')
        supplier.contact_name = request.form.get('contact_name')
        supplier.email = request.form.get('email')
        supplier.phone = request.form.get('phone')
        supplier.address = request.form.get('address')
        supplier.city = request.form.get('city')
        supplier.state = request.form.get('state')
        
        try:
            db.session.commit()
            flash('Dados atualizados com sucesso.', 'success')
            return redirect(url_for('inventory.suppliers_list'))
        except:
            db.session.rollback()
            flash('Erro ao atualizar. Verifique se o CNPJ já existe.', 'danger')
        
    return render_template('inventory/supplier_form.html', supplier=supplier)