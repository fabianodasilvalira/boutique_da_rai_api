# Modelos de Banco de Dados para Backend da Landing Page de Perfumes

## Entidades Identificadas

Após análise da landing page, foram identificadas as seguintes entidades principais:

1. **Categorias de Produtos**
2. **Produtos**
3. **Perguntas do Quiz**
4. **Opções de Respostas do Quiz**
5. **Resultados do Quiz**
6. **Mensagens de Contato**

## Modelagem de Dados

### 1. Categoria
```
- id: Integer (PK)
- nome: String
- descricao: String
- imagem_url: String
- slug: String
```

### 2. Produto
```
- id: Integer (PK)
- nome: String
- descricao: String
- preco: Decimal
- imagem_url: String
- categoria_id: Integer (FK)
- destaque: Boolean
- estoque: Integer
- data_criacao: DateTime
- data_atualizacao: DateTime
```

### 3. QuizPergunta
```
- id: Integer (PK)
- pergunta: String
- ordem: Integer
```

### 4. QuizOpcao
```
- id: Integer (PK)
- pergunta_id: Integer (FK)
- texto: String
- valor_id: String
- imagem_url: String (opcional)
```

### 5. QuizResultado
```
- id: Integer (PK)
- nome: String
- descricao: String
- recomendacao: String
- imagem_url: String
- produto_recomendado_id: Integer (FK, opcional)
```

### 6. QuizRegra
```
- id: Integer (PK)
- combinacao_respostas: JSON
- resultado_id: Integer (FK)
```

### 7. Contato
```
- id: Integer (PK)
- nome: String
- email: String
- telefone: String
- assunto: String
- mensagem: Text
- data_envio: DateTime
- respondido: Boolean
```

### 8. Usuario (para autenticação de administração)
```
- id: Integer (PK)
- nome: String
- email: String
- senha_hash: String
- ativo: Boolean
- data_criacao: DateTime
- ultimo_acesso: DateTime
```

## Relacionamentos

1. **Categoria -> Produto**: Uma categoria pode ter vários produtos (1:N)
2. **QuizPergunta -> QuizOpcao**: Uma pergunta pode ter várias opções (1:N)
3. **QuizResultado -> Produto**: Um resultado pode recomendar um produto específico (N:1)
4. **QuizRegra -> QuizResultado**: Uma regra determina um resultado (N:1)

## Considerações para Migração SQLite -> PostgreSQL

1. **Tipos de Dados**:
   - SQLite não tem tipos específicos para data/hora, usar TEXT para armazenar no formato ISO
   - Para migração para PostgreSQL, converter para tipos nativos (TIMESTAMP, DATE)

2. **Chaves Estrangeiras**:
   - Habilitar suporte a chaves estrangeiras no SQLite com PRAGMA foreign_keys = ON
   - PostgreSQL tem suporte nativo a chaves estrangeiras

3. **JSON**:
   - SQLite armazenará JSON como TEXT
   - PostgreSQL tem suporte nativo a tipo JSONB para melhor performance

4. **Índices**:
   - Criar índices para campos frequentemente consultados
   - PostgreSQL oferece tipos adicionais de índices (GIN, GIST) para consultas específicas

5. **Transações**:
   - Implementar suporte a transações para garantir integridade dos dados
   - Ambos SQLite e PostgreSQL suportam transações ACID
