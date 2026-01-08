from flask import render_template, Response
from flask_login import login_required
from app.models import Product, Supplier, Movement, Category
from . import main_bp
from app.extensions import db
import csv
import io


@main_bp.route('/')
@login_required
def report():
    products = Product.query.all()
    
    # 1. KPIs Gerais
    total_items = len(products)
    total_cost = sum(p.cost * p.quantity for p in products)
    total_revenue_potential = sum(p.price * p.quantity for p in products)
    low_stock_products = [p for p in products if p.quantity <= p.min_level]

    # 2. DADOS DO GRÁFICO (AGORA POR CATEGORIA 🏷️)
    # Fazemos uma query agrupada: Nome da Categoria + Soma do Custo do Estoque
    category_data = db.session.query(
        Category.name, 
        db.func.sum(Product.quantity * Product.cost)
    ).join(Product).group_by(Category.name).all()

    # Prepara as listas para o Chart.js
    chart_labels = []
    chart_data = []

    for name, value in category_data:
        chart_labels.append(name) # Ex: 'Eletrônicos'
        chart_data.append(float(value)) # Ex: 15000.00
        
    # Se não tiver dados (banco vazio), evita erro no gráfico
    if not chart_data:
        chart_labels = ["Sem dados"]
        chart_data = [0]

    return render_template('main/report.html', 
                         products=products,
                         total_items=total_items,
                         total_cost=total_cost,
                         total_revenue_potential=total_revenue_potential,
                         low_stock_products=low_stock_products,
                         chart_labels=chart_labels, # Passando labels de Categoria
                         chart_data=chart_data)     #

# --- ROTA EXTRA: Exportar para Excel (CSV) ---
@main_bp.route('/export/csv')
@login_required
def export_csv():
    products = Product.query.all()
    
    # Cria um arquivo na memória (não salva no disco)
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalho
    writer.writerow(['ID', 'SKU', 'Nome', 'Fornecedor', 'Custo (R$)', 'Venda (R$)', 'Estoque Atual'])
    
    # Linhas
    for p in products:
        writer.writerow([p.id, p.sku, p.name, p.supplier.name, p.cost, p.price, p.quantity])
        
    # Prepara a resposta para download
    output.seek(0)
    return Response(
        output, 
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=estoque_completo.csv"}
    )

# Vamos criar também uma rota para Dashboard (futuro)
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')