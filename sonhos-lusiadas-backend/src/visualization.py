"""
Módulo de Visualização de Dados
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa

Este módulo é responsável por gerar visualizações dos dados analisados:
- Gráficos de frequência
- Distribuição por canto
- Classificação de tipos de sonho
- Word clouds
- Gráficos interativos
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from wordcloud import WordCloud
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do matplotlib para português
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (12, 8)

class DataVisualizer:
    """Classe para geração de visualizações."""
    
    def __init__(self, output_dir: str = "results/visualizations"):
        """
        Inicializa o visualizador.
        
        Args:
            output_dir: Diretório para salvar visualizações
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Configuração de cores
        self.colors = {
            'onírico': '#3B82F6',
            'profético': '#10B981',
            'alegórico': '#8B5CF6',
            'divino': '#F59E0B',
            'ilusão': '#EF4444',
            'não_classificado': '#6B7280'
        }
    
    def generate_word_frequency_chart(self, frequencies: Dict, filename: str = "word_frequency.png") -> str:
        """
        Gera gráfico de frequência de palavras.
        
        Args:
            frequencies: Dicionário com frequências
            filename: Nome do arquivo
            
        Returns:
            Caminho do arquivo gerado
        """
        if 'word_frequency' not in frequencies:
            logger.warning("Dados de frequência de palavras não encontrados.")
            return None
        
        df = frequencies['word_frequency']
        if df.empty:
            logger.warning("DataFrame de frequência vazio.")
            return None
        
        # Pega top 15 palavras
        top_words = df.head(15)
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(top_words)), top_words['count'])
        plt.yticks(range(len(top_words)), top_words.index)
        plt.xlabel('Frequência')
        plt.title('Frequência de Palavras Relacionadas a "Sonho"')
        plt.gca().invert_yaxis()
        
        # Adiciona valores nas barras
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                    str(int(width)), ha='left', va='center')
        
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Gráfico de frequência salvo em: {filepath}")
        return filepath
    
    def generate_canto_distribution_chart(self, frequencies: Dict, filename: str = "canto_distribution.png") -> str:
        """
        Gera gráfico de distribuição por canto.
        
        Args:
            frequencies: Dicionário com frequências
            filename: Nome do arquivo
            
        Returns:
            Caminho do arquivo gerado
        """
        if 'canto_frequency' not in frequencies:
            logger.warning("Dados de frequência por canto não encontrados.")
            return None
        
        df = frequencies['canto_frequency']
        if df.empty:
            logger.warning("DataFrame de frequência por canto vazio.")
            return None
        
        plt.figure(figsize=(12, 8))
        cantos = [f"Canto {i}" for i in df.index]
        bars = plt.bar(cantos, df['count'])
        
        plt.xlabel('Canto')
        plt.ylabel('Frequência')
        plt.title('Distribuição de Ocorrências por Canto')
        plt.xticks(rotation=45)
        
        # Adiciona valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    str(int(height)), ha='center', va='bottom')
        
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Gráfico de distribuição por canto salvo em: {filepath}")
        return filepath
    
    def generate_classification_chart(self, frequencies: Dict, filename: str = "classification_distribution.png") -> str:
        """
        Gera gráfico de distribuição por classificação.
        
        Args:
            frequencies: Dicionário com frequências
            filename: Nome do arquivo
            
        Returns:
            Caminho do arquivo gerado
        """
        if 'classification_frequency' not in frequencies:
            logger.warning("Dados de frequência por classificação não encontrados.")
            return None
        
        df = frequencies['classification_frequency']
        if df.empty:
            logger.warning("DataFrame de frequência por classificação vazio.")
            return None
        
        # Cria cores baseadas na classificação
        colors = [self.colors.get(classification, '#6B7280') for classification in df.index]
        
        plt.figure(figsize=(10, 8))
        wedges, texts, autotexts = plt.pie(df['count'], labels=df.index, colors=colors, 
                                          autopct='%1.1f%%', startangle=90)
        
        plt.title('Distribuição por Tipo de Sonho')
        
        # Melhora a aparência dos textos
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Gráfico de classificação salvo em: {filepath}")
        return filepath
    
    def generate_wordcloud(self, contexts_df: pd.DataFrame, filename: str = "wordcloud.png") -> str:
        """
        Gera word cloud dos contextos.
        
        Args:
            contexts_df: DataFrame com contextos
            filename: Nome do arquivo
            
        Returns:
            Caminho do arquivo gerado
        """
        if contexts_df.empty:
            logger.warning("DataFrame de contextos vazio.")
            return None
        
        # Combina todos os contextos
        all_contexts = ' '.join(contexts_df['context'].astype(str))
        
        # Remove palavras muito comuns
        stopwords = {'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'das', 'dos', 
                    'em', 'na', 'no', 'nas', 'nos', 'para', 'por', 'com', 'sem', 'sobre',
                    'que', 'quem', 'onde', 'quando', 'como', 'porque', 'mas', 'e', 'ou'}
        
        # Cria word cloud
        wordcloud = WordCloud(
            width=800, height=400,
            background_color='white',
            max_words=100,
            stopwords=stopwords,
            colormap='viridis'
        ).generate(all_contexts)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud - Contextos de "Sonho"')
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Word cloud salvo em: {filepath}")
        return filepath
    
    def generate_interactive_dashboard(self, contexts_df: pd.DataFrame, frequencies: Dict, 
                                     patterns: Dict, filename: str = "dashboard.html") -> str:
        """
        Gera dashboard interativo com Plotly.
        
        Args:
            contexts_df: DataFrame com contextos
            frequencies: Dicionário com frequências
            patterns: Dicionário com padrões
            filename: Nome do arquivo
            
        Returns:
            Caminho do arquivo gerado
        """
        # Cria subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Frequência de Palavras', 'Distribuição por Canto', 
                          'Classificação de Sonhos', 'Contextos por Canto'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "scatter"}]]
        )
        
        # Gráfico 1: Frequência de palavras
        if 'word_frequency' in frequencies and not frequencies['word_frequency'].empty:
            word_freq = frequencies['word_frequency'].head(10)
            fig.add_trace(
                go.Bar(x=word_freq['count'], y=word_freq.index, orientation='h'),
                row=1, col=1
            )
        
        # Gráfico 2: Distribuição por canto
        if 'canto_frequency' in frequencies and not frequencies['canto_frequency'].empty:
            canto_freq = frequencies['canto_frequency']
            fig.add_trace(
                go.Bar(x=[f"Canto {i}" for i in canto_freq.index], y=canto_freq['count']),
                row=1, col=2
            )
        
        # Gráfico 3: Classificação de sonhos
        if 'classification_frequency' in frequencies and not frequencies['classification_frequency'].empty:
            class_freq = frequencies['classification_frequency']
            colors = [self.colors.get(classification, '#6B7280') for classification in class_freq.index]
            fig.add_trace(
                go.Pie(labels=class_freq.index, values=class_freq['count'], 
                      marker_colors=colors),
                row=2, col=1
            )
        
        # Gráfico 4: Contextos por canto (scatter)
        if not contexts_df.empty and 'canto' in contexts_df.columns:
            canto_contexts = contexts_df.groupby('canto').size()
            fig.add_trace(
                go.Scatter(x=canto_contexts.index, y=canto_contexts.values, 
                          mode='markers+lines', name='Contextos por Canto'),
                row=2, col=2
            )
        
        # Atualiza layout
        fig.update_layout(
            title_text="Dashboard - Análise de 'Sonho' em Os Lusíadas",
            showlegend=False,
            height=800
        )
        
        filepath = os.path.join(self.output_dir, filename)
        fig.write_html(filepath)
        
        logger.info(f"Dashboard interativo salvo em: {filepath}")
        return filepath
    
    def generate_all_visualizations(self, contexts_df: pd.DataFrame, frequencies: Dict, 
                                   patterns: Dict) -> Dict[str, str]:
        """
        Gera todas as visualizações disponíveis.
        
        Args:
            contexts_df: DataFrame com contextos
            frequencies: Dicionário com frequências
            patterns: Dicionário com padrões
            
        Returns:
            Dicionário com caminhos dos arquivos gerados
        """
        generated_files = {}
        
        try:
            # Gráfico de frequência de palavras
            filepath = self.generate_word_frequency_chart(frequencies)
            if filepath:
                generated_files['word_frequency'] = filepath
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de frequência: {e}")
        
        try:
            # Gráfico de distribuição por canto
            filepath = self.generate_canto_distribution_chart(frequencies)
            if filepath:
                generated_files['canto_distribution'] = filepath
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de canto: {e}")
        
        try:
            # Gráfico de classificação
            filepath = self.generate_classification_chart(frequencies)
            if filepath:
                generated_files['classification_distribution'] = filepath
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de classificação: {e}")
        
        try:
            # Word cloud
            filepath = self.generate_wordcloud(contexts_df)
            if filepath:
                generated_files['wordcloud'] = filepath
        except Exception as e:
            logger.error(f"Erro ao gerar word cloud: {e}")
        
        try:
            # Dashboard interativo
            filepath = self.generate_interactive_dashboard(contexts_df, frequencies, patterns)
            if filepath:
                generated_files['interactive_dashboard'] = filepath
        except Exception as e:
            logger.error(f"Erro ao gerar dashboard: {e}")
        
        logger.info(f"Geradas {len(generated_files)} visualizações.")
        return generated_files

