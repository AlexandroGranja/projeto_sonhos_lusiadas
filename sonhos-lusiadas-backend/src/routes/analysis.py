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

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria blueprint
analysis_bp = Blueprint('analysis', __name__)

# Configuração de upload
ALLOWED_EXTENSIONS = {'txt', 'docx', 'pdf'}
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
            
            return jsonify({
                'message': 'Arquivo enviado com sucesso',
                'filename': filename,
                'filepath': filepath
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

@analysis_bp.route('/complete-analysis', methods=['POST'])
def complete_analysis():
    """Análise completa do texto."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texto é obrigatório'}), 400
        
        # Simulação de análise completa
        results = {
            'preprocessing': {
                'original_length': len(text),
                'processed_length': len(text.lower().strip()),
                'sentences': text.count('.') + text.count('!') + text.count('?')
            },
            'semantic_expansion': {
                'seed_words': 5,
                'expanded_words': 15,
                'total_vocabulary': 20
            },
            'context_analysis': {
                'total_contexts': 8,
                'onírico': 3,
                'profético': 2,
                'alegórico': 3
            },
            'visualizations': {
                'word_frequency': True,
                'context_distribution': True,
                'dream_types': True
            }
        }
        
        return jsonify({
            'message': 'Análise completa realizada com sucesso',
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Erro na análise completa: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500