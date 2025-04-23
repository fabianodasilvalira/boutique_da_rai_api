# README - Backend FastAPI para Landing Page de Perfumes

Este projeto implementa um backend completo usando FastAPI para a landing page de perfumes, seguindo o padrão SOLID. O backend foi desenvolvido com uma arquitetura modular e extensível, utilizando SQLite como banco de dados inicial, mas preparado para migração futura para PostgreSQL.

## Estrutura do Projeto

```
perfumes_api/
├── app/
│   ├── api/
│   ├── core/
│   │   ├── config.py         # Configurações da aplicação
│   │   └── database.py       # Configuração do banco de dados
│   ├── models/
│   │   └── models.py         # Modelos SQLAlchemy
│   ├── repositories/
│   │   └── repositories.py   # Camada de acesso a dados
│   ├── routers/
│   │   ├── categorias.py     # Endpoints de categorias
│   │   ├── produtos.py       # Endpoints de produtos
│   │   ├── quiz.py           # Endpoints do quiz
│   │   ├── contatos.py       # Endpoints de contatos
│   │   └── usuarios.py       # Endpoints de usuários
│   ├── schemas/
│   │   └── schemas.py        # Schemas Pydantic
│   ├── services/
│   │   └── services.py       # Camada de serviços
│   └── main.py               # Aplicação principal
├── migrations/               # Migrações Alembic
├── tests/
│   └── test_api.py           # Testes da API
├── venv/                     # Ambiente virtual Python
├── alembic.ini               # Configuração do Alembic
├── setup_migrations.py       # Script para configurar migrações
├── start.sh                  # Script para iniciar a API
└── run_tests.sh              # Script para executar testes
```

## Entidades Principais

1. **Categorias**: Tipos de produtos (masculino, feminino, unissex, infantil, cosméticos, bijuterias)
2. **Produtos**: Itens disponíveis para venda
3. **Quiz**: Sistema de recomendação de perfumes baseado em preferências
4. **Contatos**: Formulário de contato para clientes
5. **Usuários**: Sistema de autenticação para administração

## Tecnologias Utilizadas

- **FastAPI**: Framework web de alta performance
- **SQLAlchemy**: ORM para interação com banco de dados
- **Pydantic**: Validação de dados e serialização
- **Alembic**: Gerenciamento de migrações de banco de dados
- **SQLite**: Banco de dados inicial (preparado para migração para PostgreSQL)
- **JWT**: Autenticação baseada em tokens

## Padrão SOLID

O projeto segue os princípios SOLID:

1. **S - Princípio da Responsabilidade Única**: Cada classe tem uma única responsabilidade
2. **O - Princípio Aberto-Fechado**: Entidades extensíveis sem modificação
3. **L - Princípio da Substituição de Liskov**: Subclasses podem substituir suas classes base
4. **I - Princípio da Segregação de Interface**: Interfaces específicas são melhores que uma única interface geral
5. **D - Princípio da Inversão de Dependência**: Dependência em abstrações, não em implementações concretas

## Instalação e Execução

### Requisitos

- Python 3.10+
- pip

### Configuração

1. Clone o repositório
2. Crie e ative o ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```
   pip install fastapi uvicorn sqlalchemy pydantic python-dotenv alembic
   ```

### Execução

1. Inicie a API:
   ```
   ./start.sh
   ```
2. Acesse a documentação da API em:
   ```
   http://localhost:8000/docs
   ```

### Testes

Execute os testes automatizados:
```
./run_tests.sh
```

## Migração para PostgreSQL

Para migrar de SQLite para PostgreSQL:

1. Atualize as configurações no arquivo `.env`:
   ```
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   POSTGRES_DB=perfumes_db
   ```
2. Execute as migrações do Alembic:
   ```
   alembic upgrade head
   ```

## Endpoints da API

### Categorias
- `GET /api/v1/categorias/`: Lista todas as categorias
- `GET /api/v1/categorias/{id}`: Obtém uma categoria específica
- `POST /api/v1/categorias/`: Cria uma nova categoria
- `PUT /api/v1/categorias/{id}`: Atualiza uma categoria
- `DELETE /api/v1/categorias/{id}`: Remove uma categoria

### Produtos
- `GET /api/v1/produtos/`: Lista todos os produtos
- `GET /api/v1/produtos/destaques`: Lista produtos em destaque
- `GET /api/v1/produtos/categoria/{id}`: Lista produtos por categoria
- `GET /api/v1/produtos/{id}`: Obtém um produto específico
- `POST /api/v1/produtos/`: Cria um novo produto
- `PUT /api/v1/produtos/{id}`: Atualiza um produto
- `DELETE /api/v1/produtos/{id}`: Remove um produto

### Quiz
- `GET /api/v1/quiz/perguntas/`: Lista todas as perguntas
- `GET /api/v1/quiz/opcoes/pergunta/{id}`: Lista opções de uma pergunta
- `GET /api/v1/quiz/resultados/`: Lista todos os resultados
- `POST /api/v1/quiz/processar`: Processa respostas e retorna resultado

### Contatos
- `GET /api/v1/contatos/`: Lista todos os contatos
- `GET /api/v1/contatos/nao-respondidos`: Lista contatos não respondidos
- `POST /api/v1/contatos/`: Cria um novo contato
- `PUT /api/v1/contatos/{id}/marcar-respondido`: Marca contato como respondido

### Usuários
- `POST /api/v1/usuarios/token`: Obtém token de autenticação
- `GET /api/v1/usuarios/me`: Obtém informações do usuário atual
- `POST /api/v1/usuarios/`: Cria um novo usuário

## Inicialização de Dados

Para inicializar o banco de dados com dados de exemplo:
```
curl -X POST http://localhost:8000/init-db
```
# boutique_da_rai_api
