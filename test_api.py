#!/usr/bin/env python3
"""
Teste direto da API
"""

import requests
import json

# Teste com texto que contém "sonho"
test_text = """
O sonho divino da glória portuguesa revelou-se em visões proféticas.
O sonho de Dom Manuel foi uma visão sagrada que legitimou a expansão marítima.
As visões proféticas mostraram o destino glorioso de Portugal.
"""

def test_api():
    try:
        # Teste 1: Health check
        print("=== TESTE 1: Health Check ===")
        response = requests.get("http://localhost:5000/api/analysis/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Teste 2: Análise completa
        print("=== TESTE 2: Análise Completa ===")
        data = {"text": test_text}
        response = requests.post(
            "http://localhost:5000/api/analysis/complete-analysis",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Análise realizada com sucesso!")
            print(f"Resultados: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar com o backend")
        print("Verifique se o backend está rodando em http://localhost:5000")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_api()
