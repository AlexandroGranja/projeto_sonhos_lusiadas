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
            logger.error(f"Modelo spaCy \'{model_name}\' não encontrado. "
                        "Execute: python -m spacy download pt_core_news_sm")
            raise
        
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
            RSLPStemmer()
        except LookupError:
            import nltk
            nltk.download("rslp")
    
    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e normalizando.
        
        Args:
            text: Texto bruto para limpeza
            
        Returns:
            Texto limpo
        """
        # Remove quebras de linha excessivas
        text = re.sub(r'\n+', ' ', text)
        
        # Remove caracteres especiais, mantendo apenas letras, números e espaços
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remove números
        text = re.sub(r'\d+', '', text)
        
        # Converte para minúsculas
        text = text.lower()
        
        # Remove espaços excessivos
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def preprocess(self, text: str, remove_stopwords: bool = True) -> str:
        """
        Processa o texto completo: limpeza, tokenização e lematização.
        
        Args:
            text: Texto bruto para processamento
            remove_stopwords: Se deve remover stopwords
            
        Returns:
            Texto processado
        """
        # Limpa o texto
        cleaned_text = self.clean_text(text)
        
        # Processa com spaCy
        doc = self.nlp(cleaned_text)
        
        # Extrai tokens processados
        tokens = []
        for token in doc:
            # Pula stopwords se solicitado
            if remove_stopwords and token.is_stop:
                continue
            
            # Pula pontuação e espaços
            if token.is_punct or token.is_space:
                continue
            
            # Pula tokens muito curtos
            if len(token.lemma_) < 2:
                continue
            
            tokens.append(token.lemma_)
        
        return " ".join(tokens)
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extrai sentenças do texto.
        
        Args:
            text: Texto para extração de sentenças
            
        Returns:
            Lista de sentenças
        """
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]
    
    def extract_verses_by_canto(self, text: str) -> Dict[int, List[str]]:
        """
        Extrai versos organizados por canto de Os Lusíadas.
        
        Args:
            text: Texto completo de Os Lusíadas
            
        Returns:
            Dicionário com cantos e seus versos
        """
        cantos = {}
        current_canto = 0
        
        lines = text.split('\n')
        current_verses = []
        
        for line in lines:
            line = line.strip()
            
            # Detecta início de novo canto
            canto_match = re.search(r'canto\s+([ivxlc]+)', line.lower())
            if canto_match:
                # Salva canto anterior se existir
                if current_canto > 0 and current_verses:
                    cantos[current_canto] = current_verses
                
                # Converte número romano para arábico
                roman_num = canto_match.group(1)
                current_canto = self._roman_to_int(roman_num)
                current_verses = []
                continue
            
            # Adiciona verso se não estiver vazio e for significativo
            if line and len(line) > 10 and not line.startswith('***'):
                current_verses.append(line)
        
        # Adiciona último canto
        if current_canto > 0 and current_verses:
            cantos[current_canto] = current_verses
        
        return cantos
    
    def _roman_to_int(self, roman: str) -> int:
        """Converte número romano para inteiro."""
        roman_numerals = {
            'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100
        }
        
        roman = roman.lower()
        total = 0
        prev_value = 0
        
        for char in reversed(roman):
            value = roman_numerals.get(char, 0)
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value
        
        return total

def process_lusiadas_text(input_path: str, output_path: str) -> Dict:
    """
    Processa o texto de Os Lusíadas e salva o resultado.
    
    Args:
        input_path: Caminho para o arquivo de entrada
        output_path: Caminho para o arquivo de saída
        
    Returns:
        Estatísticas do processamento
    """
    preprocessor = TextPreprocessor()
    
    # Carrega o texto
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    logger.info(f"Texto carregado: {len(text)} caracteres")
    
    # Extrai versos por canto
    cantos = preprocessor.extract_verses_by_canto(text)
    logger.info(f"Encontrados {len(cantos)} cantos")
    
    # Processa o texto completo
    processed_text = preprocessor.preprocess(text)
    
    # Salva texto processado
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(processed_text)
    
    # Salva versos por canto
    cantos_path = output_path.replace('.txt', '_cantos.txt')
    with open(cantos_path, 'w', encoding='utf-8') as f:
        for canto, versos in cantos.items():
            f.write(f"=== CANTO {canto} ===\n")
            for verso in versos:
                f.write(f"{verso}\n")
            f.write("\n")
    
    stats = {
        'original_chars': len(text),
        'processed_chars': len(processed_text),
        'cantos_found': len(cantos),
        'total_verses': sum(len(versos) for versos in cantos.values())
    }
    
    logger.info(f"Processamento concluído: {stats}")
    return stats

if __name__ == "__main__":
    # Exemplo de uso
    input_file = "../data/raw/os_lusiadas.txt"
    output_file = "../data/processed/os_lusiadas_clean.txt"
    
    if os.path.exists(input_file):
        stats = process_lusiadas_text(input_file, output_file)
        print(f"Processamento concluído: {stats}")
    else:
        print(f"Arquivo não encontrado: {input_file}")
