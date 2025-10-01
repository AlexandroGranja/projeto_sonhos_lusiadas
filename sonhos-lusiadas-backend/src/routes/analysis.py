#!/usr/bin/env python3
"""
Rotas de análise do backend Sonhos Lusíadas
"""

import os
import sys
import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import json

# Importar bibliotecas para processamento de arquivos
try:
    import docx2txt
    DOCX2TXT_AVAILABLE = True
    print("✅ docx2txt disponível para processamento de arquivos .doc")
except ImportError:
    DOCX2TXT_AVAILABLE = False
    print("⚠️ docx2txt não disponível - arquivos .doc podem não funcionar")

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria blueprint
analysis_bp = Blueprint('analysis', __name__)

# Configuração de upload
ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """Verifica se a API está funcionando."""
    return jsonify({
        'status': 'ok',
        'message': 'API de análise funcionando!',
        'version': '1.0.0'
    })

@analysis_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload de arquivo para análise."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Processar arquivos Word
            content = ""
            if filename.endswith('.docx'):
                try:
                    import zipfile
                    import xml.etree.ElementTree as ET
                    
                    # DOCX é um arquivo ZIP
                    with zipfile.ZipFile(filepath, 'r') as docx:
                        # Ler o documento principal
                        document = docx.read('word/document.xml')
                        root = ET.fromstring(document)
                        
                        # Extrair texto de todos os parágrafos
                        for paragraph in root.iter():
                            if paragraph.text:
                                content += paragraph.text + " "
                            if paragraph.tail:
                                content += paragraph.tail + " "
                                
                    content = content.strip()
                    print(f"DEBUG: Conteúdo DOCX extraído: {content[:200]}...")
                    
                except Exception as e:
                    print(f"Erro ao processar DOCX: {e}")
                    content = "Erro ao processar arquivo DOCX"
                    
            elif filename.endswith('.doc'):
                if DOCX2TXT_AVAILABLE:
                    try:
                        print("DEBUG: Processando arquivo .doc com docx2txt...")
                        content = docx2txt.process(filepath)
                        content = content.strip()
                        print(f"DEBUG: Conteúdo DOC extraído: {content[:200]}...")
                        
                    except Exception as e:
                        print(f"Erro ao processar DOC com docx2txt: {e}")
                        content = f"Erro ao processar arquivo DOC: {str(e)}"
                else:
                    print("docx2txt não disponível, tentando método alternativo...")
                    try:
                        # Método alternativo para .doc
                        import subprocess
                        
                        # Tentar usar antiword se disponível
                        result = subprocess.run(['antiword', filepath], 
                                             capture_output=True, text=True, timeout=30)
                        if result.returncode == 0:
                            content = result.stdout.strip()
                            print(f"DEBUG: Conteúdo DOC extraído com antiword: {content[:200]}...")
                        else:
                            content = "Erro: antiword não disponível para processar arquivo .doc"
                            
                    except Exception as e:
                        print(f"Erro ao processar DOC: {e}")
                        content = "Erro ao processar arquivo DOC - formato não suportado"
                    
            elif filename.endswith('.txt'):
                # Para arquivos .txt, ler diretamente
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(f"DEBUG: Conteúdo TXT lido: {content[:200]}...")
                except Exception as e:
                    print(f"Erro ao ler TXT: {e}")
                    content = f"Erro ao ler arquivo TXT: {str(e)}"
            
            return jsonify({
                'message': 'Arquivo processado com sucesso',
                'filename': filename,
                'filepath': filepath,
                'content': content,
                'content_length': len(content)
            })
        else:
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
            
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/preprocess', methods=['POST'])
def preprocess_text():
    """Pré-processa texto para análise."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texto não fornecido'}), 400
        
        # Simulação de pré-processamento
        processed_text = text.lower().strip()
        
        return jsonify({
            'message': 'Texto pré-processado com sucesso',
            'processed_text': processed_text,
            'length': len(processed_text)
        })
        
    except Exception as e:
        logger.error(f"Erro no pré-processamento: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/expand-semantic', methods=['POST'])
def expand_semantic():
    """Expansão semântica de vocabulário."""
    try:
        data = request.get_json()
        context = data.get('context', 'Os Lusíadas de Camões')
        
        # Simulação de expansão semântica
        expanded_words = [
            'sonho', 'pesadelo', 'visão', 'sombra', 'glória',
            'fantasia', 'ilusão', 'devaneio', 'quimera', 'miragem',
            'aparição', 'revelação', 'profecia', 'presságio', 'augúrio'
        ]
        
        return jsonify({
            'message': 'Expansão semântica realizada',
            'context': context,
            'expanded_words': expanded_words,
            'count': len(expanded_words)
        })
        
    except Exception as e:
        logger.error(f"Erro na expansão semântica: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/analyze-contexts', methods=['POST'])
def analyze_contexts():
    """Análise de contextos no texto."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        words = data.get('words', [])
        
        if not text or not words:
            return jsonify({'error': 'Texto e palavras são obrigatórios'}), 400
        
        # Simulação de análise de contextos
        contexts = []
        for word in words:
            if word in text.lower():
                contexts.append({
                    'word': word,
                    'context': f"Contexto encontrado para '{word}'",
                    'type': 'onírico',
                    'confidence': 0.85
                })
        
        return jsonify({
            'message': 'Análise de contextos realizada',
            'contexts': contexts,
            'total': len(contexts)
        })
        
    except Exception as e:
        logger.error(f"Erro na análise de contextos: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/visualize', methods=['POST'])
def generate_visualizations():
    """Gera visualizações dos dados."""
    try:
        data = request.get_json()
        
        # Simulação de geração de visualizações
        visualizations = {
            'word_frequency': {
                'type': 'bar',
                'data': [{'word': 'sonho', 'count': 15}, {'word': 'visão', 'count': 8}]
            },
            'context_types': {
                'type': 'pie',
                'data': [{'type': 'onírico', 'count': 10}, {'type': 'profético', 'count': 5}]
            }
        }
        
        return jsonify({
            'message': 'Visualizações geradas com sucesso',
            'visualizations': visualizations
        })
        
    except Exception as e:
        logger.error(f"Erro na geração de visualizações: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/download', methods=['GET'])
def download_results():
    """Download dos resultados da análise."""
    try:
        filename = request.args.get('filename', 'results.json')
        
        # Simulação de download
        results = {
            'analysis_date': '2024-09-30',
            'total_words': 1000,
            'dream_contexts': 25,
            'visualizations': 3
        }
        
        return jsonify({
            'message': 'Download disponível',
            'filename': filename,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Erro no download: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Dicionário expandido de termos relacionados
EXPANDED_TERMS = {
    'onírico': [
        'sonho', 'sonhar', 'sonhador', 'sonhante', 'sonhoso',
        'pesadelo', 'pesadelar', 'pesadelante', 'pesadeloso',
        'dormir', 'adormecer', 'despertar', 'desperto',
        'sonolência', 'sonolento', 'sonolentamente',
        'sonambulismo', 'sonambúlico', 'sonambular',
        'insônia', 'insone', 'insoniamente', 'insoniar',
        'soneca', 'sonecar', 'sonecante',
        'repouso', 'repousar', 'repousante',
        'descanso', 'descansar', 'descansante'
    ],
    'profético': [
        'visão', 'visionário', 'visionar', 'visionante',
        'profecia', 'profético', 'profetizar', 'profetizante',
        'revelação', 'revelar', 'revelador', 'revelante',
        'aparição', 'aparecer', 'aparecimento', 'aparente',
        'oráculo', 'oracular', 'oracularmente',
        'vaticínio', 'vaticinar', 'vaticinador', 'vaticinante',
        'presságio', 'pressagiar', 'pressagiador',
        'augúrio', 'augurar', 'augurador',
        'predição', 'predizer', 'preditor'
    ],
    'alegórico': [
        'sombra', 'sombreado', 'sombreadamente', 'sombreador',
        'fantasia', 'fantasioso', 'fantasiosamente', 'fantasiar',
        'ilusão', 'ilusório', 'ilusoriamente', 'ilusionar',
        'metáfora', 'metafórico', 'metafóricamente',
        'símbolo', 'simbólico', 'simbolicamente', 'simbolizar',
        'alegoria', 'alegórico', 'alegoricamente', 'alegorizar',
        'emblema', 'emblemático', 'emblematicamente',
        'figura', 'figurado', 'figuradamente', 'figurar',
        'representação', 'representar', 'representante'
    ],
    'divino': [
        'glória', 'glorioso', 'gloriosamente', 'glorificar',
        'divino', 'divinamente', 'divindade', 'divinizar',
        'celestial', 'celestialmente', 'celestialidade',
        'sobrenatural', 'sobrenaturalmente', 'sobrenaturalidade',
        'milagre', 'milagroso', 'milagrosamente', 'milagrar',
        'sagrado', 'sagradamente', 'sacralidade', 'sacralizar',
        'santo', 'santamente', 'santidade', 'santificar',
        'bendito', 'benditamente', 'bendizer',
        'abençoado', 'abençoar', 'abençoador',
        'miraculoso', 'miraculosamente'
    ]
}

def count_expanded_terms(text):
    """Conta termos expandidos no texto."""
    results = {}
    text_lower = text.lower()
    
    print(f"DEBUG: Analisando texto: {text_lower[:100]}...")
    print(f"DEBUG: Tamanho do texto: {len(text_lower)} caracteres")
    
    for category, terms in EXPANDED_TERMS.items():
        results[category] = {}
        total_count = 0
        
        for term in terms:
            count = text_lower.count(term.lower())
            if count > 0:
                results[category][term] = count
                total_count += count
                print(f"DEBUG: Encontrado '{term}': {count} vezes")
        
        results[category]['total'] = total_count
        print(f"DEBUG: {category}: {total_count} termos encontrados")
    
    print(f"DEBUG: Resultado final: {results}")
    return results

def analyze_dream_contexts(text):
    """Analisa contextos de sonhos no texto."""
    # Dividir texto em sentenças
    sentences = text.split('.')
    dream_contexts = []
    
    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        
        # Verificar se contém termos relacionados a sonhos
        dream_terms = []
        for category, terms in EXPANDED_TERMS.items():
            for term in terms:
                if term.lower() in sentence_lower:
                    dream_terms.append({
                        'term': term,
                        'category': category
                    })
        
        if dream_terms:
            dream_contexts.append({
                'sentence': sentence.strip(),
                'position': i,
                'terms': dream_terms,
                'context_type': classify_context_type(dream_terms)
            })
    
    return dream_contexts

def classify_context_type(terms):
    """Classifica o tipo de contexto baseado nos termos encontrados."""
    categories = [term['category'] for term in terms]
    
    if 'divino' in categories:
        return 'divino'
    elif 'profético' in categories:
        return 'profético'
    elif 'alegórico' in categories:
        return 'alegórico'
    else:
        return 'onírico'

def calculate_analysis_metrics(text, results):
    """Calcula métricas de validação da análise."""
    total_words = len(text.split())
    total_dream_terms = sum(category['total'] for category in results['expanded_terms'].values())
    
    return {
        'coverage': total_dream_terms / total_words if total_words > 0 else 0,
        'total_words': total_words,
        'dream_terms_found': total_dream_terms,
        'categories_covered': len([cat for cat in results['expanded_terms'].values() if cat['total'] > 0]),
        'confidence_score': min(95, (total_dream_terms / total_words) * 1000) if total_words > 0 else 0
    }

@analysis_bp.route('/complete-analysis', methods=['POST'])
def complete_analysis():
    """Análise completa do texto com metodologia expandida."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        print(f"DEBUG BACKEND: Texto recebido: {text[:100]}...")
        print(f"DEBUG BACKEND: Tamanho do texto: {len(text)} caracteres")
        
        if not text:
            return jsonify({'error': 'Texto é obrigatório'}), 400
        
        # Análise expandida de termos
        expanded_terms = count_expanded_terms(text)
        
        # Análise de contextos
        dream_contexts = analyze_dream_contexts(text)
        
        # Classificação por tipos
        context_classification = {
            'onírico': len([ctx for ctx in dream_contexts if ctx['context_type'] == 'onírico']),
            'profético': len([ctx for ctx in dream_contexts if ctx['context_type'] == 'profético']),
            'alegórico': len([ctx for ctx in dream_contexts if ctx['context_type'] == 'alegórico']),
            'divino': len([ctx for ctx in dream_contexts if ctx['context_type'] == 'divino'])
        }
        
        # Processamento do texto
        preprocessing = {
            'original_length': len(text),
            'processed_length': len(text.lower().strip()),
            'sentences': text.count('.') + text.count('!') + text.count('?'),
            'words': len(text.split()),
            'unique_words': len(set(text.lower().split()))
        }
        
        # Resultados completos
        results = {
            'preprocessing': preprocessing,
            'expanded_terms': expanded_terms,
            'dream_contexts': dream_contexts,
            'context_classification': context_classification,
            'semantic_expansion': {
                'total_categories': len(EXPANDED_TERMS),
                'total_terms_searched': sum(len(terms) for terms in EXPANDED_TERMS.values()),
                'terms_found': sum(cat['total'] for cat in expanded_terms.values()),
                'coverage_percentage': (sum(cat['total'] for cat in expanded_terms.values()) / preprocessing['words']) * 100
            },
            'visualizations': {
                'word_frequency': True,
                'context_distribution': True,
                'dream_types': True,
                'expanded_analysis': True
            }
        }
        
        # Métricas de validação
        metrics = calculate_analysis_metrics(text, results)
        results['validation_metrics'] = metrics
        
        return jsonify({
            'message': 'Análise expandida realizada com sucesso',
            'results': results,
            'methodology': {
                'name': 'Análise Semântica Expandida dos Lusíadas',
                'version': '2.0',
                'description': 'Metodologia completa para análise de temas oníricos com expansão semântica',
                'categories_analyzed': list(EXPANDED_TERMS.keys()),
                'total_terms': sum(len(terms) for terms in EXPANDED_TERMS.values())
            }
        })
        
    except Exception as e:
        logger.error(f"Erro na análise completa: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500