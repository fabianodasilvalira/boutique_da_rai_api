#!/bin/bash

# Script para executar os testes da API de Perfumes

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar a API em background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Aguardar a API iniciar
echo "Aguardando a API iniciar..."
sleep 5

# Executar os testes
echo "Executando testes..."
python tests/test_api.py

# Encerrar a API
echo "Encerrando a API..."
kill $API_PID
