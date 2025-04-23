"""
Script para configurar o Alembic para migrações de banco de dados
"""
import os
from pathlib import Path

# Criar diretório para migrações
Path("perfumes_api/migrations").mkdir(parents=True, exist_ok=True)
Path("perfumes_api/migrations/versions").mkdir(parents=True, exist_ok=True)

# Criar arquivo de configuração do Alembic
alembic_ini = """# alembic.ini
[alembic]
script_location = migrations
prepend_sys_path = .

# Configuração para SQLite (desenvolvimento)
# sqlalchemy.url = sqlite:///./perfumes.db

# Configuração para PostgreSQL (produção)
# A URL será definida dinamicamente no env.py

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""

# Criar arquivo env.py para Alembic
env_py = """import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.models.models import Base as ModelsBase
from app.models.imagem import Imagem

# Combine all metadata
target_metadata = ModelsBase.metadata

# Import configurações
from app.core.config import settings

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    if settings.USE_POSTGRES:
        return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    else:
        return settings.DATABASE_URL


def run_migrations_offline():
    \"\"\"Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    \"\"\"
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    \"\"\"Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    \"\"\"
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

# Criar arquivo script.py.mako para Alembic
script_mako = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
"""

# Escrever arquivos
with open("perfumes_api/alembic.ini", "w") as f:
    f.write(alembic_ini)

with open("perfumes_api/migrations/env.py", "w") as f:
    f.write(env_py)

Path("perfumes_api/migrations/script.py.mako").write_text(script_mako)

# Criar primeira migração
initial_migration = """\"\"\"Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2023-04-23

\"\"\"
from alembic import op
import sqlalchemy as sa
import json

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Categorias
    op.create_table('categorias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('descricao', sa.String(length=255), nullable=True),
        sa.Column('imagem_url', sa.String(length=255), nullable=True),
        sa.Column('slug', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categorias_id'), 'categorias', ['id'], unique=False)
    op.create_index(op.f('ix_categorias_slug'), 'categorias', ['slug'], unique=True)

    # Produtos
    op.create_table('produtos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('descricao', sa.String(length=255), nullable=True),
        sa.Column('preco', sa.Float(), nullable=False),
        sa.Column('imagem_url', sa.String(length=255), nullable=True),
        sa.Column('categoria_id', sa.Integer(), nullable=True),
        sa.Column('destaque', sa.Boolean(), nullable=True),
        sa.Column('estoque', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['categoria_id'], ['categorias.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_produtos_id'), 'produtos', ['id'], unique=False)

    # Quiz Perguntas
    op.create_table('quiz_perguntas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pergunta', sa.String(length=255), nullable=False),
        sa.Column('ordem', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_perguntas_id'), 'quiz_perguntas', ['id'], unique=False)

    # Quiz Opções
    op.create_table('quiz_opcoes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pergunta_id', sa.Integer(), nullable=True),
        sa.Column('texto', sa.String(length=255), nullable=False),
        sa.Column('valor_id', sa.String(length=50), nullable=False),
        sa.Column('imagem_url', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['pergunta_id'], ['quiz_perguntas.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_opcoes_id'), 'quiz_opcoes', ['id'], unique=False)

    # Quiz Resultados
    op.create_table('quiz_resultados',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('descricao', sa.String(length=255), nullable=True),
        sa.Column('recomendacao', sa.String(length=255), nullable=True),
        sa.Column('imagem_url', sa.String(length=255), nullable=True),
        sa.Column('produto_recomendado_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['produto_recomendado_id'], ['produtos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_resultados_id'), 'quiz_resultados', ['id'], unique=False)

    # Quiz Regras
    op.create_table('quiz_regras',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('combinacao_respostas', sa.JSON(), nullable=True),
        sa.Column('resultado_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['resultado_id'], ['quiz_resultados.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_regras_id'), 'quiz_regras', ['id'], unique=False)

    # Contatos
    op.create_table('contatos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('telefone', sa.String(length=20), nullable=True),
        sa.Column('assunto', sa.String(length=100), nullable=True),
        sa.Column('mensagem', sa.Text(), nullable=False),
        sa.Column('respondido', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contatos_id'), 'contatos', ['id'], unique=False)

    # Usuários
    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('ultimo_acesso', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)

    # Imagens
    op.create_table('imagens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('filepath', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('content_type', sa.String(length=100), nullable=False),
        sa.Column('entidade_tipo', sa.String(length=50), nullable=False),
        sa.Column('entidade_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_imagens_id'), 'imagens', ['id'], unique=False)
    op.create_index(op.f('ix_imagens_filename'), 'imagens', ['filename'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_imagens_filename'), table_name='imagens')
    op.drop_index(op.f('ix_imagens_id'), table_name='imagens')
    op.drop_table('imagens')
    
    op.drop_index(op.f('ix_usuarios_id'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_table('usuarios')
    
    op.drop_index(op.f('ix_contatos_id'), table_name='contatos')
    op.drop_table('contatos')
    
    op.drop_index(op.f('ix_quiz_regras_id'), table_name='quiz_regras')
    op.drop_table('quiz_regras')
    
    op.drop_index(op.f('ix_quiz_resultados_id'), table_name='quiz_resultados')
    op.drop_table('quiz_resultados')
    
    op.drop_index(op.f('ix_quiz_opcoes_id'), table_name='quiz_opcoes')
    op.drop_table('quiz_opcoes')
    
    op.drop_index(op.f('ix_quiz_perguntas_id'), table_name='quiz_perguntas')
    op.drop_table('quiz_perguntas')
    
    op.drop_index(op.f('ix_produtos_id'), table_name='produtos')
    op.drop_table('produtos')
    
    op.drop_index(op.f('ix_categorias_slug'), table_name='categorias')
    op.drop_index(op.f('ix_categorias_id'), table_name='categorias')
    op.drop_table('categorias')
"""

# Criar diretório de versões e salvar a migração inicial
os.makedirs("perfumes_api/migrations/versions", exist_ok=True)
with open("perfumes_api/migrations/versions/001_initial.py", "w") as f:
    f.write(initial_migration)

print("Configuração do Alembic concluída com sucesso!")
