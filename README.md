 💰 Sistema Financeiro Simplificado

Aplicação backend para controle financeiro pessoal, desenvolvida com **Python + Flask** e banco de dados relacional. Permite que usuários registrem receitas e despesas categorizadas, com validação de regras de negócio para garantir a consistência dos dados.

---

## 📋 Descrição do Sistema

O sistema permite o cadastro de usuários e categorias financeiras, além do registro de lançamentos (entradas e saídas). Cada lançamento é obrigatoriamente associado a um usuário e a uma categoria, e passa por validações para garantir integridade dos dados. A aplicação também oferece um resumo financeiro por usuário, com totais de entradas, saídas e saldo calculado.

---

## 🗄️ Estrutura do Banco de Dados

O banco possui **3 tabelas** com relacionamentos entre si:

### `usuarios`
| Coluna       | Tipo         | Descrição                        |
|--------------|--------------|----------------------------------|
| `id`         | Integer (PK) | Identificador único              |
| `nome`       | String(100)  | Nome do usuário                  |
| `email`      | String(150)  | E-mail único do usuário          |
| `criado_em`  | DateTime     | Data/hora de criação do registro |

### `categorias`
| Coluna      | Tipo         | Descrição                  |
|-------------|--------------|----------------------------|
| `id`        | Integer (PK) | Identificador único        |
| `nome`      | String(100)  | Nome da categoria          |
| `descricao` | String(255)  | Descrição opcional         |

### `lancamentos`
| Coluna         | Tipo         | Descrição                                   |
|----------------|--------------|---------------------------------------------|
| `id`           | Integer (PK) | Identificador único                         |
| `descricao`    | String(255)  | Descrição do lançamento                     |
| `valor`        | Float        | Valor positivo do lançamento                |
| `tipo`         | String(10)   | Tipo: `"entrada"` ou `"saida"`              |
| `data`         | DateTime     | Data/hora do lançamento                     |
| `usuario_id`   | Integer (FK) | Referência ao usuário (`usuarios.id`)       |
| `categoria_id` | Integer (FK) | Referência à categoria (`categorias.id`)    |

**Relacionamentos:**
- `usuarios` → `lancamentos`: 1:N (um usuário pode ter vários lançamentos)
- `categorias` → `lancamentos`: 1:N (uma categoria pode ter vários lançamentos)

---

## 🚦 Rotas da Aplicação

### Usuários — `/usuarios`

| Método   | Rota             | Descrição                        |
|----------|------------------|----------------------------------|
| `POST`   | `/usuarios/`     | Cadastrar novo usuário           |
| `GET`    | `/usuarios/`     | Listar todos os usuários         |
| `GET`    | `/usuarios/<id>` | Buscar usuário por ID            |
| `PUT`    | `/usuarios/<id>` | Atualizar dados do usuário       |
| `DELETE` | `/usuarios/<id>` | Remover usuário                  |

### Categorias — `/categorias`

| Método   | Rota               | Descrição                      |
|----------|--------------------|--------------------------------|
| `POST`   | `/categorias/`     | Criar nova categoria           |
| `GET`    | `/categorias/`     | Listar todas as categorias     |
| `GET`    | `/categorias/<id>` | Buscar categoria por ID        |
| `PUT`    | `/categorias/<id>` | Atualizar categoria            |
| `DELETE` | `/categorias/<id>` | Remover categoria              |

### Lançamentos — `/lancamentos`

| Método   | Rota                           | Descrição                                              |
|----------|--------------------------------|--------------------------------------------------------|
| `POST`   | `/lancamentos/`                | Criar novo lançamento                                  |
| `GET`    | `/lancamentos/`                | Listar lançamentos (filtros opcionais por query params)|
| `GET`    | `/lancamentos/<id>`            | Buscar lançamento por ID                               |
| `GET`    | `/lancamentos/resumo/<usuario_id>` | Resumo financeiro do usuário (entradas, saídas, saldo)|
| `PUT`    | `/lancamentos/<id>`            | Atualizar lançamento                                   |
| `DELETE` | `/lancamentos/<id>`            | Remover lançamento                                     |

#### Filtros disponíveis em `GET /lancamentos/`
| Parâmetro      | Tipo    | Descrição                          |
|----------------|---------|------------------------------------|
| `usuario_id`   | Integer | Filtra por usuário                 |
| `tipo`         | String  | Filtra por `"entrada"` ou `"saida"`|
| `categoria_id` | Integer | Filtra por categoria               |

---

## ⚙️ Regras de Negócio

1. **Valor positivo obrigatório:** todo lançamento deve ter `valor > 0`. Valores zerados ou negativos são rejeitados com erro `422`.

2. **Tipo restrito:** o campo `tipo` aceita somente `"entrada"` ou `"saida"`. Qualquer outro valor é rejeitado com erro `422`.

3. **Categoria obrigatória:** todo lançamento deve estar associado a uma categoria existente. Não é possível criar um lançamento com `categoria_id` inválido.

4. **Usuário obrigatório:** todo lançamento deve estar associado a um usuário existente. Não é possível criar um lançamento com `usuario_id` inválido.

5. **E-mail único:** não é permitido cadastrar dois usuários com o mesmo e-mail. Tentativas retornam erro `409`.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10+
- pip

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd backend
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Copie o arquivo de exemplo e preencha com seus dados:
```bash
cp .env.example .env
```

Edite o `.env`:
```env
DATABASE_URL=sqlite:///financeiro.db
SECRET_KEY=sua-chave-secreta
```

### 5. Execute as migrations
```bash
flask db upgrade
```

### 6. Inicie o servidor
```bash
python run.py
```

A API estará disponível em `http://localhost:5000`.

---

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py          # Factory da aplicação Flask
│   ├── models.py            # Modelos do banco de dados
│   └── routes/
│       ├── usuarios.py      # Rotas de usuários
│       ├── categorias.py    # Rotas de categorias
│       └── lancamentos.py   # Rotas de lançamentos
├── migrations/              # Versionamento do banco (Flask-Migrate)
├── frontend/
│   └── index.html           # Interface web (opcional)
├── .env.example             # Exemplo de variáveis de ambiente
├── .gitignore
├── banco.sql                # Script SQL do banco
├── requirements.txt
└── run.py                   # Ponto de entrada da aplicação
```

---

## 🛠️ Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- SQLite (padrão) ou outro banco via `DATABASE_URL`
