"""
Rotas da API para análise de textos literários
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa
"""

from flask import Blueprint, request, jsonify, send_file
import os
import sys
import json
import tempfile
import logging
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd

# Adiciona o diretório src ao path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

try:
    from preprocessing import TextPreprocessor, process_lusiadas_text
    from semantic_expansion import SemanticExpander
    from search_analysis import ContextAnalyzer, run_complete_analysis
    from visualization import DataVisualizer, create_visualization_report
except ImportError as e:
    logging.error(f"Erro ao importar módulos: {e}")

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint para rotas de análise
analysis_bp = Blueprint('analysis', __name__)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'docx', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Cria diretório de upload se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path, file_extension):
    """
    Extrai texto de diferentes tipos de arquivo.
    
    Args:
        file_path: Caminho para o arquivo
        file_extension: Extensão do arquivo
        
    Returns:
        Texto extraído
    """
    try:
        if file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_extension == 'docx':
            from docx import Document
            doc = Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        
        elif file_extension == 'pdf':
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_extension}")
    
    except Exception as e:
        logger.error(f"Erro ao extrair texto do arquivo: {e}")
        raise

@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar saúde da API."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@analysis_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint para upload de arquivos.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Tipo de arquivo não permitido. Use: .txt, .docx, .pdf'
            }), 400
        
        # Salva arquivo
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        file.save(file_path)
        
        # Extrai texto
        file_extension = filename.rsplit('.', 1)[1].lower()
        text_content = extract_text_from_file(file_path, file_extension)
        
        # Estatísticas básicas
        stats = {
            'filename': filename,
            'file_size': os.path.getsize(file_path),
            'text_length': len(text_content),
            'word_count': len(text_content.split()),
            'upload_time': datetime.now().isoformat()
        }
        
        return jsonify({
            'message': 'Arquivo enviado com sucesso',
            'file_id': filename,
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/preprocess', methods=['POST'])
def preprocess_text():
    """
    Endpoint para pré-processamento de texto.
    """
    try:
        data = request.get_json()
        
        if 'file_id' in data:
            # Processa arquivo enviado
            file_path = os.path.join(UPLOAD_FOLDER, data['file_id'])
            if not os.path.exists(file_path):
                return jsonify({'error': 'Arquivo não encontrado'}), 404
            
            file_extension = data['file_id'].rsplit('.', 1)[1].lower()
            text = extract_text_from_file(file_path, file_extension)
        
        elif 'text' in data:
            # Processa texto direto
            text = data['text']
        
        else:
            return jsonify({'error': 'Forneça file_id ou text'}), 400
        
        # Inicializa preprocessador
        preprocessor = TextPreprocessor()
        
        # Processa texto
        processed_text = preprocessor.preprocess(text)
        sentences = preprocessor.extract_sentences(text)
        
        # Se for Os Lusíadas, extrai cantos
        cantos = {}
        if 'lusíadas' in text.lower() or 'lusiadas' in text.lower():
            cantos = preprocessor.extract_verses_by_canto(text)
        
        # Estatísticas
        stats = {
            'original_length': len(text),
            'processed_length': len(processed_text),
            'sentences_count': len(sentences),
            'cantos_found': len(cantos),
            'processing_time': datetime.now().isoformat()
        }
        
        return jsonify({
            'processed_text': processed_text,
            'sentences': sentences[:10],  # Primeiras 10 sentenças
            'cantos': {str(k): v[:5] for k, v in list(cantos.items())[:3]},  # Primeiros 3 cantos, 5 versos cada
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"Erro no pré-processamento: {e}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/expand-semantic', methods=['POST'])
def expand_semantic():
    """
    Endpoint para expansão semântica.
    """
    try:
        data = request.get_json()
        
        # Parâmetros opcionais
        context = data.get('context', 'Os Lusíadas de Camões')
        use_claude = data.get('use_claude', True)
        use_fasttext = data.get('use_fasttext', False)
        use_bertimbau = data.get('use_bertimbau', True)
        
        # Inicializa expansor
        expander = SemanticExpander()
        
        results = {
            'seed_words': expander.seed_words,
            'claude_expansion': [],
            'fasttext_expansion': [],
            'bertimbau_expansion': [],
            'combined_expansion': []
        }
        
        # Expansão com Claude
        if use_claude:
            claude_words = expander.expand_with_claude(context)
            results['claude_expansion'] = claude_words
        
        # Expansão com FastText
        if use_fasttext:
            fasttext_words = list(expander.expand_with_fasttext())
            results['fasttext_expansion'] = fasttext_words
        
        # Expansão com BERTimbau
        if use_bertimbau:
            bertimbau_words = list(expander.expand_with_bertimbau())
            results['bertimbau_expansion'] = bertimbau_words
        
        # Combina todas as palavras
        all_words = set(expander.seed_words)
        all_words.update(results['claude_expansion'])
        all_words.update(results['fasttext_expansion'])
        all_words.update(results['bertimbau_expansion'])
        
        results['combined_expansion'] = sorted(list(all_words))
        
        # Estatísticas
        stats = {
            'total_words': len(results['combined_expansion']),
            'claude_words': len(results['claude_expansion']),
            'fasttext_words': len(results['fasttext_expansion']),
            'bertimbau_words': len(results['bertimbau_expansion']),
            'expansion_time': datetime.now().isoformat()
        }
        
        return jsonify({
            'expansion_results': results,
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"Erro na expansão semântica: {e}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/analyze-contexts', methods=['POST'])
def analyze_contexts():
    """
    Endpoint para análise de contextos.
    """
    try:
        data = request.get_json()
        
        # Parâmetros obrigatórios
        if 'text' not in data or 'words' not in data:
            return jsonify({'error': 'Forneça text e words'}), 400
        
        text = data['text']
        words = data['words']
        
        # Parâmetros opcionais
        context_window = data.get('context_window', 100)
        classify_with_claude = data.get('classify_with_claude', True)
        
        # Inicializa analisador
        analyzer = ContextAnalyzer()
        
        # Busca contextos
        contexts_df = analyzer.search_contexts(text, words, context_window)
        
        if contexts_df.empty:
            return jsonify({
                'message': 'Nenhum contexto encontrado',
                'contexts': [],
                'frequencies': {},
                'patterns': {}
            })
        
        # Classifica contextos com Claude se solicitado
        if classify_with_claude:
            contexts_df = analyzer.classify_contexts_with_claude(contexts_df)
        
        # Calcula frequências
        frequencies = analyzer.calculate_frequencies(contexts_df)
        
        # Analisa padrões
        patterns = analyzer.analyze_patterns(contexts_df)
        
        # Converte DataFrame para formato JSON
        contexts_list = contexts_df.to_dict('records')
        
        # Converte DataFrames em frequencies para dicionários
        frequencies_json = {}
        for key, value in frequencies.items():
            if isinstance(value, pd.DataFrame):
                frequencies_json[key] = value.to_dict('records')
            else:
                frequencies_json[key] = value
        
        return jsonify({
            'contexts': contexts_list[:50],  # Limita a 50 contextos para performance
            'total_contexts': len(contexts_df),
            'frequencies': frequencies_json,
            'patterns': patterns
        })
    
    except Exception as e:
        logger.error(f"Erro na análise de contextos: {e}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/generate-visualizations', methods=['POST'])
def generate_visualizations():
    """
    Endpoint para gerar visualizações.
    """
    try:
        data = request.get_json()
        
        # Parâmetros obrigatórios
        if 'contexts' not in data or 'frequencies' not in data:
            return jsonify({'error': 'Forneça contexts e frequencies'}), 400
        
        # Converte dados de volta para DataFrames
        contexts_df = pd.DataFrame(data['contexts'])
        
        frequencies = {}
        for key, value in data['frequencies'].items():
            if isinstance(value, list):
                frequencies[key] = pd.DataFrame(value)
            else:
                frequencies[key] = value
        
        patterns = data.get('patterns', {})
        
        # Cria diretório temporário para visualizações
        temp_dir = tempfile.mkdtemp()
        
        # Inicializa visualizador
        visualizer = DataVisualizer(temp_dir)
        
        # Gera visualizações
        generated_files = visualizer.generate_all_visualizations(
            contexts_df, frequencies, patterns
        )
        
        # Cria relatório
        report_path = create_visualization_report(generated_files, temp_dir)
        
        # Lista arquivos gerados
        files_info = {}
        for key, path in generated_files.items():
            if os.path.exists(path):
                files_info[key] = {
                    'filename': os.path.basename(path),
                    'size': os.path.getsize(path),
                    'path': path
                }
        
        return jsonify({
            'message': 'Visualizações geradas com sucesso',
            'files': files_info,
            'report_path': report_path,
            'temp_dir': temp_dir
        })
    
    except Exception as e:
        logger.error(f"Erro na geração de visualizações: {e}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    """
    Endpoint para download de arquivos gerados.
    """
    try:
        # Busca arquivo em diretórios possíveis
        possible_dirs = [
            UPLOAD_FOLDER,
            'results',
            'results/visualizations',
            tempfile.gettempdir()
        ]
        
        file_path = None
        for directory in possible_dirs:
            potential_path = os.path.join(directory, filename)
            if os.path.exists(potential_path):
                file_path = potential_path
                break
        
        if not file_path:
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        return send_file(file_path, as_attachment=True)
    
    except Exception as e:
        logger.error(f"Erro no download: {e}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/complete-analysis', methods=['POST'])
def complete_analysis():
    """
    Endpoint para análise completa (pipeline completo).
    """
    try:
        data = request.get_json()
        
        # Parâmetros
        if 'file_id' in data:
            file_path = os.path.join(UPLOAD_FOLDER, data['file_id'])
            if not os.path.exists(file_path):
                return jsonify({'error': 'Arquivo não encontrado'}), 404
            
            file_extension = data['file_id'].rsplit('.', 1)[1].lower()
            text = extract_text_from_file(file_path, file_extension)
        
        elif 'text' in data:
            text = data['text']
        
        else:
            return jsonify({'error': 'Forneça file_id ou text'}), 400
        
        # Pipeline completo
        results = {}
        
        # 1. Pré-processamento
        preprocessor = TextPreprocessor()
        processed_text = preprocessor.preprocess(text)
        cantos = preprocessor.extract_verses_by_canto(text)
        results['preprocessing'] = {
            'processed_text_length': len(processed_text),
            'cantos_found': len(cantos)
        }
        
        # 2. Expansão semântica
        expander = SemanticExpander()
        expansion_results = expander.get_comprehensive_expansion()
        words = expansion_results['combined_expansion']
        results['semantic_expansion'] = {
            'total_words': len(words),
            'expansion_methods': list(expansion_results.keys())
        }
        
        # 3. Análise de contextos
        analyzer = ContextAnalyzer()
        contexts_df = analyzer.search_contexts(processed_text, words)
        
        if not contexts_df.empty:
            contexts_df = analyzer.classify_contexts_with_claude(contexts_df)
            frequencies = analyzer.calculate_frequencies(contexts_df)
            patterns = analyzer.analyze_patterns(contexts_df)
            
            results['context_analysis'] = {
                'total_contexts': len(contexts_df),
                'unique_words_found': contexts_df['word'].nunique()
            }
        else:
            frequencies = {}
            patterns = {}
            results['context_analysis'] = {
                'total_contexts': 0,
                'unique_words_found': 0
            }
        
        # 4. Visualizações
        temp_dir = tempfile.mkdtemp()
        visualizer = DataVisualizer(temp_dir)
        generated_files = visualizer.generate_all_visualizations(
            contexts_df, frequencies, patterns
        )
        
        results['visualizations'] = {
            'files_generated': len(generated_files),
            'temp_dir': temp_dir
        }
        
        # Resumo final
        summary = {
            'analysis_complete': True,
            'timestamp': datetime.now().isoformat(),
            'pipeline_steps': list(results.keys()),
            'total_processing_time': 'calculated_in_frontend'
        }
        
        return jsonify({
            'summary': summary,
            'results': results,
            'contexts': contexts_df.to_dict('records')[:20] if not contexts_df.empty else [],
            'frequencies': {k: v.to_dict('records') if isinstance(v, pd.DataFrame) else v 
                          for k, v in frequencies.items()},
            'patterns': patterns,
            'generated_files': generated_files
        })
    
    except Exception as e:
        logger.error(f"Erro na análise completa: {e}")
        return jsonify({'error': str(e)}), 500

# Registra blueprint no app principal
def register_analysis_routes(app):
    """Registra as rotas de análise no app Flask."""
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
