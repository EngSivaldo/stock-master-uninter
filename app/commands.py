import click
from flask.cli import with_appcontext
from app.extensions import db  # <--- Importação correta para sua estrutura
from app.models import User    # Certifique-se que o model User existe aqui

def register_commands(app):
    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("password")
    @with_appcontext
    def create_admin(username, password):
        """Cria um usuário administrador via terminal."""
        # Verifica se já existe
        if User.query.filter_by(username=username).first():
            click.echo(f"[-] Erro: O usuário '{username}' já existe no sistema.")
            return

        try:
            # Cria o objeto admin
            new_admin = User(username=username, role='admin')
            # O seu model User deve ter este método para gerar o hash da senha
            new_admin.set_password(password)
            
            db.session.add(new_admin)
            db.session.commit()
            click.echo(f"[+] Sucesso: Administrador '{username}' criado com sucesso!")
        except Exception as e:
            db.session.rollback()
            click.echo(f"[-] Erro crítico ao salvar no banco: {e}")