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
from semantic_expansion import SemanticExpander

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextAnalyzer:
    """Classe para análise de contexto e busca de padrões."""
    
    def __init__(self):
        """Inicializa o analisador de contexto."""
        self.semantic_expander = SemanticExpander()
        self.results_cache = {}
    
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
                start_pos = max(0, match.start() - context_window)
                end_pos = min(len(text), match.end() + context_window)
                
                context = text[start_pos:end_pos].strip()
                matched_word = match.group()
                
                # Calcula posição relativa no texto
                relative_position = match.start() / len(text)
                
                results.append({
                    'word': word,
                    'matched_form': matched_word,
                    'context': context,
                    'position': match.start(),
                    'relative_position': relative_position,
                    'context_length': len(context)
                })
        
        df = pd.DataFrame(results)
        logger.info(f"Encontradas {len(df)} ocorrências de {len(words)} palavras.")
        
        return df
    
    def search_contexts_by_canto(self, cantos_dict: Dict[int, List[str]], 
                                words: List[str]) -> pd.DataFrame:
        """
        Busca contextos organizados por canto.
        
        Args:
            cantos_dict: Dicionário com cantos e versos
            words: Lista de palavras para buscar
            
        Returns:
            DataFrame com contextos por canto
        """
        results = []
        
        for canto_num, versos in cantos_dict.items():
            canto_text = " ".join(versos)
            
            for word in words:
                pattern = re.compile(rf'\b\w*{re.escape(word)}\w*\b', re.IGNORECASE)
                
                for match in pattern.finditer(canto_text):
                    # Encontra o verso específico
                    char_pos = match.start()
                    current_pos = 0
                    verso_num = 0
                    
                    for i, verso in enumerate(versos):
                        if current_pos <= char_pos < current_pos + len(verso):
                            verso_num = i + 1
                            break
                        current_pos += len(verso) + 1  # +1 para o espaço
                    
                    # Contexto: verso atual + anterior + próximo
                    context_versos = []
                    for j in range(max(0, verso_num-2), min(len(versos), verso_num+2)):
                        context_versos.append(versos[j])
                    
                    context = " ".join(context_versos)
                    matched_word = match.group()
                    
                    results.append({
                        'word': word,
                        'matched_form': matched_word,
                        'canto': canto_num,
                        'verso': verso_num,
                        'context': context,
                        'verso_text': versos[verso_num-1] if verso_num > 0 else "",
                        'position_in_canto': match.start()
                    })
        
        df = pd.DataFrame(results)
        logger.info(f"Encontradas {len(df)} ocorrências em {len(cantos_dict)} cantos.")
        
        return df
    
    def classify_contexts_with_claude(self, df: pd.DataFrame, 
                                    batch_size: int = 10) -> pd.DataFrame:
        """
        Classifica contextos usando Claude Sonnet 4.
        
        Args:
            df: DataFrame com contextos
            batch_size: Tamanho do lote para processamento
            
        Returns:
            DataFrame com classificações adicionadas
        """
        if df.empty:
            return df
        
        # Adiciona colunas para classificação
        df['dream_type'] = 'unknown'
        df['confidence'] = 'baixa'
        df['literary_analysis'] = ''
        df['literary_function'] = ''
        
        # Processa em lotes para evitar sobrecarga da API
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            for idx, row in batch.iterrows():
                try:
                    analysis = self.semantic_expander.analyze_dream_context_with_claude(
                        row['context']
                    )
                    
                    df.at[idx, 'dream_type'] = analysis.get('type', 'unknown')
                    df.at[idx, 'confidence'] = analysis.get('confidence', 'baixa')
                    df.at[idx, 'literary_analysis'] = analysis.get('analysis', '')
                    df.at[idx, 'literary_function'] = analysis.get('literary_function', '')
                    
                    logger.info(f"Classificado contexto {idx+1}/{len(df)}")
                    
                except Exception as e:
                    logger.error(f"Erro ao classificar contexto {idx}: {e}")
                    continue
        
        return df
    
    def calculate_frequencies(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Calcula frequências de diferentes formas.
        
        Args:
            df: DataFrame com contextos
            
        Returns:
            Dicionário com diferentes análises de frequência
        """
        frequencies = {}
        
        # Frequência por palavra
        word_freq = df['word'].value_counts().reset_index()
        word_freq.columns = ['word', 'frequency']
        frequencies['by_word'] = word_freq
        
        # Frequência por canto (se disponível)
        if 'canto' in df.columns:
            canto_freq = df['canto'].value_counts().sort_index().reset_index()
            canto_freq.columns = ['canto', 'frequency']
            frequencies['by_canto'] = canto_freq
            
            # Frequência por palavra e canto
            word_canto_freq = df.groupby(['word', 'canto']).size().reset_index(name='frequency')
            frequencies['by_word_canto'] = word_canto_freq
        
        # Frequência por tipo de sonho (se classificado)
        if 'dream_type' in df.columns:
            type_freq = df['dream_type'].value_counts().reset_index()
            type_freq.columns = ['dream_type', 'frequency']
            frequencies['by_dream_type'] = type_freq
        
        # Estatísticas gerais
        stats = {
            'total_occurrences': len(df),
            'unique_words': df['word'].nunique(),
            'unique_contexts': df['context'].nunique(),
            'avg_context_length': df['context_length'].mean() if 'context_length' in df.columns else 0
        }
        
        if 'canto' in df.columns:
            stats['cantos_with_occurrences'] = df['canto'].nunique()
            stats['avg_occurrences_per_canto'] = len(df) / df['canto'].nunique()
        
        frequencies['statistics'] = pd.DataFrame([stats])
        
        logger.info(f"Calculadas frequências: {list(frequencies.keys())}")
        
        return frequencies
    
    def analyze_patterns(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Analisa padrões nos dados.
        
        Args:
            df: DataFrame com contextos
            
        Returns:
            Dicionário com análises de padrões
        """
        patterns = {}
        
        # Padrões de distribuição
        if 'relative_position' in df.columns:
            # Divide o texto em seções
            df['text_section'] = pd.cut(df['relative_position'], 
                                      bins=10, labels=range(1, 11))
            section_dist = df['text_section'].value_counts().sort_index()
            patterns['distribution_by_section'] = section_dist.to_dict()
        
        # Padrões de co-ocorrência
        if 'canto' in df.columns:
            # Palavras que aparecem no mesmo canto
            canto_words = df.groupby('canto')['word'].apply(list).to_dict()
            cooccurrence = defaultdict(int)
            
            for canto, words in canto_words.items():
                word_pairs = [(w1, w2) for i, w1 in enumerate(words) 
                             for w2 in words[i+1:]]
                for pair in word_pairs:
                    cooccurrence[tuple(sorted(pair))] += 1
            
            patterns['word_cooccurrence'] = dict(cooccurrence)
        
        # Padrões de tipos de sonho por canto
        if 'dream_type' in df.columns and 'canto' in df.columns:
            type_by_canto = df.groupby(['canto', 'dream_type']).size().unstack(fill_value=0)
            patterns['dream_types_by_canto'] = type_by_canto.to_dict()
        
        # Análise de sentimento/tom (básica)
        positive_words = ['glória', 'visão', 'revelação', 'profecia']
        negative_words = ['pesadelo', 'sombra', 'ilusão', 'engano']
        
        df['sentiment'] = 'neutral'
        for idx, row in df.iterrows():
            context_lower = row['context'].lower()
            if any(word in context_lower for word in positive_words):
                df.at[idx, 'sentiment'] = 'positive'
            elif any(word in context_lower for word in negative_words):
                df.at[idx, 'sentiment'] = 'negative'
        
        sentiment_dist = df['sentiment'].value_counts().to_dict()
        patterns['sentiment_distribution'] = sentiment_dist
        
        logger.info(f"Analisados padrões: {list(patterns.keys())}")
        
        return patterns
    
    def save_analysis_results(self, df: pd.DataFrame, frequencies: Dict, 
                            patterns: Dict, output_dir: str):
        """
        Salva todos os resultados da análise.
        
        Args:
            df: DataFrame principal com contextos
            frequencies: Análises de frequência
            patterns: Análises de padrões
            output_dir: Diretório de saída
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Salva DataFrame principal
        main_file = os.path.join(output_dir, 'contexts_analysis.csv')
        df.to_csv(main_file, index=False, encoding='utf-8')
        
        # Salva frequências
        freq_dir = os.path.join(output_dir, 'frequencies')
        os.makedirs(freq_dir, exist_ok=True)
        
        for name, freq_df in frequencies.items():
            if isinstance(freq_df, pd.DataFrame):
                freq_file = os.path.join(freq_dir, f'{name}.csv')
                freq_df.to_csv(freq_file, index=False, encoding='utf-8')
        
        # Salva padrões em JSON
        patterns_file = os.path.join(output_dir, 'patterns_analysis.json')
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, ensure_ascii=False, indent=2, default=str)
        
        # Salva resumo executivo
        summary_file = os.path.join(output_dir, 'analysis_summary.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=== RESUMO DA ANÁLISE ===\n\n")
            
            if 'statistics' in frequencies:
                stats = frequencies['statistics'].iloc[0].to_dict()
                f.write("ESTATÍSTICAS GERAIS:\n")
                for key, value in stats.items():
                    f.write(f"- {key}: {value}\n")
                f.write("\n")
            
            f.write("PALAVRAS MAIS FREQUENTES:\n")
            if 'by_word' in frequencies:
                top_words = frequencies['by_word'].head(10)
                for _, row in top_words.iterrows():
                    f.write(f"- {row['word']}: {row['frequency']} ocorrências\n")
                f.write("\n")
            
            if 'dream_types_by_canto' in patterns:
                f.write("DISTRIBUIÇÃO DE TIPOS DE SONHO POR CANTO:\n")
                f.write(str(patterns['dream_types_by_canto']))
                f.write("\n\n")
        
        logger.info(f"Resultados salvos em: {output_dir}")

def run_complete_analysis(text_file: str, cantos_file: str, 
                         words_file: str, output_dir: str) -> Dict:
    """
    Executa análise completa do texto.
    
    Args:
        text_file: Arquivo com texto processado
        cantos_file: Arquivo com cantos organizados
        words_file: Arquivo com palavras expandidas
        output_dir: Diretório de saída
        
    Returns:
        Dicionário com resultados da análise
    """
    analyzer = ContextAnalyzer()
    
    # Carrega dados
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Carrega palavras expandidas
    if words_file.endswith('.json'):
        with open(words_file, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
            words = words_data.get('combined_expansion', [])
    else:
        words_df = pd.read_csv(words_file)
        words = words_df['palavra'].tolist() if 'palavra' in words_df.columns else []
    
    # Busca contextos
    df = analyzer.search_contexts(text, words)
    
    # Se tiver arquivo de cantos, faz análise por canto também
    if os.path.exists(cantos_file):
        # Implementar carregamento de cantos do arquivo
        pass
    
    # Classifica contextos com Claude
    df = analyzer.classify_contexts_with_claude(df)
    
    # Calcula frequências
    frequencies = analyzer.calculate_frequencies(df)
    
    # Analisa padrões
    patterns = analyzer.analyze_patterns(df)
    
    # Salva resultados
    analyzer.save_analysis_results(df, frequencies, patterns, output_dir)
    
    return {
        'contexts_df': df,
        'frequencies': frequencies,
        'patterns': patterns,
        'summary': {
            'total_contexts': len(df),
            'unique_words': df['word'].nunique(),
            'analysis_complete': True
        }
    }

if __name__ == "__main__":
    # Exemplo de uso
    text_file = "../data/processed/os_lusiadas_clean.txt"
    cantos_file = "../data/processed/os_lusiadas_clean_cantos.txt"
    words_file = "../results/expanded_words.json"
    output_dir = "../results/analysis"
    
    if all(os.path.exists(f) for f in [text_file, words_file]):
        results = run_complete_analysis(text_file, cantos_file, words_file, output_dir)
        print(f"Análise concluída: {results['summary']}")
    else:
        print("Arquivos necessários não encontrados. Execute os módulos anteriores primeiro.")
