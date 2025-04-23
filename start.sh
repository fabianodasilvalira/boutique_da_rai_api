#!/bin/bash

# Script para iniciar a API de Perfumes

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar a API
echo "Iniciando a API de Perfumes..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
