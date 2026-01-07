from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import db
from . import auth_bp
from app.decorators import admin_required # <--- Importante!


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inventory.index')) 
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('inventory.index'))
        else:
            flash('Usuário ou senha inválidos.')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth_bp.route('/support')
def support():
    # Renderiza a tela de ajuda/suporte
    return render_template('auth/support.html')



from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import db
from . import auth_bp
from app.decorators import admin_required # <--- Importante!

# ... (Mantenha as rotas de login/logout/suporte que já existem) ...

# --- ÁREA ADMINISTRATIVA DE USUÁRIOS ---

@auth_bp.route('/users')
@login_required
@admin_required # Só Admin entra aqui
def users_list():
    users = User.query.all()
    return render_template('auth/users_list.html', users=users)

@auth_bp.route('/users/new', methods=['GET', 'POST'])
@login_required
@admin_required
def user_create():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Verificação simples se já existe
        if User.query.filter_by(username=username).first():
            flash('Este nome de usuário já existe.', 'danger')
        else:
            new_user = User(username=username, role=role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Usuário {username} criado com sucesso!', 'success')
            return redirect(url_for('auth.users_list'))
            
    return render_template('auth/user_form.html', user=None)

@auth_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.role = request.form.get('role')
        
        # Só altera a senha se o campo não estiver vazio
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)
            
        try:
            db.session.commit()
            flash('Dados do usuário atualizados.', 'success')
            return redirect(url_for('auth.users_list'))
        except Exception as e:
            flash('Erro ao atualizar.', 'danger')
            
    return render_template('auth/user_form.html', user=user)

@auth_bp.route('/users/delete/<int:id>')
@login_required
@admin_required
def user_delete(id):
    # REGRA DE OURO: Não permitir que o admin se auto-delete
    if id == current_user.id:
        flash('Você não pode excluir a si mesmo!', 'warning')
        return redirect(url_for('auth.users_list'))
        
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuário {user.username} removido.', 'success')
    return redirect(url_for('auth.users_list'))