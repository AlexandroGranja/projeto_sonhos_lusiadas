"""
Módulo de Busca e Análise de Contexto
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa

Este módulo é responsável por:
- Buscar ocorrências das palavras expandidas no texto
- Extrair contextos relevantes
- Contar frequências por canto
- Classificar contextos usando Claude Sonnet 4
"""

import re
import pandas as pd
import os
import logging
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter
import json
import openai
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextAnalyzer:
    """Classe para análise de contexto e busca de padrões."""
    
    def __init__(self):
        """Inicializa o analisador de contexto."""
        self.openai_client = None
        self._setup_openai()
        self.results_cache = {}
    
    def _setup_openai(self):
        """Configura o cliente OpenAI."""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            try:
                openai.api_key = api_key
                self.openai_client = openai
                logger.info("Cliente OpenAI configurado para análise de contexto.")
            except Exception as e:
                logger.error(f"Erro ao configurar OpenAI: {e}")
                self.openai_client = None
        else:
            logger.warning("OPENAI_API_KEY não encontrada para análise de contexto.")
    
    def search_contexts(self, text: str, words: List[str], 
                       context_window: int = 100) -> pd.DataFrame:
        """
        Busca contextos das palavras no texto.
        
        Args:
            text: Texto para busca
            words: Lista de palavras para buscar
            context_window: Tamanho da janela de contexto (caracteres)
            
        Returns:
            DataFrame com palavras, contextos e posições
        """
        results = []
        
        for word in words:
            # Cria padrão de busca flexível
            pattern = re.compile(rf'\b\w*{re.escape(word)}\w*\b', re.IGNORECASE)
            
            for match in pattern.finditer(text):
                start = max(0, match.start() - context_window // 2)
                end = min(len(text), match.end() + context_window // 2)
                
                context = text[start:end].strip()
                
                # Extrai canto se possível
                canto = self._extract_canto_from_position(text, match.start())
                
                results.append({
                    'word': word,
                    'context': context,
                    'position': match.start(),
                    'canto': canto,
                    'match_text': match.group(),
                    'context_length': len(context)
                })
        
        if not results:
            return pd.DataFrame()
        
        return pd.DataFrame(results)
    
    def _extract_canto_from_position(self, text: str, position: int) -> Optional[int]:
        """
        Extrai o canto baseado na posição no texto.
        
        Args:
            text: Texto completo
            position: Posição da palavra
            
        Returns:
            Número do canto ou None
        """
        # Busca por padrões de canto antes da posição
        canto_pattern = re.compile(r'Canto\s+([IVX]+)', re.IGNORECASE)
        
        text_before = text[:position]
        cantos = list(canto_pattern.finditer(text_before))
        
        if cantos:
            last_canto = cantos[-1]
            return self._roman_to_int(last_canto.group(1))
        
        return None
    
    def _roman_to_int(self, roman: str) -> int:
        """Converte numeral romano para inteiro."""
        roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev_value = 0
        
        for char in reversed(roman):
            value = roman_numerals[char]
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        
        return result
    
    def classify_contexts_with_openai(self, contexts_df: pd.DataFrame) -> pd.DataFrame:
        """
        Classifica contextos usando OpenAI GPT-4.
        
        Args:
            contexts_df: DataFrame com contextos
            
        Returns:
            DataFrame com classificação adicionada
        """
        if not self.openai_client or contexts_df.empty:
            return contexts_df
        
        # Adiciona coluna de classificação
        contexts_df = contexts_df.copy()
        contexts_df['classification'] = 'não_classificado'
        contexts_df['confidence'] = 0.0
        
        # Processa em lotes para eficiência
        batch_size = 5
        for i in range(0, len(contexts_df), batch_size):
            batch = contexts_df.iloc[i:i+batch_size]
            
            try:
                classifications = self._classify_batch(batch)
                
                for j, classification in enumerate(classifications):
                    if i + j < len(contexts_df):
                        contexts_df.iloc[i + j, contexts_df.columns.get_loc('classification')] = classification['type']
                        contexts_df.iloc[i + j, contexts_df.columns.get_loc('confidence')] = classification['confidence']
                
                # Pequena pausa para evitar rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Erro na classificação do lote {i//batch_size + 1}: {e}")
        
        return contexts_df
    
    def _classify_batch(self, batch_df: pd.DataFrame) -> List[Dict]:
        """
        Classifica um lote de contextos.
        
        Args:
            batch_df: DataFrame com lote de contextos
            
        Returns:
            Lista de classificações
        """
        contexts_text = []
        for _, row in batch_df.iterrows():
            contexts_text.append(f"Palavra: {row['word']}\nContexto: {row['context']}")
        
        prompt = f"""
        Classifique os seguintes contextos de palavras relacionadas a "sonho" em Os Lusíadas:
        
        {chr(10).join(contexts_text)}
        
        Para cada contexto, identifique o tipo de sonho:
        1. "onírico" - sonhos, pesadelos, devaneios
        2. "profético" - visões, presságios, augúrios
        3. "alegórico" - símbolos, metáforas, alegorias
        4. "divino" - revelações, aparições divinas
        5. "ilusão" - quimeras, miragens, falsas aparências
        
        Retorne JSON com formato:
        [{{"type": "tipo", "confidence": 0.95}}, ...]
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            max_tokens=1000,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        try:
            # Extrai JSON da resposta
            json_text = response.choices[0].message.content
            json_match = re.search(r'\[.*\]', json_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback para classificação simples
                return [{"type": "não_classificado", "confidence": 0.0} for _ in range(len(batch_df))]
        except Exception as e:
            logger.error(f"Erro ao processar classificação: {e}")
            return [{"type": "não_classificado", "confidence": 0.0} for _ in range(len(batch_df))]
    
    def calculate_frequencies(self, contexts_df: pd.DataFrame) -> Dict:
        """
        Calcula frequências das palavras encontradas.
        
        Args:
            contexts_df: DataFrame com contextos
            
        Returns:
            Dicionário com frequências
        """
        if contexts_df.empty:
            return {}
        
        frequencies = {}
        
        # Frequência por palavra
        word_freq = contexts_df['word'].value_counts()
        frequencies['word_frequency'] = word_freq.to_frame('count')
        
        # Frequência por canto
        if 'canto' in contexts_df.columns:
            canto_freq = contexts_df.groupby('canto')['word'].count()
            frequencies['canto_frequency'] = canto_freq.to_frame('count')
        
        # Frequência por classificação
        if 'classification' in contexts_df.columns:
            class_freq = contexts_df['classification'].value_counts()
            frequencies['classification_frequency'] = class_freq.to_frame('count')
        
        # Frequência por palavra e canto
        if 'canto' in contexts_df.columns:
            word_canto_freq = contexts_df.groupby(['word', 'canto']).size().unstack(fill_value=0)
            frequencies['word_canto_frequency'] = word_canto_freq
        
        return frequencies
    
    def analyze_patterns(self, contexts_df: pd.DataFrame) -> Dict:
        """
        Analisa padrões nos contextos encontrados.
        
        Args:
            contexts_df: DataFrame com contextos
            
        Returns:
            Dicionário com padrões identificados
        """
        if contexts_df.empty:
            return {}
        
        patterns = {}
        
        # Padrões de palavras mais frequentes
        top_words = contexts_df['word'].value_counts().head(10)
        patterns['top_words'] = top_words.to_dict()
        
        # Padrões por canto
        if 'canto' in contexts_df.columns:
            canto_patterns = contexts_df.groupby('canto')['word'].apply(list).to_dict()
            patterns['canto_patterns'] = canto_patterns
        
        # Padrões de classificação
        if 'classification' in contexts_df.columns:
            class_patterns = contexts_df.groupby('classification')['word'].apply(list).to_dict()
            patterns['classification_patterns'] = class_patterns
        
        # Padrões de contexto (palavras que aparecem juntas)
        context_words = []
        for context in contexts_df['context']:
            words = re.findall(r'\b\w+\b', context.lower())
            context_words.extend(words)
        
        word_cooccurrence = Counter(context_words)
        patterns['context_cooccurrence'] = dict(word_cooccurrence.most_common(20))
        
        return patterns

def run_complete_analysis(text: str, words: List[str]) -> Dict:
    """
    Executa análise completa do texto.
    
    Args:
        text: Texto para análise
        words: Lista de palavras para buscar
        
    Returns:
        Dicionário com resultados completos
    """
    analyzer = ContextAnalyzer()
    
    # Busca contextos
    contexts_df = analyzer.search_contexts(text, words)
    
    if contexts_df.empty:
        return {
            'contexts': [],
            'frequencies': {},
            'patterns': {},
            'message': 'Nenhum contexto encontrado'
        }
    
    # Classifica contextos
    contexts_df = analyzer.classify_contexts_with_claude(contexts_df)
    
    # Calcula frequências
    frequencies = analyzer.calculate_frequencies(contexts_df)
    
    # Analisa padrões
    patterns = analyzer.analyze_patterns(contexts_df)
    
    return {
        'contexts': contexts_df.to_dict('records'),
        'frequencies': {k: v.to_dict() if hasattr(v, 'to_dict') else v for k, v in frequencies.items()},
        'patterns': patterns,
        'total_contexts': len(contexts_df),
        'unique_words': contexts_df['word'].nunique()
    }


