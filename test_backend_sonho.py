#!/usr/bin/env python3
import requests
import json

# Teste com trecho que contém "sonho" em estrofes específicas
test_text = """CANTO II
56
Sonhos que a alma enleva e o coração aflige
57
E que às vezes nos fazem despertar
58
Com lágrimas nos olhos, e às vezes
59
Nos fazem rir, e às vezes chorar
60
E que às vezes nos fazem sonhar
61
Com coisas que nunca hão de ser
62
E que às vezes nos fazem dormir
63
E que às vezes nos fazem acordar

CANTO VIII
47
Sonhos proféticos que o futuro mostram
48
E que às vezes nos fazem temer
49
E que às vezes nos fazem esperar
50
E que às vezes nos fazem crer
51
E que às vezes nos fazem duvidar"""

payload = {
    "text": test_text,
    "mode": "estrito"
}

print("=== TESTANDO BACKEND COM TEXTO CONTENDO SONHO ===")
print(f"Texto enviado: {test_text[:100]}...")
print()

try:
    response = requests.post(
        "http://localhost:5000/api/analysis/complete-analysis",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("=== RESPOSTA DO BACKEND ===")
        print(f"Status: {response.status_code}")
        print(f"Total de ocorrências: {data['results']['aggregate']['semantic_expansion']['terms_found']}")
        print(f"Cantos identificados: {data['results']['aggregate']['cantos_identified']}")
        print()
        
        print("=== RESULTADOS POR CANTO ===")
        for canto, info in data['results']['by_canto'].items():
            stanzas = info.get('stanzas', [])
            terms_found = info.get('semantic_expansion', {}).get('terms_found', 0)
            print(f"{canto}: {terms_found} ocorrências nas estrofes {stanzas}")
            
            # Mostrar contextos encontrados
            contexts = info.get('dream_contexts', [])
            for ctx in contexts[:3]:  # Primeiros 3 contextos
                stanza = ctx.get('stanza', 'N/A')
                sentence = ctx.get('sentence', '')[:50]
                print(f"  Estrofe {stanza}: {sentence}...")
        
        print()
        print("=== CLASSIFICAÇÃO ===")
        classification = data['results']['aggregate']['context_classification']
        for category, count in classification.items():
            print(f"{category}: {count}")
            
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Erro na requisição: {e}")
