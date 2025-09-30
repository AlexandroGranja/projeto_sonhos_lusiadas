"""
Módulo de Pré-processamento de Texto
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa

Este módulo é responsável por preparar o texto para análise, incluindo:
- Limpeza de texto
- Tokenização
- Lematização
- Remoção de stopwords
"""

import spacy
import re
import os
from typing import List, Dict, Optional
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextPreprocessor:
    """Classe para pré-processamento de texto."""
    
    def __init__(self, model_name: str = "pt_core_news_sm"):
        """
        Inicializa o preprocessador.
        
        Args:
            model_name: Nome do modelo spaCy para português
        """
        try:
            self.nlp = spacy.load(model_name)
            logger.info(f"Modelo spaCy '{model_name}' carregado com sucesso.")
        except OSError:
            logger.error(f"Modelo spaCy '{model_name}' não encontrado. "
                        "Execute: python -m spacy download pt_core_news_sm")
            # Usa modelo básico como fallback
            self.nlp = spacy.blank("pt")
            logger.warning("Usando modelo básico spaCy sem recursos avançados.")
        
        # Garante que as stopwords do NLTK estão disponíveis
        try:
            import nltk
            from nltk.corpus import stopwords
            stopwords.words("portuguese")
        except LookupError:
            import nltk
            nltk.download("stopwords")
        
        # Garante que o stemmer RSLP do NLTK está disponível
        try:
            from nltk.stem import RSLPStemmer
            self.stemmer = RSLPStemmer()
        except:
            logger.warning("Stemmer RSLP não disponível. Usando lemmatização do spaCy.")
            self.stemmer = None
    
    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e normalizando.
        
        Args:
            text: Texto original
            
        Returns:
            Texto limpo
        """
        # Remove caracteres especiais mas mantém acentos
        text = re.sub(r'[^\w\s\u00C0-\u017F]', ' ', text)
        
        # Remove espaços extras
        text = re.sub(r'\s+', ' ', text)
        
        # Remove quebras de linha
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        return text.strip()
    
    def preprocess(self, text: str) -> str:
        """
        Pré-processa o texto completo.
        
        Args:
            text: Texto original
            
        Returns:
            Texto pré-processado
        """
        # Limpa o texto
        cleaned_text = self.clean_text(text)
        
        # Processa com spaCy
        doc = self.nlp(cleaned_text)
        
        # Extrai tokens limpos
        tokens = []
        for token in doc:
            if not token.is_space and not token.is_punct:
                # Usa lemmatização se disponível
                if hasattr(token, 'lemma_') and token.lemma_:
                    tokens.append(token.lemma_.lower())
                else:
                    tokens.append(token.text.lower())
        
        return ' '.join(tokens)
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extrai sentenças do texto.
        
        Args:
            text: Texto original
            
        Returns:
            Lista de sentenças
        """
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    
    def extract_verses_by_canto(self, text: str) -> Dict[int, List[str]]:
        """
        Extrai versos organizados por canto (específico para Os Lusíadas).
        
        Args:
            text: Texto de Os Lusíadas
            
        Returns:
            Dicionário com cantos e seus versos
        """
        cantos = {}
        
        # Padrão para identificar cantos
        canto_pattern = re.compile(r'Canto\s+([IVX]+)', re.IGNORECASE)
        
        # Divide o texto em linhas
        lines = text.split('\n')
        
        current_canto = None
        current_verses = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Verifica se é início de canto
            canto_match = canto_pattern.search(line)
            if canto_match:
                # Salva canto anterior
                if current_canto is not None:
                    cantos[current_canto] = current_verses
                
                # Inicia novo canto
                current_canto = self._roman_to_int(canto_match.group(1))
                current_verses = []
            elif current_canto is not None and line:
                # Adiciona verso ao canto atual
                current_verses.append(line)
        
        # Salva último canto
        if current_canto is not None:
            cantos[current_canto] = current_verses
        
        return cantos
    
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

def process_lusiadas_text(text: str) -> Dict:
    """
    Processa texto de Os Lusíadas de forma específica.
    
    Args:
        text: Texto de Os Lusíadas
        
    Returns:
        Dicionário com dados processados
    """
    preprocessor = TextPreprocessor()
    
    # Processa texto
    processed_text = preprocessor.preprocess(text)
    sentences = preprocessor.extract_sentences(text)
    cantos = preprocessor.extract_verses_by_canto(text)
    
    return {
        'processed_text': processed_text,
        'sentences': sentences,
        'cantos': cantos,
        'total_words': len(processed_text.split()),
        'total_sentences': len(sentences),
        'total_cantos': len(cantos)
    }


