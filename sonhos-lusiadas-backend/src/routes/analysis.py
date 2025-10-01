#!/usr/bin/env python3
"""
Rotas de análise do backend Sonhos Lusíadas
"""

import os
import sys
import logging
import re
import unicodedata
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import json

# Importar bibliotecas para processamento de arquivos
try:
    import docx2txt
    DOCX2TXT_AVAILABLE = True
    print("OK: docx2txt disponivel para processamento de arquivos .doc")
except ImportError:
    DOCX2TXT_AVAILABLE = False
    print("AVISO: docx2txt nao disponivel - arquivos .doc podem nao funcionar")

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

def remove_gutenberg_boilerplate(text: str) -> str:
    """Remove cabeçalhos/rodapés padrão do Project Gutenberg e numerações soltas."""
    if not isinstance(text, str):
        return ''

    start_markers = [
        "*** START OF THIS PROJECT GUTENBERG EBOOK OS LUSÍADAS ***",
        "*** START OF THE PROJECT GUTENBERG EBOOK OS LUSÍADAS ***"
    ]
    end_markers = [
        "*** END OF THIS PROJECT GUTENBERG EBOOK OS LUSÍADAS ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK OS LUSÍADAS ***"
    ]

    start_idx = -1
    end_idx = -1
    for m in start_markers:
        i = text.find(m)
        if i != -1:
            start_idx = i + len(m)
            break
    for m in end_markers:
        i = text.find(m)
        if i != -1:
            end_idx = i
            break

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        text = text[start_idx:end_idx]
    elif start_idx != -1:
        text = text[start_idx:]
    elif end_idx != -1:
        text = text[:end_idx]

    # Normaliza quebras; preserva linhas numéricas (números de estrofe)
    text = re.sub(r"\r\n?", "\n", text)
    return text.strip()


def split_cantos(text):
    """Separa o texto em cantos CANTO I ... CANTO X.

    Retorna um dicionário { 'CANTO I': texto, ..., 'CANTO X': texto }.
    Caso não encontre marcadores de canto, retorna {'COMPLETO': text}.
    """
    if not text:
        return {'COMPLETO': ''}

    # Normaliza quebras e espaços para melhorar o split
    normalized = re.sub(r"\r\n?", "\n", text)

    # Suporta: CANTO I..X e CANTO PRIMEIRO..DÉCIMO (com e sem acento)
    roman = r"(I|II|III|IV|V|VI|VII|VIII|IX|X)"
    extenso = r"(PRIMEIRO|SEGUNDO|TERCEIRO|QUARTO|QUINTO|SEXTO|SE[TÍI]MO|OITAVO|NONO|D[ÉE]CIMO)"
    pattern = re.compile(rf"(^|\n)\s*CANTO\s+({roman}|{extenso})\b", re.IGNORECASE)
    parts = []
    last_index = 0
    matches = list(pattern.finditer(normalized))

    if not matches:
        return {'COMPLETO': text}

    for idx, m in enumerate(matches):
        if idx > 0:
            prev = matches[idx - 1]
            canto_roman = prev.group(2).upper()
            canto_title = f"CANTO {canto_roman}"
            parts.append((canto_title, normalized[last_index:m.start()].strip()))
        last_index = m.end()

    # Último bloco
    last_match = matches[-1]
    canto_marker = last_match.group(2).upper()
    canto_title = f"CANTO {canto_marker}"
    parts.append((canto_title, normalized[last_index:].strip()))

    # Constrói dict, ignorando blocos vazios
    result = {}
    for title, content in parts:
        if content:
            result[title] = content

    return result if result else {'COMPLETO': text}

def normalize_text(text: str) -> str:
    """Normaliza texto para comparação: minúsculas, remove acentos, espaçamentos básicos."""
    if not isinstance(text, str):
        return ''
    lowered = text.lower()
    # remove acentos
    no_acc = unicodedata.normalize('NFKD', lowered)
    no_acc = ''.join(ch for ch in no_acc if not unicodedata.combining(ch))
    # normaliza espaços
    no_acc = re.sub(r"\s+", " ", no_acc).strip()
    return no_acc

def build_term_pattern(term: str) -> re.Pattern:
    """Cria regex com bordas de palavra para um termo já normalizado."""
    term_norm = normalize_text(term)
    # protege caracteres especiais
    esc = re.escape(term_norm)
    # bordas de palavra; permite termos compostos
    return re.compile(rf"\b{esc}\b", re.IGNORECASE)

def build_sonho_pattern() -> re.Pattern:
    """Padrão específico para capturar 'sonho*' e variações."""
    # Busca por: sonho, sonhos, sonhar, sonhando, sonhador, sonhante, sonhoso, etc.
    return re.compile(r'\bsonh[a-z]*\b', re.IGNORECASE)

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

