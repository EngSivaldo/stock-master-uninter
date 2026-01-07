from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Product, Movement, Supplier
from app.extensions import db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
@login_required
def index():
    # Se ainda não tivermos templates, vamos retornar texto simples para testar
    products = Product.query.all()
    return render_template('inventory/index.html', products=products)

@inventory_bp.route('/movement/new', methods=['GET', 'POST'])
@login_required
def new_movement():
    products = Product.query.all()
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        mov_type = request.form.get('type')
        quantity = int(request.form.get('quantity'))
        
        product = Product.query.get(product_id)
        
        if not product:
            flash('Produto não encontrado.')
            return redirect(url_for('inventory.new_movement'))

        try:
            if mov_type == 'OUT':
                if product.quantity < quantity:
                    flash(f'Erro: Saldo insuficiente! Estoque atual: {product.quantity}', 'danger')
                    return redirect(url_for('inventory.new_movement'))
                product.quantity -= quantity
            elif mov_type == 'IN':
                product.quantity += quantity
            
            movement = Movement(type=mov_type, quantity=quantity, product_id=product.id, user_id=current_user.id)
            
            db.session.add(movement)
            db.session.commit()
            flash('Movimentação realizada com sucesso!', 'success')
            return redirect(url_for('inventory.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao processar: {str(e)}', 'danger')
            
    return render_template('inventory/movement_form.html', products=products)