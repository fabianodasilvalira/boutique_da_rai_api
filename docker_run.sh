#!/bin/bash

# Script para executar a aplicação usando Docker

# Construir e iniciar os containers
echo "Iniciando os containers..."
docker-compose up -d

# Aguardar o banco de dados iniciar
echo "Aguardando o banco de dados iniciar..."
sleep 10

# Executar as migrações do Alembic
echo "Aplicando migrações do banco de dados..."
docker-compose exec api alembic upgrade head

# Inicializar dados de exemplo (opcional)
echo "Deseja inicializar o banco de dados com dados de exemplo? (s/n)"
read resposta
if [ "$resposta" = "s" ]; then
    echo "Inicializando dados de exemplo..."
    docker-compose exec api python -c "import requests; requests.post('http://localhost:8000/init-db')"
fi

echo "Aplicação iniciada com sucesso!"
echo "A API está disponível em: http://localhost:8000"
echo "Documentação da API: http://localhost:8000/docs"