# Dicionários de termos
EXPANDED_TERMS_FULL = {
    'onírico': [
        'sonho', 'sonhar', 'pesadelo',
        'dormir', 'adormecer', 'despertar',
        'sonolência', 'sonolento', 'repouso', 'repousar',
        'descanso', 'descansar'
    ],
    'profético': [
        'visão', 'profecia', 'revelação', 'aparição',
        'oráculo', 'vaticínio', 'presságio', 'augúrio', 'predição'
    ],
    'alegórico': [
        'sombra', 'fantasia', 'ilusão', 'metáfora', 'símbolo', 'alegoria', 'figura'
    ],
    'divino': [
        'glória', 'glorioso', 'divino', 'celestial', 'sobrenatural',
        'milagre', 'milagroso', 'sagrado', 'santo', 'bendito', 'abençoado', 'miraculoso'
    ]
}

EXPANDED_TERMS_STRICT = {
    'onírico': [
        'sonho', 'sonhos', 'sonhar', 'sonhando', 'sonhador', 'sonhante', 'sonhoso', 'sonhava', 'sonhei', 'sonharia',
        'pesadelo', 'pesadelos', 'pesadelar', 'pesadelando', 'pesadelava',
        'dormir', 'dormindo', 'dormia', 'dormiu', 'dormirá', 'adormecer', 'adormecendo', 'adormecia', 'adormeceu',
        'despertar', 'despertando', 'despertava', 'despertou', 'despertará',
        'repouso', 'repousar', 'repousando', 'repousava', 'repousou',
        'descanso', 'descansar', 'descansando', 'descansava', 'descansou',
        'sonolência', 'sonolento', 'sonolentamente',
        'sonambulismo', 'sonambúlico', 'sonambular',
        'insônia', 'insone', 'insoniamente',
        'soneca', 'sonecar', 'sonecante'
    ],
    'profético': [
        'visão', 'visões', 'visionário', 'visionar', 'visionando', 'visionava', 'visionou',
        'profecia', 'profécias', 'profético', 'profetizar', 'profetizando', 'profetizava', 'profetizou',
        'revelação', 'revelações', 'revelar', 'revelando', 'revelava', 'revelou',
        'aparição', 'aparições', 'aparecer', 'aparecendo', 'aparecia', 'apareceu',
        'oráculo', 'oráculos', 'oracular', 'oracularmente',
        'presságio', 'presságios', 'pressagiar', 'pressagiando', 'pressagiava', 'pressagiou',
        'vaticínio', 'vaticínios', 'vaticinar', 'vaticinando', 'vaticinava', 'vaticinou',
        'augúrio', 'augúrios', 'augurar', 'augurando', 'augurava', 'augurou'
    ]
}

def get_terms(mode: str):
    """Retorna dicionário de termos por modo (estrito ou completo)."""
    if (mode or '').lower() == 'estrito':
        return EXPANDED_TERMS_STRICT
    return EXPANDED_TERMS_FULL

def count_expanded_terms(text: str, terms_to_use: dict) -> dict:
    """Conta termos expandidos no texto dado um conjunto de termos."""
    results: dict = {}
    text_norm = normalize_text(text)
    sonho_pattern = build_sonho_pattern()

    for category, terms in terms_to_use.items():
        results[category] = {}
        total_count = 0
        
        # Busca específica por "sonho*" para categoria onírica
        if category == 'onírico':
            sonho_matches = sonho_pattern.findall(text_norm)
            if sonho_matches:
                # Agrupa variações de sonho
                sonho_variations = {}
                for match in sonho_matches:
                    sonho_variations[match] = sonho_variations.get(match, 0) + 1
                
                for variation, count in sonho_variations.items():
                    results[category][variation] = count
                    total_count += count
        
        # Busca pelos outros termos
        for term in terms:
            pat = build_term_pattern(term)
            count = len(pat.findall(text_norm))
            if count > 0:
                results[category][term] = count
                total_count += count
        results[category]['total'] = total_count
    return results

