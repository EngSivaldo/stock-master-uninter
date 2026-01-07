from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Movement, Product
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/report')
@login_required
def report():
    # AULA: SQLAlchemy Query
    # Aqui estamos buscando TODAS as movimentações.
    # .order_by(Movement.date.desc()) -> Ordena por Data Decrescente (do mais novo para o mais velho)
    movements = Movement.query.order_by(Movement.date.desc()).all()
    
    return render_template('main/report.html', movements=movements)

# Vamos criar também uma rota para Dashboard (futuro)
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')