# Stock Master - Sistema de Gerenciamento de Estoques 📦

Projeto desenvolvido como requisito parcial para o **Estágio Supervisionado Obrigatório** do curso de **Engenharia de Software** do Centro Universitário Internacional **UNINTER**.

**Aluno:** Sivaldo Vieira de Almeida  
**RU:**  
**Ano:** 2026

## 🎯 Objetivos

O Stock Master visa solucionar problemas de controle de mercadorias em PMEs, garantindo rastreabilidade de entradas e saídas e evitando rupturas de estoque.

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework:** Flask 3.x
- **Banco de Dados:** SQLite (SQLAlchemy ORM)
- **Frontend:** Bootstrap 5 & Jinja2
- **Autenticação:** Flask-Login (RBAC: Admin/Operador)

## ⚙️ Funcionalidades

- [x] Login e Autenticação Segura
- [x] Controle de Acesso (Admin vs Operador)
- [x] Cadastro de Produtos e Fornecedores
- [x] Movimentação de Estoque (Entrada/Saída)
- [x] Validação de Saldo Negativo (Transação Atômica)

## 🔧 Como rodar o projeto

```bash
# Clone o repositório
git clone [https://github.com/EngSivaldo/stock-master-uninter.git](https://github.com//stock-master-uninter.git)

# Entre na pasta
cd stock-master-uninter

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados
flask db upgrade

# Crie o usuário Admin via Shell
# (Ver instruções no relatório)

# Execute
python run.py
```

Projeto Simulado - TUCURUÍ/PA - 2026