def analyze_dream_contexts(text: str, terms_to_use: dict) -> list:
    """Analisa contextos e identifica número de estrofe quando presente na linha anterior.

    Heurística de estrofe: muitas edições do Gutenberg apresentam números de estrofe
    em uma linha sozinha antes do bloco de versos. Vamos propagar o último número
    visto para as linhas seguintes até surgir um novo número.
    """
    lines = re.split(r"\n+", text)
    dream_contexts: list = []

    current_stanza = None
    buffer_sentence = ''
    sonho_pattern = build_sonho_pattern()

    def flush_buffer(idx: int, stanza_num):
        nonlocal buffer_sentence
        s = buffer_sentence.strip()
        if not s:
            return None
        s_norm = normalize_text(s)
        dream_terms = []
        
        # Busca específica por "sonho*" primeiro
        sonho_matches = sonho_pattern.findall(s_norm)
        if sonho_matches:
            print(f"DEBUG: Encontrado 'sonho*' na estrofe {stanza_num}: {sonho_matches} - '{s[:50]}...'")
            for match in sonho_matches:
                excerpt = s if len(s) <= 220 else (s[:220] + '...')
                dream_terms.append({'term': match, 'category': 'onírico', 'excerpt': excerpt})
        
        # Busca pelos outros termos
        for category, terms in terms_to_use.items():
            for term in terms:
                if build_term_pattern(term).search(s_norm):
                    excerpt = s if len(s) <= 220 else (s[:220] + '...')
                    dream_terms.append({'term': term, 'category': category, 'excerpt': excerpt})
        
        buffer_sentence = ''
        if dream_terms:
            return {
                'sentence': s,
                'position': idx,
                'stanza': stanza_num,
                'terms': dream_terms,
                'context_type': classify_context_type(dream_terms)
            }
        return None

    idx = 0
    for raw in lines:
        line = raw.strip()
        if not line:
            # quebra de bloco: fecha buffer como sentença
            ctx = flush_buffer(idx, current_stanza)
            if ctx:
                dream_contexts.append(ctx)
                idx += 1
            continue

        # Detecta linha que é somente número (possível estrofe)
        if re.fullmatch(r"\d+", line):
            # fecha buffer antes de mudar estrofe
            ctx = flush_buffer(idx, current_stanza)
            if ctx:
                dream_contexts.append(ctx)
                idx += 1
            current_stanza = int(line)
            print(f"DEBUG: Detectada estrofe {current_stanza}")
            continue
        
        # Também detecta números no início da linha seguidos de espaço
        stanza_match = re.match(r"^(\d+)\s", line)
        if stanza_match:
            # fecha buffer antes de mudar estrofe
            ctx = flush_buffer(idx, current_stanza)
            if ctx:
                dream_contexts.append(ctx)
                idx += 1
            current_stanza = int(stanza_match.group(1))
            print(f"DEBUG: Detectada estrofe {current_stanza} no início da linha")
            # Remove o número do início da linha
            line = line[stanza_match.end():].strip()
            if not line:
                continue

        # acumula verso na sentença corrente
        if buffer_sentence:
            buffer_sentence += ' ' + line
        else:
            buffer_sentence = line

    # flush final
    ctx = flush_buffer(idx, current_stanza)
    if ctx:
        dream_contexts.append(ctx)

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

def calculate_analysis_metrics(text: str, aggregated: dict) -> dict:
    """Calcula métricas de validação globais a partir do texto e agregados."""
    total_words = len(text.split())
    terms_found = aggregated.get('semantic_expansion', {}).get('terms_found', 0)
    coverage = (terms_found / total_words) if total_words > 0 else 0
    confidence = min(95, coverage * 1000) if total_words > 0 else 0
    return {
        'coverage': coverage,
        'total_words': total_words,
        'dream_terms_found': terms_found,
        'confidence_score': confidence
    }

