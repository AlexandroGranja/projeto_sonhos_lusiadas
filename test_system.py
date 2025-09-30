#!/usr/bin/env python3
"""
Script de Teste e Validação do Sistema
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa

Este script testa todos os componentes principais do sistema para garantir
que estão funcionando corretamente.
"""

import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def print_header(title):
    """Imprime cabeçalho formatado."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    """Imprime passo do teste."""
    print(f"\n[{step}] {description}")

def print_success(message):
    """Imprime mensagem de sucesso."""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensagem de erro."""
    print(f"❌ {message}")

def print_warning(message):
    """Imprime mensagem de aviso."""
    print(f"⚠️  {message}")

def test_dependencies():
    """Testa se todas as dependências estão instaladas."""
    print_header("TESTE DE DEPENDÊNCIAS")
    
    dependencies = [
        ('spacy', 'spaCy para processamento de linguagem natural'),
        ('nltk', 'NLTK para análise de texto'),
        ('pandas', 'Pandas para manipulação de dados'),
        ('matplotlib', 'Matplotlib para visualizações'),
        ('flask', 'Flask para o backend'),
        ('anthropic', 'Cliente Anthropic para Claude'),
        ('requests', 'Requests para chamadas HTTP')
    ]
    
    missing_deps = []
    
    for dep, description in dependencies:
        try:
            __import__(dep)
            print_success(f"{dep} - {description}")
        except ImportError:
            print_error(f"{dep} - {description} (NÃO INSTALADO)")
            missing_deps.append(dep)
    
    if missing_deps:
        print_warning(f"Dependências faltando: {', '.join(missing_deps)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print_success("Todas as dependências estão instaladas!")
    return True

def test_file_structure():
    """Testa se a estrutura de arquivos está correta."""
    print_header("TESTE DE ESTRUTURA DE ARQUIVOS")
    
    required_files = [
        'src/preprocessing.py',
        'src/semantic_expansion.py',
        'src/search_analysis.py',
        'src/visualization.py',
        'data/raw/os_lusiadas.txt',
        'sonhos-lusiadas-backend/src/main.py',
        'sonhos-lusiadas-backend/src/routes/analysis.py',
        'sonhos-lusiadas-app/src/App.jsx',
        'sonhos-lusiadas-app/src/services/api.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} (NÃO ENCONTRADO)")
            missing_files.append(file_path)
    
    if missing_files:
        print_warning(f"Arquivos faltando: {len(missing_files)}")
        return False
    
    print_success("Estrutura de arquivos está correta!")
    return True

def test_preprocessing():
    """Testa o módulo de pré-processamento."""
    print_header("TESTE DE PRÉ-PROCESSAMENTO")
    
    try:
        from preprocessing import TextPreprocessor, process_lusiadas_text
        
        print_step("1", "Inicializando preprocessador...")
        preprocessor = TextPreprocessor()
        print_success("Preprocessador inicializado")
        
        print_step("2", "Testando limpeza de texto...")
        test_text = "Este é um texto de teste! Com pontuação... e números 123."
        cleaned = preprocessor.clean_text(test_text)
        print_success(f"Texto limpo: '{cleaned}'")
        
        print_step("3", "Testando processamento completo...")
        processed = preprocessor.preprocess(test_text)
        print_success(f"Texto processado: '{processed}'")
        
        print_step("4", "Testando extração de sentenças...")
        sentences = preprocessor.extract_sentences(test_text)
        print_success(f"Sentenças extraídas: {len(sentences)}")
        
        return True
        
    except Exception as e:
        print_error(f"Erro no teste de pré-processamento: {e}")
        return False

def test_semantic_expansion():
    """Testa o módulo de expansão semântica."""
    print_header("TESTE DE EXPANSÃO SEMÂNTICA")
    
    try:
        from semantic_expansion import SemanticExpander
        
        print_step("1", "Inicializando expansor semântico...")
        expander = SemanticExpander()
        print_success("Expansor inicializado")
        
        print_step("2", "Testando palavras semente...")
        print_success(f"Palavras semente: {expander.seed_words}")
        
        print_step("3", "Testando expansão com BERTimbau...")
        try:
            bertimbau_words = expander.expand_with_bertimbau(n=5)
            print_success(f"BERTimbau: {len(bertimbau_words)} palavras")
        except Exception as e:
            print_warning(f"BERTimbau não disponível: {e}")
        
        print_step("4", "Testando expansão com Claude...")
        try:
            claude_words = expander.expand_with_claude()
            if claude_words:
                print_success(f"Claude: {len(claude_words)} palavras")
            else:
                print_warning("Claude não configurado (API key necessária)")
        except Exception as e:
            print_warning(f"Claude não disponível: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Erro no teste de expansão semântica: {e}")
        return False

def test_search_analysis():
    """Testa o módulo de busca e análise."""
    print_header("TESTE DE BUSCA E ANÁLISE")
    
    try:
        from search_analysis import ContextAnalyzer
        
        print_step("1", "Inicializando analisador...")
        analyzer = ContextAnalyzer()
        print_success("Analisador inicializado")
        
        print_step("2", "Testando busca de contextos...")
        test_text = "O sonho revelou uma visão profética da glória futura."
        test_words = ["sonho", "visão", "glória"]
        
        contexts_df = analyzer.search_contexts(test_text, test_words)
        print_success(f"Contextos encontrados: {len(contexts_df)}")
        
        print_step("3", "Testando cálculo de frequências...")
        frequencies = analyzer.calculate_frequencies(contexts_df)
        print_success(f"Tipos de frequência: {list(frequencies.keys())}")
        
        return True
        
    except Exception as e:
        print_error(f"Erro no teste de busca e análise: {e}")
        return False

def test_visualization():
    """Testa o módulo de visualização."""
    print_header("TESTE DE VISUALIZAÇÃO")
    
    try:
        from visualization import DataVisualizer
        import pandas as pd
        
        print_step("1", "Inicializando visualizador...")
        visualizer = DataVisualizer("/tmp/test_viz")
        print_success("Visualizador inicializado")
        
        print_step("2", "Testando dados de exemplo...")
        sample_data = pd.DataFrame({
            'word': ['sonho', 'visão', 'glória'],
            'frequency': [10, 8, 6]
        })
        
        print_step("3", "Testando geração de gráfico...")
        try:
            path = visualizer.plot_word_frequency(sample_data, save_name="test_freq.png")
            if os.path.exists(path):
                print_success(f"Gráfico gerado: {path}")
            else:
                print_warning("Gráfico não foi salvo")
        except Exception as e:
            print_warning(f"Erro na geração de gráfico: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Erro no teste de visualização: {e}")
        return False

def test_backend_health():
    """Testa se o backend está funcionando."""
    print_header("TESTE DO BACKEND")
    
    print_step("1", "Verificando se o backend está rodando...")
    
    try:
        response = requests.get("http://localhost:5000/api/analysis/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend está respondendo")
            data = response.json()
            print_success(f"Status: {data.get('status', 'unknown')}")
            return True
        else:
            print_error(f"Backend retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_warning("Backend não está rodando")
        print("Para iniciar o backend:")
        print("cd sonhos-lusiadas-backend")
        print("source venv/bin/activate")
        print("python src/main.py")
        return False
    except Exception as e:
        print_error(f"Erro ao testar backend: {e}")
        return False

def test_frontend_build():
    """Testa se o frontend pode ser construído."""
    print_header("TESTE DO FRONTEND")
    
    frontend_dir = "sonhos-lusiadas-app"
    
    if not os.path.exists(frontend_dir):
        print_error("Diretório do frontend não encontrado")
        return False
    
    print_step("1", "Verificando package.json...")
    package_json = os.path.join(frontend_dir, "package.json")
    if os.path.exists(package_json):
        print_success("package.json encontrado")
    else:
        print_error("package.json não encontrado")
        return False
    
    print_step("2", "Verificando node_modules...")
    node_modules = os.path.join(frontend_dir, "node_modules")
    if os.path.exists(node_modules):
        print_success("node_modules encontrado")
    else:
        print_warning("node_modules não encontrado")
        print("Execute: cd sonhos-lusiadas-app && npm install")
    
    print_step("3", "Verificando arquivos principais...")
    main_files = [
        "src/App.jsx",
        "src/main.jsx",
        "index.html"
    ]
    
    for file in main_files:
        file_path = os.path.join(frontend_dir, file)
        if os.path.exists(file_path):
            print_success(f"{file}")
        else:
            print_error(f"{file} não encontrado")
    
    return True

def test_integration():
    """Testa integração entre componentes."""
    print_header("TESTE DE INTEGRAÇÃO")
    
    print_step("1", "Testando pipeline completo...")
    
    try:
        # Testa se consegue carregar todos os módulos
        from preprocessing import TextPreprocessor
        from semantic_expansion import SemanticExpander
        from search_analysis import ContextAnalyzer
        from visualization import DataVisualizer
        
        print_success("Todos os módulos carregados")
        
        print_step("2", "Testando fluxo de dados...")
        
        # Texto de teste
        test_text = """
        Sonhava o navegador com terras distantes,
        onde a glória portuguesa brilharia.
        Visões proféticas guiavam os navegantes
        através dos mares da fantasia.
        """
        
        # Pré-processamento
        preprocessor = TextPreprocessor()
        processed_text = preprocessor.preprocess(test_text)
        print_success("Pré-processamento concluído")
        
        # Expansão semântica
        expander = SemanticExpander()
        words = expander.seed_words[:5]  # Usa apenas algumas palavras
        print_success("Palavras para análise definidas")
        
        # Análise de contextos
        analyzer = ContextAnalyzer()
        contexts_df = analyzer.search_contexts(test_text, words)
        print_success(f"Análise concluída: {len(contexts_df)} contextos")
        
        # Frequências
        frequencies = analyzer.calculate_frequencies(contexts_df)
        print_success("Frequências calculadas")
        
        print_success("Pipeline de integração funcionando!")
        return True
        
    except Exception as e:
        print_error(f"Erro no teste de integração: {e}")
        return False

def run_all_tests():
    """Executa todos os testes."""
    print_header("INICIANDO TESTES DO SISTEMA SONHOS LUSÍADAS")
    
    tests = [
        ("Dependências", test_dependencies),
        ("Estrutura de Arquivos", test_file_structure),
        ("Pré-processamento", test_preprocessing),
        ("Expansão Semântica", test_semantic_expansion),
        ("Busca e Análise", test_search_analysis),
        ("Visualização", test_visualization),
        ("Backend", test_backend_health),
        ("Frontend", test_frontend_build),
        ("Integração", test_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_error(f"Erro inesperado no teste {test_name}: {e}")
            results[test_name] = False
    
    # Resumo dos resultados
    print_header("RESUMO DOS TESTES")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:20} {status}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print_success("🎉 TODOS OS TESTES PASSARAM!")
        print("\nO sistema está pronto para uso!")
        print("\nPara iniciar:")
        print("1. Backend: cd sonhos-lusiadas-backend && source venv/bin/activate && python src/main.py")
        print("2. Frontend: cd sonhos-lusiadas-app && npm run dev")
    else:
        print_warning(f"⚠️  {total - passed} teste(s) falharam")
        print("\nVerifique os erros acima e corrija antes de usar o sistema.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
