"""
Módulo de Análise NLP Tradicional
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa

Este módulo implementa técnicas tradicionais de Processamento de Linguagem Natural
para análise de sonhos em Os Lusíadas, substituindo dependências de LLMs por:

- Tokenização e lematização
- POS Tagging (Part-of-Speech)
- Análise de coocorrência de palavras
- Algoritmos de similaridade semântica baseados em corpus
- Técnicas de processamento de linguagem natural estatísticas
- Análise de padrões linguísticos baseada em regras
"""

import re
import nltk
import spacy
import numpy as np
import pandas as pd
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TraditionalNLPAnalyzer:
    """Analisador NLP tradicional para análise de sonhos em Os Lusíadas."""
    
    def __init__(self):
        """Inicializa o analisador NLP tradicional."""
        self.nlp = None
        self.stemmer = None
        self.stopwords = set()
        self._setup_nlp_models()
        
        # Termos relacionados ao sono (agrupados por categoria)
        # FOCO ESPECÍFICO EM SONHOS - não termos gerais
        self.sleep_terms = {
            'onírico': [
                'sonho', 'sonhos', 'sonhar', 'sonhando', 'sonhador', 'sonhante', 'sonhoso', 
                'sonhava', 'sonhei', 'sonharia', 'sonhado', 'sonhante',
                'pesadelo', 'pesadelos', 'pesadelar', 'pesadelando', 'pesadelava',
                'dormir', 'dormindo', 'dormia', 'dormiu', 'dormirá', 'adormecer', 'adormecendo', 
                'adormecia', 'adormeceu', 'despertar', 'despertando', 'despertava', 'despertou',
                'repouso', 'repousar', 'repousando', 'repousava', 'repousou',
                'descanso', 'descansar', 'descansando', 'descansava', 'descansou',
                'sonolência', 'sonolento', 'sonolentamente', 'sonambulismo', 'sonambúlico',
                'insônia', 'insone', 'soneca', 'sonecar', 'sonecante'
            ],
            'profético': [
                'visão', 'visões', 'visionário', 'visionar', 'visionando', 'visionava',
                'profecia', 'profécias', 'profético', 'profetizar', 'profetizando', 'profetizava',
                'revelação', 'revelações', 'revelar', 'revelando', 'revelava', 'revelou',
                'aparição', 'aparições', 'aparecer', 'aparecendo', 'aparecia', 'apareceu',
                'oráculo', 'oráculos', 'oracular', 'presságio', 'presságios', 'pressagiar',
                'vaticínio', 'vaticínios', 'vaticinar', 'vaticinando', 'vaticinava',
                'augúrio', 'augúrios', 'augurar', 'augurando', 'augurava'
            ],
            'alegórico': [
                'sombra', 'sombras', 'sombreado', 'sombreado', 'sombreado',
                'fantasia', 'fantasias', 'fantasioso', 'fantasioso',
                'ilusão', 'ilusões', 'ilusório', 'iludir', 'iludindo', 'iludia',
                'metáfora', 'metáforas', 'metafórico', 'símbolo', 'símbolos', 'simbólico',
                'alegoria', 'alegorias', 'alegórico', 'figura', 'figuras', 'figurado'
            ],
            'divino': [
                'glória', 'glorioso', 'glorificar', 'glorificando', 'glorificava',
                'divino', 'divinos', 'divinizar', 'divinizando', 'divinizava',
                'celestial', 'celestiais', 'sobrenatural', 'sobrenaturais',
                'milagre', 'milagres', 'milagroso', 'milagrosos',
                'sagrado', 'sagrados', 'santificar', 'santificando', 'santificava',
                'santo', 'santos', 'santidade', 'bendito', 'abençoado', 'abençoar'
            ],
            'ilusório': [
                'ilusão', 'ilusões', 'ilusório', 'iludir', 'iludindo', 'iludia',
                'quimera', 'quimeras', 'quimérico', 'miragem', 'miragens',
                'falsa', 'falso', 'falsos', 'falsas', 'falsidade', 'falsificar'
            ]
        }
        
        # Categorias de classificação (mantidas conforme solicitado)
        self.categories = {
            'onírico': ['sono', 'sonho', 'dormir', 'pesadelo'],
            'profético': ['visão', 'profecia', 'revelação', 'presságio'],
            'alegórico': ['sombra', 'fantasia', 'ilusão', 'metáfora'],
            'divino': ['glória', 'divino', 'celestial', 'sobrenatural'],
            'ilusório': ['ilusão', 'quimera', 'miragem', 'falsa']
        }
    
    def _setup_nlp_models(self):
        """Configura modelos NLP necessários."""
        try:
            # Carrega modelo spaCy para português
            self.nlp = spacy.load("pt_core_news_sm")
            logger.info("Modelo spaCy carregado com sucesso.")
        except OSError:
            logger.warning("Modelo spaCy não encontrado. Usando modelo básico.")
            self.nlp = spacy.blank("pt")
            # Garante segmentação de sentenças mesmo no modelo básico
            if 'sentencizer' not in self.nlp.pipe_names:
                self.nlp.add_pipe('sentencizer')
        
        try:
            # Configura stemmer RSLP
            from nltk.stem import RSLPStemmer
            self.stemmer = RSLPStemmer()
            logger.info("Stemmer RSLP configurado.")
        except:
            logger.warning("Stemmer RSLP não disponível.")
            self.stemmer = None
        
        try:
            # Carrega stopwords
            from nltk.corpus import stopwords
            self.stopwords = set(stopwords.words('portuguese'))
            logger.info("Stopwords carregadas.")
        except LookupError:
            nltk.download('stopwords')
            from nltk.corpus import stopwords
            self.stopwords = set(stopwords.words('portuguese'))
            logger.info("Stopwords baixadas e carregadas.")
    
    def tokenize_and_lemmatize(self, text: str) -> List[str]:
        """
        Tokeniza e lematiza o texto.
        
        Args:
            text: Texto para processar
            
        Returns:
            Lista de tokens lematizados
        """
        doc = self.nlp(text)
        tokens = []
        
        for token in doc:
            if not token.is_space and not token.is_punct and not token.is_stop:
                if hasattr(token, 'lemma_') and token.lemma_:
                    tokens.append(token.lemma_.lower())
                else:
                    tokens.append(token.text.lower())
        
        return tokens
    
    def pos_tagging(self, text: str) -> List[Tuple[str, str]]:
        """
        Realiza POS tagging do texto.
        
        Args:
            text: Texto para analisar
            
        Returns:
            Lista de tuplas (token, pos_tag)
        """
        doc = self.nlp(text)
        pos_tags = []
        
        for token in doc:
            if not token.is_space and not token.is_punct:
                pos_tags.append((token.text.lower(), token.pos_))
        
        return pos_tags
    
    def extract_sleep_related_terms(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extrai termos relacionados ao sono usando técnicas tradicionais.
        
        Args:
            text: Texto para analisar
            
        Returns:
            Dicionário com termos encontrados e seus contextos
        """
        results = defaultdict(list)
        text_lower = text.lower()
        
        for category, terms in self.sleep_terms.items():
            for term in terms:
                # Captura o termo e possíveis flexões simples (sufixos alfanuméricos)
                pattern = re.compile(rf'\b{re.escape(term)}\w*\b', re.IGNORECASE)
                for match in pattern.finditer(text_lower):
                    # Extrai contexto (100 caracteres antes e depois para contexto mais rico)
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()
                    
                    # Identifica estrofe se possível
                    stanza = self._extract_stanza_number(text, match.start())
                    
                    results[category].append({
                        'term': match.group(0),
                        'context': context,
                        'text': context,  # Adiciona campo 'text' para compatibilidade
                        'excerpt': context,  # Adiciona campo 'excerpt' para compatibilidade
                        'position': match.start(),
                        'stanza': stanza,
                        'category': category
                    })
        
        return dict(results)
    
    def _extract_stanza_number(self, text: str, position: int) -> Optional[int]:
        """
        Extrai número da estrofe baseado na posição.
        
        Args:
            text: Texto completo
            position: Posição do termo
            
        Returns:
            Número da estrofe ou None
        """
        # Busca por números de estrofe antes da posição
        text_before = text[:position]
        
        # Padrão para números de estrofe (números soltos em linhas)
        stanza_pattern = re.compile(r'^\s*(\d+)\s*$', re.MULTILINE)
        matches = list(stanza_pattern.finditer(text_before))
        
        if matches:
            return int(matches[-1].group(1))
        
        return None
    
    def analyze_cooccurrence(self, text: str, window_size: int = 5) -> Dict[str, Dict[str, int]]:
        """
        Analisa coocorrência de palavras relacionadas ao sono.
        
        Args:
            text: Texto para analisar
            window_size: Tamanho da janela de coocorrência
            
        Returns:
            Dicionário com matriz de coocorrência
        """
        tokens = self.tokenize_and_lemmatize(text)
        cooccurrence = defaultdict(lambda: defaultdict(int))
        
        # Identifica posições dos termos de sono
        sleep_positions = []
        for i, token in enumerate(tokens):
            for category, terms in self.sleep_terms.items():
                for term in terms:
                    if token.startswith(term):
                        sleep_positions.append((i, token, category))
        
        # Calcula coocorrência
        for pos, sleep_token, category in sleep_positions:
            start = max(0, pos - window_size)
            end = min(len(tokens), pos + window_size + 1)
            
            for i in range(start, end):
                if i != pos:
                    cooccurrence[sleep_token][tokens[i]] += 1
        
        return dict(cooccurrence)
    
    def calculate_semantic_similarity(self, text: str) -> Dict[str, float]:
        """
        Calcula similaridade semântica usando TF-IDF.
        
        Args:
            text: Texto para analisar
            
        Returns:
            Dicionário com scores de similaridade
        """
        # Divide texto em sentenças
        sentences = [sent.text for sent in self.nlp(text).sents]
        
        if len(sentences) < 2:
            return {}
        
        # Cria vetorizador TF-IDF
        vectorizer = TfidfVectorizer(
            stop_words=list(self.stopwords),
            ngram_range=(1, 2),
            max_features=1000
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Calcula similaridade coseno
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Encontra sentenças mais similares
            similarities = {}
            for i in range(len(sentences)):
                for j in range(i + 1, len(sentences)):
                    similarity = similarity_matrix[i][j]
                    if similarity > 0.1:  # Threshold mínimo
                        similarities[f"sentence_{i}_{j}"] = similarity
            
            return similarities
            
        except Exception as e:
            logger.error(f"Erro no cálculo de similaridade: {e}")
            return {}
    
    def classify_dream_contexts(self, contexts: List[Dict]) -> List[Dict]:
        """
        Classifica contextos de sonho usando regras baseadas em padrões.
        
        Args:
            contexts: Lista de contextos encontrados
            
        Returns:
            Lista de contextos classificados
        """
        classified_contexts = []
        
        for context in contexts:
            category = context.get('category', 'onírico')
            text = context.get('context', '').lower()
            
            # Regras de classificação baseadas em padrões
            classification = self._classify_by_patterns(text, category)
            confidence = self._calculate_confidence(text, category)
            
            # Mapeia campos para o formato esperado pelo frontend
            classified_context = {
                'context_type': classification,
                'classification': classification,  # Mantém compatibilidade
                'confidence_score': confidence,
                'confidence': confidence,  # Mantém compatibilidade
                'sentence': context.get('context', ''),
                'text': context.get('context', ''),  # Mantém compatibilidade
                'excerpt': context.get('context', ''),  # Mantém compatibilidade
                'stanza': context.get('stanza'),
                'position': context.get('position'),
                'terms': [{
                    'term': context.get('term', ''),
                    'category': category,
                    'excerpt': context.get('context', '')
                }],
                'reasoning': self._generate_reasoning(text, classification, confidence)
            }
            
            classified_contexts.append(classified_context)
        
        return classified_contexts
    
    def _classify_by_patterns(self, text: str, category: str) -> str:
        """
        Classifica contexto baseado em padrões linguísticos.
        
        Args:
            text: Texto do contexto
            category: Categoria do termo
            
        Returns:
            Classificação do contexto
        """
        # Padrões para cada categoria
        patterns = {
            'divino': [
                r'\b(glória|divino|celestial|sobrenatural|milagre|sagrado|santo)\b',
                r'\b(deus|deuses|divindade|oráculo)\b',
                r'\b(revelação|aparição|manifestação)\b'
            ],
            'profético': [
                r'\b(visão|profecia|presságio|augúrio|vaticínio)\b',
                r'\b(futuro|porvir|predição|oráculo)\b',
                r'\b(anunciar|prever|pressagiar)\b'
            ],
            'alegórico': [
                r'\b(símbolo|metáfora|alegoria|figura)\b',
                r'\b(representar|significar|simbolizar)\b',
                r'\b(como|qual|assim como)\b'
            ],
            'ilusório': [
                r'\b(ilusão|quimera|miragem|falsa|falso)\b',
                r'\b(enganar|enganoso|fictício)\b',
                r'\b(aparência|semblante|aspecto)\b'
            ],
            'onírico': [
                r'\b(sonho|sonhar|dormir|pesadelo)\b',
                r'\b(adormecer|despertar|sonolento)\b',
                r'\b(repouso|descanso|soneca)\b'
            ]
        }
        
        # Conta ocorrências de padrões
        pattern_scores = {}
        for cat, pattern_list in patterns.items():
            score = 0
            for pattern in pattern_list:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            pattern_scores[cat] = score
        
        # Retorna categoria com maior score
        if pattern_scores:
            return max(pattern_scores, key=pattern_scores.get)
        
        return 'onírico'  # Default
    
    def _calculate_confidence(self, text: str, category: str) -> float:
        """
        Calcula confiança da classificação.
        
        Args:
            text: Texto do contexto
            category: Categoria do termo
            
        Returns:
            Score de confiança (0.0 a 1.0)
        """
        base_confidence = 0.5
        
        # Bonus por comprimento do contexto
        length_bonus = min(0.3, len(text) / 200)
        
        # Bonus por termos específicos
        specific_terms = ['sonho', 'visão', 'profecia', 'revelação', 'glória']
        term_bonus = 0.0
        for term in specific_terms:
            if term in text.lower():
                term_bonus += 0.1
        
        # Penalty por contexto muito curto
        length_penalty = 0.0
        if len(text) < 30:
            length_penalty = 0.2
        
        confidence = min(0.95, base_confidence + length_bonus + term_bonus - length_penalty)
        return round(confidence, 2)
    
    def _generate_reasoning(self, text: str, classification: str, confidence: float) -> str:
        """
        Gera explicação do raciocínio da classificação.
        
        Args:
            text: Texto do contexto
            classification: Classificação atribuída
            confidence: Confiança da classificação
            
        Returns:
            Explicação do raciocínio
        """
        reasoning = f"Classificado como '{classification}' com confiança de {confidence:.2f}. "
        
        if classification == 'divino':
            reasoning += "O contexto contém termos relacionados a revelações divinas ou sobrenaturais."
        elif classification == 'profético':
            reasoning += "O contexto sugere visões ou presságios sobre eventos futuros."
        elif classification == 'alegórico':
            reasoning += "O contexto indica uso simbólico ou metafórico relacionado a sonhos."
        elif classification == 'ilusório':
            reasoning += "O contexto refere-se a ilusões, quimeras ou falsas aparências."
        else:  # onírico
            reasoning += "O contexto refere-se diretamente a sonhos, pesadelos ou estados de sono."
        
        if len(text) > 100:
            reasoning += f" Contexto rico com {len(text)} caracteres."
        
        return reasoning
    
    def analyze_dream_patterns(self, text: str) -> Dict:
        """
        Analisa padrões de sonhos no texto usando técnicas tradicionais (modo completo).
        
        Args:
            text: Texto para analisar
            
        Returns:
            Dicionário com padrões identificados
        """
        # Extrai termos relacionados ao sono
        sleep_terms = self.extract_sleep_related_terms(text)
        
        # Analisa coocorrência
        cooccurrence = self.analyze_cooccurrence(text)
        
        # Calcula similaridade semântica
        similarity = self.calculate_semantic_similarity(text)
        
        # Classifica contextos
        all_contexts = []
        for category, contexts in sleep_terms.items():
            all_contexts.extend(contexts)
        
        classified_contexts = self.classify_dream_contexts(all_contexts)
        
        return {
            'sleep_terms': sleep_terms,
            'cooccurrence': cooccurrence,
            'similarity': similarity,
            'classified_contexts': classified_contexts,
            'total_contexts': len(classified_contexts),
            'categories_found': list(sleep_terms.keys())
        }
    
    def analyze_dream_patterns_strict(self, text: str) -> Dict:
        """
        Analisa padrões de sonhos no texto usando modo estrito (apenas termos muito específicos).
        
        Args:
            text: Texto para analisar
            
        Returns:
            Dicionário com padrões identificados
        """
        # Termos muito específicos para modo estrito
        strict_terms = {
            'onírico': [
                'sonho', 'sonhos', 'sonhar', 'sonhando', 'sonhava', 'sonhei', 'sonharia',
                'pesadelo', 'pesadelos', 'pesadelar', 'pesadelando', 'pesadelava',
                'dormir', 'dormindo', 'dormia', 'dormiu', 'adormecer', 'adormecendo', 'adormecia',
                'despertar', 'despertando', 'despertava', 'despertou',
                'repouso', 'repousar', 'repousando', 'repousava',
                'descanso', 'descansar', 'descansando', 'descansava',
                'sonolência', 'sonolento', 'soneca', 'sonecar'
            ],
            'profético': [
                'visão', 'visões', 'profecia', 'profécias', 'profetizar', 'profetizando',
                'revelação', 'revelações', 'revelar', 'revelando', 'revelava',
                'aparição', 'aparições', 'aparecer', 'aparecendo', 'aparecia',
                'vaticínio', 'vaticínios', 'vaticinar', 'vaticinando', 'vaticinava',
                'presságio', 'presságios', 'pressagiar', 'pressagiando', 'pressagiava'
            ],
            'alegórico': [
                'sombra', 'sombras', 'fantasia', 'fantasias', 'ilusão', 'ilusões',
                'metáfora', 'metáforas', 'símbolo', 'símbolos', 'alegoria', 'alegorias'
            ],
            'divino': [
                'glória', 'glorioso', 'divino', 'divinos', 'celestial', 'celestiais',
                'milagre', 'milagres', 'milagroso', 'sagrado', 'sagrados', 'santo', 'santos'
            ],
            'ilusório': [
                'ilusão', 'ilusões', 'quimera', 'quimeras', 'miragem', 'miragens',
                'falsa', 'falso', 'falsos', 'falsas'
            ]
        }
        
        # Extrai apenas termos estritos
        sleep_terms = self._extract_terms_with_list(text, strict_terms)
        
        # Analisa coocorrência
        cooccurrence = self.analyze_cooccurrence(text)
        
        # Calcula similaridade semântica
        similarity = self.calculate_semantic_similarity(text)
        
        # Classifica contextos
        all_contexts = []
        for category, contexts in sleep_terms.items():
            all_contexts.extend(contexts)
        
        classified_contexts = self.classify_dream_contexts(all_contexts)
        
        return {
            'sleep_terms': sleep_terms,
            'cooccurrence': cooccurrence,
            'similarity': similarity,
            'classified_contexts': classified_contexts,
            'total_contexts': len(classified_contexts),
            'categories_found': list(sleep_terms.keys())
        }
    
    def _extract_terms_with_list(self, text: str, terms_dict: Dict[str, List[str]]) -> Dict[str, List[Dict]]:
        """
        Extrai termos usando uma lista específica de termos.
        
        Args:
            text: Texto para analisar
            terms_dict: Dicionário com termos por categoria
            
        Returns:
            Dicionário com termos encontrados
        """
        results = defaultdict(list)
        text_lower = text.lower()
        
        for category, terms in terms_dict.items():
            for term in terms:
                # Captura o termo exato e possíveis flexões
                pattern = re.compile(rf'\b{re.escape(term)}\w*\b', re.IGNORECASE)
                for match in pattern.finditer(text_lower):
                    # Extrai contexto (100 caracteres antes e depois)
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()
                    
                    # Identifica estrofe se possível
                    stanza = self._extract_stanza_number(text, match.start())
                    
                    results[category].append({
                        'term': match.group(0),
                        'context': context,
                        'text': context,
                        'excerpt': context,
                        'position': match.start(),
                        'stanza': stanza,
                        'category': category
                    })
        
        return dict(results)

def create_traditional_analyzer() -> TraditionalNLPAnalyzer:
    """Cria instância do analisador NLP tradicional."""
    return TraditionalNLPAnalyzer()

