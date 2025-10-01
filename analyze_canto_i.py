#!/usr/bin/env python3
"""
Análise do Canto I de Os Lusíadas
"""

import sys
import os
sys.path.append('sonhos-lusiadas-backend/src')

from preprocessing import extract_canto
from search_analysis import run_complete_analysis
from semantic_expansion import SemanticExpander

def main():
    print("=== ANÁLISE DO CANTO I DE OS LUSÍADAS ===\n")
    
    # Carrega o texto
    try:
        with open('data/raw/os_lusiadas.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        print("✅ Texto carregado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao carregar texto: {e}")
        return
    
    # Extrai o Canto I
    try:
        canto_i = extract_canto(text, 1)
        print(f"✅ Canto I extraído - {len(canto_i)} caracteres")
        print(f"\n--- PRIMEIROS 500 CARACTERES DO CANTO I ---")
        print(canto_i[:500] + "...")
    except Exception as e:
        print(f"❌ Erro ao extrair Canto I: {e}")
        return
    
    # Inicializa o expansor semântico
    try:
        expander = SemanticExpander()
        expanded_terms = expander.get_comprehensive_expansion()
        print(f"\n✅ Termos semânticos expandidos - {len(expanded_terms['combined_expansion'])} palavras")
        
        print(f"\n--- PALAVRAS-CHAVE SEMENTE ---")
        print(", ".join(expander.seed_words))
        
        print(f"\n--- EXPANSÃO COMBINADA (primeiras 20) ---")
        print(", ".join(expanded_terms['combined_expansion'][:20]))
        
    except Exception as e:
        print(f"❌ Erro na expansão semântica: {e}")
        return
    
    # Executa análise
    try:
        print(f"\n=== EXECUTANDO ANÁLISE COMPLETA ===")
        results = run_complete_analysis(canto_i, expanded_terms['combined_expansion'])
        
        print(f"\n--- RESULTADOS DA ANÁLISE ---")
        print(f"Total de palavras analisadas: {len(expanded_terms['combined_expansion'])}")
        print(f"Contextos encontrados: {len(results.get('contexts', []))}")
        print(f"Padrões encontrados: {len(results.get('patterns', []))}")
        
        # Mostra contextos encontrados
        if results.get('contexts'):
            print(f"\n--- CONTEXTOS DE SONHO ENCONTRADOS ---")
            for i, context in enumerate(results['contexts'][:5], 1):
                print(f"{i}. {context}")
        
        # Mostra padrões encontrados
        if results.get('patterns'):
            print(f"\n--- PADRÕES ENCONTRADOS ---")
            for pattern in results['patterns'][:5]:
                print(f"- {pattern}")
                
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        return

if __name__ == "__main__":
    main()
