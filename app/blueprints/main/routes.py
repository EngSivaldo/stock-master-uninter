from flask import render_template, Response
from flask_login import login_required
from app.models import Product, Supplier, Movement
from . import main_bp
from app.extensions import db
import csv
import io


from flask import render_template, Response
from flask_login import login_required
from app.models import Product, Supplier, Movement
from . import main_bp
from app.extensions import db
import csv
import io

@main_bp.route('/')
@login_required
def report():
    # 1. Dados Gerais
    products = Product.query.all()
    total_items = len(products)
    
    # 2. Cálculo Financeiro (Custo Total do Estoque)
    # Soma (Quantidade * Preço de Custo) de cada produto
    total_cost = sum(p.quantity * p.cost for p in products)
    
    # Soma (Quantidade * Preço de Venda) - Valor potencial de venda
    total_revenue_potential = sum(p.quantity * p.price for p in products)

    # 3. Produtos com Estoque Baixo (Alerta)
    low_stock_products = [p for p in products if p.quantity <= p.min_level]

    # 4. Dados para o Gráfico (Top 5 Fornecedores por Quantidade de Produtos)
    # Isso é um pouco de "Magia SQL" feita em Python para simplificar
    suppliers = Supplier.query.all()
    chart_labels = []
    chart_data = []
    
    for s in suppliers:
        # Conta quantos produtos esse fornecedor tem cadastrados
        qtd_prods = len(s.products) 
        if qtd_prods > 0:
            chart_labels.append(s.name)
            chart_data.append(qtd_prods)

    return render_template('main/report.html', 
                         products=products,
                         total_items=total_items,
                         total_cost=total_cost,
                         total_revenue_potential=total_revenue_potential,
                         low_stock_products=low_stock_products,
                         chart_labels=chart_labels,
                         chart_data=chart_data)

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