def create_visualization_report(generated_files: Dict[str, str], output_dir: str) -> str:
    """
    Cria relatório HTML com todas as visualizações.
    
    Args:
        generated_files: Dicionário com arquivos gerados
        output_dir: Diretório de saída
        
    Returns:
        Caminho do relatório HTML
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Visualizações - Sonhos Lusíadas</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { text-align: center; color: #2c3e50; }
            .section { margin: 30px 0; }
            .chart { text-align: center; margin: 20px 0; }
            .chart img { max-width: 100%; height: auto; }
            .chart h3 { color: #34495e; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌙 Relatório de Análise - Sonhos Lusíadas</h1>
            <p>Visualizações geradas automaticamente</p>
        </div>
    """
    
    # Adiciona cada visualização
    for chart_type, filepath in generated_files.items():
        if os.path.exists(filepath):
            filename = os.path.basename(filepath)
            if filename.endswith('.png'):
                html_content += f"""
                <div class="section">
                    <div class="chart">
                        <h3>{chart_type.replace('_', ' ').title()}</h3>
                        <img src="{filename}" alt="{chart_type}">
                    </div>
                </div>
                """
            elif filename.endswith('.html'):
                html_content += f"""
                <div class="section">
                    <div class="chart">
                        <h3>{chart_type.replace('_', ' ').title()}</h3>
                        <iframe src="{filename}" width="100%" height="600"></iframe>
                    </div>
                </div>
                """
    
    html_content += """
        <div class="section">
            <p><em>Relatório gerado automaticamente pelo sistema de análise literária.</em></p>
        </div>
    </body>
    </html>
    """
    
    report_path = os.path.join(output_dir, "relatorio_visualizacoes.html")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"Relatório HTML salvo em: {report_path}")
    return report_path


