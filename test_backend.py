#!/usr/bin/env python3
"""
Script de teste para o backend Sonhos Lusíadas
"""

import sys
import os

# Adiciona o diretório do backend ao path
backend_path = os.path.join(os.path.dirname(__file__), 'sonhos-lusiadas-backend', 'src')
sys.path.insert(0, backend_path)

try:
    print("🔍 Testando importações...")
    
    # Testa importação do Flask
    from flask import Flask
    print("✅ Flask importado com sucesso")
    
    # Testa importação dos módulos customizados
    from preprocessing import TextPreprocessor
    print("✅ TextPreprocessor importado com sucesso")
    
    from semantic_expansion import SemanticExpander
    print("✅ SemanticExpander importado com sucesso")
    
    from search_analysis import ContextAnalyzer
    print("✅ ContextAnalyzer importado com sucesso")
    
    from visualization import DataVisualizer
    print("✅ DataVisualizer importado com sucesso")
    
    # Testa criação de instâncias
    print("\n🔧 Testando criação de instâncias...")
    
    preprocessor = TextPreprocessor()
    print("✅ TextPreprocessor criado com sucesso")
    
    expander = SemanticExpander()
    print("✅ SemanticExpander criado com sucesso")
    
    analyzer = ContextAnalyzer()
    print("✅ ContextAnalyzer criado com sucesso")
    
    visualizer = DataVisualizer()
    print("✅ DataVisualizer criado com sucesso")
    
    # Testa processamento básico
    print("\n📝 Testando processamento básico...")
    
    test_text = "Este é um sonho de glória e visão profética."
    processed = preprocessor.preprocess(test_text)
    print(f"✅ Texto processado: {processed}")
    
    # Testa expansão semântica
    expansion = expander.get_comprehensive_expansion()
    print(f"✅ Expansão semântica: {len(expansion['combined_expansion'])} palavras")
    
    print("\n🎉 Todos os testes passaram! O backend está funcionando corretamente.")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    sys.exit(1)
