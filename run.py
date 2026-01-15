# run.py
from app import create_app

# Instancia a aplicação usando a factory
app = create_app()

if __name__ == "__main__":
    # O host 0.0.0.0 é importante para containers (Docker)
    # O debug deve vir de variáveis de ambiente em produção
    app.run(host="0.0.0.0", port=5000)