@analysis_bp.route('/complete-analysis', methods=['POST'])
def complete_analysis():
    """Análise completa do texto com separação por cantos e modo estrito opcional."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        mode = (data.get('mode', 'default') or 'default').lower()  # 'default' ou 'estrito'

        print(f"DEBUG BACKEND: Texto recebido: {text[:100]}...")
        print(f"DEBUG BACKEND: Tamanho do texto: {len(text)} caracteres")
        print(f"DEBUG BACKEND: Modo: {mode}")

        if not text:
            return jsonify({'error': 'Texto é obrigatório'}), 400

        # Limpa boilerplate do Gutenberg
        cleaned_text = remove_gutenberg_boilerplate(text)

        # Define termos conforme modo
        terms_to_use = get_terms(mode)

        # Separa por cantos
        cantos = split_cantos(cleaned_text)

        per_canto_results = {}
        aggregate_counts = {'onírico': 0, 'profético': 0, 'alegórico': 0, 'divino': 0}
        aggregate_terms_found = 0
        aggregate_words = 0
        aggregate_unique_words = set()
        aggregate_sentences = 0

        # Acúmulos para compatibilidade legada
        legacy_expanded_terms: dict = {}
        legacy_dream_contexts: list = []

        for canto_title, canto_text in cantos.items():
            canto_expanded = count_expanded_terms(canto_text, terms_to_use)
            canto_contexts = analyze_dream_contexts(canto_text, terms_to_use)
            # Estrofes com ocorrência
            stanzas_with_hits = sorted({ctx.get('stanza') for ctx in canto_contexts if ctx.get('stanza') is not None})
            canto_classification = {
                'onírico': len([ctx for ctx in canto_contexts if ctx['context_type'] == 'onírico']),
                'profético': len([ctx for ctx in canto_contexts if ctx['context_type'] == 'profético']),
                'alegórico': len([ctx for ctx in canto_contexts if ctx['context_type'] == 'alegórico']),
                'divino': len([ctx for ctx in canto_contexts if ctx['context_type'] == 'divino'])
            }
            canto_pre = {
                'original_length': len(canto_text),
                'processed_length': len(normalize_text(canto_text)),
                'sentences': len(re.split(r"(?<=[\.!?])\s+|\n+", canto_text)),
                'words': len(canto_text.split()),
                'unique_words': len(set(normalize_text(canto_text).split()))
            }

            per_canto_results[canto_title] = {
                'preprocessing': canto_pre,
                'expanded_terms': canto_expanded,
                'dream_contexts': canto_contexts,
                'context_classification': canto_classification,
                'stanzas': stanzas_with_hits,
                'semantic_expansion': {
                    'total_categories': len(terms_to_use),
                    'total_terms_searched': sum(len(terms) for terms in terms_to_use.values()),
                    'terms_found': sum(cat['total'] for cat in canto_expanded.values()),
                    'coverage_percentage': (sum(cat['total'] for cat in canto_expanded.values()) / canto_pre['words']) * 100 if canto_pre['words'] > 0 else 0
                }
            }

            # Agrega
            for k in aggregate_counts.keys():
                aggregate_counts[k] += canto_classification.get(k, 0)
            aggregate_terms_found += sum(cat.get('total', 0) for cat in canto_expanded.values())
            aggregate_words += canto_pre['words']
            aggregate_unique_words.update(set(normalize_text(canto_text).split()))
            aggregate_sentences += canto_pre['sentences']

            # Compatibilidade legada: somar termos por categoria/termo
            for category, terms in canto_expanded.items():
                if category not in legacy_expanded_terms:
                    legacy_expanded_terms[category] = {}
                for term, cnt in terms.items():
                    if term == 'total':
                        continue
                    legacy_expanded_terms[category][term] = legacy_expanded_terms[category].get(term, 0) + int(cnt)

            # Compatibilidade legada: juntar contextos e anotar o canto
            for ctx in canto_contexts:
                ctx_with_canto = dict(ctx)
                ctx_with_canto['canto'] = canto_title
                legacy_dream_contexts.append(ctx_with_canto)

        aggregate_results = {
            'preprocessing': {
                'original_length': len(cleaned_text),
                'processed_length': len(normalize_text(cleaned_text)),
                'sentences': aggregate_sentences,
                'words': aggregate_words,
                'unique_words': len(aggregate_unique_words)
            },
            'context_classification': aggregate_counts,
            'semantic_expansion': {
                'total_categories': len(terms_to_use),
                'total_terms_searched': sum(len(terms) for terms in terms_to_use.values()),
                'terms_found': aggregate_terms_found,
                'coverage_percentage': (aggregate_terms_found / aggregate_words) * 100 if aggregate_words > 0 else 0
            },
            'cantos_identified': len(cantos),
            # Novo: mapa de estrofes por canto
            'stanzas_by_canto': {k: v.get('stanzas', []) for k, v in per_canto_results.items()}
        }

        # Métricas globais
        aggregate_results['validation_metrics'] = calculate_analysis_metrics(cleaned_text, aggregate_results)

        # Estrutura de resposta com detalhamento e campos legados para o frontend atual
        legacy_flat = {
            'preprocessing': aggregate_results['preprocessing'],
            'expanded_terms': legacy_expanded_terms,
            'context_classification': aggregate_results['context_classification'],
            'validation_metrics': aggregate_results['validation_metrics'],
            'dream_contexts': legacy_dream_contexts,
        }

        return jsonify({
            'message': 'Análise expandida realizada com sucesso',
            'results': {
                'by_canto': per_canto_results,
                'aggregate': aggregate_results,
                # Campos legados (compat):
                **legacy_flat
            },
            'methodology': {
                'name': 'Análise Semântica Expandida dos Lusíadas',
                'version': '2.0',
                'description': 'Metodologia completa para análise de temas oníricos com expansão semântica',
                'categories_analyzed': list(terms_to_use.keys()),
                'total_terms': sum(len(terms) for terms in terms_to_use.values()),
                'mode': mode
            }
        })

    except Exception as e:
        logger.error(f"Erro na análise completa: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500