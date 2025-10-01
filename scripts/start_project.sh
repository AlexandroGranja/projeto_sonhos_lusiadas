#!/bin/bash

echo "========================================"
echo "  Sonhos Lusíadas - Sistema de Análise"
echo "========================================"
echo

echo "Iniciando backend..."
cd ../sonhos-lusiadas-backend
python src/main.py &
BACKEND_PID=$!

sleep 3

echo
echo "Iniciando frontend..."
cd ../sonhos-lusiadas-app
npm run dev &
FRONTEND_PID=$!

echo
echo "========================================"
echo "  Sistema iniciado com sucesso!"
echo "========================================"
echo
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo
echo "Pressione Ctrl+C para parar os serviços..."

# Função para parar os processos quando o script for interrompido
cleanup() {
    echo
    echo "Parando serviços..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Aguarda indefinidamente
wait
