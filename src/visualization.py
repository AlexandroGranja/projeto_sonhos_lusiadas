"""
Módulo de Visualização de Dados
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa

Este módulo é responsável por gerar visualizações dos resultados da análise:
- Gráficos de frequência
- Nuvens de palavras
- Gráficos de distribuição por canto
- Redes de co-ocorrência
- Dashboards interativos
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
import os
import logging
from typing import Dict, List, Tuple, Optional
import json

# Configuração de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataVisualizer:
    """Classe para visualização de dados da análise literária."""
    
    def __init__(self, output_dir: str = "../results/visualizations"):
        """
        Inicializa o visualizador.
        
        Args:
            output_dir: Diretório para salvar visualizações
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Configurações de estilo
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#C73E1D',
            'neutral': '#6C757D'
        }
        
        # Configuração matplotlib para português
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16
    
    def plot_word_frequency(self, df: pd.DataFrame, top_n: int = 20, 
                           save_name: str = "word_frequency.png") -> str:
        """
        Cria gráfico de frequência de palavras.
        
        Args:
            df: DataFrame com colunas 'word' e 'frequency'
            top_n: Número de palavras mais frequentes
            save_name: Nome do arquivo para salvar
            
        Returns:
            Caminho do arquivo salvo
        """
        plt.figure(figsize=(12, 8))
        
        # Seleciona top N palavras
        top_words = df.head(top_n)
        
        # Cria gráfico de barras
        bars = plt.bar(range(len(top_words)), top_words['frequency'], 
                      color=self.colors['primary'], alpha=0.8)
        
        # Personaliza o gráfico
        plt.title(f'Frequência das {top_n} Palavras Mais Comuns Relacionadas a "Sonho"', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Palavras', fontsize=12)
        plt.ylabel('Frequência', fontsize=12)
        
        # Configura eixo X
        plt.xticks(range(len(top_words)), top_words['word'], 
                  rotation=45, ha='right')
        
        # Adiciona valores nas barras
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Salva o gráfico
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Gráfico de frequência salvo em: {save_path}")
        return save_path
    
    def create_wordcloud(self, text_data: str, save_name: str = "wordcloud.png") -> str:
        """
        Cria nuvem de palavras.
        
        Args:
            text_data: Texto para gerar a nuvem
            save_name: Nome do arquivo para salvar
            
        Returns:
            Caminho do arquivo salvo
        """
        # Configuração da nuvem de palavras
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5,
            random_state=42
        ).generate(text_data)
        
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nuvem de Palavras: Tema "Sonho" em Os Lusíadas', 
                 fontsize=18, fontweight='bold', pad=20)
        
        # Salva a nuvem
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Nuvem de palavras salva em: {save_path}")
        return save_path
    
    def plot_canto_distribution(self, df: pd.DataFrame, 
                               save_name: str = "canto_distribution.png") -> str:
        """
        Cria gráfico de distribuição por canto.
        
        Args:
            df: DataFrame com colunas 'canto' e 'frequency'
            save_name: Nome do arquivo para salvar
            
        Returns:
            Caminho do arquivo salvo
        """
        plt.figure(figsize=(14, 8))
        
        # Cria gráfico de linha e barras
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Gráfico de barras
        bars = ax1.bar(df['canto'], df['frequency'], 
                      color=self.colors['secondary'], alpha=0.7)
        ax1.set_title('Distribuição de Ocorrências por Canto', 
                     fontsize=14, fontweight='bold')
        ax1.set_xlabel('Canto')
        ax1.set_ylabel('Número de Ocorrências')
        ax1.grid(True, alpha=0.3)
        
        # Adiciona valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Gráfico de linha (tendência)
        ax2.plot(df['canto'], df['frequency'], 
                marker='o', linewidth=2, markersize=6,
                color=self.colors['accent'])
        ax2.fill_between(df['canto'], df['frequency'], alpha=0.3,
                        color=self.colors['accent'])
        ax2.set_title('Tendência de Ocorrências ao Longo dos Cantos', 
                     fontsize=14, fontweight='bold')
        ax2.set_xlabel('Canto')
        ax2.set_ylabel('Número de Ocorrências')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salva o gráfico
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Gráfico de distribuição por canto salvo em: {save_path}")
        return save_path
    
    def plot_dream_types(self, df: pd.DataFrame, 
                        save_name: str = "dream_types.png") -> str:
        """
        Cria gráfico de tipos de sonho.
        
        Args:
            df: DataFrame com colunas 'dream_type' e 'frequency'
            save_name: Nome do arquivo para salvar
            
        Returns:
            Caminho do arquivo salvo
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Gráfico de pizza
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['accent'], self.colors['success'], 
                 self.colors['neutral']]
        
        wedges, texts, autotexts = ax1.pie(df['frequency'], 
                                          labels=df['dream_type'],
                                          autopct='%1.1f%%',
                                          colors=colors[:len(df)],
                                          startangle=90)
        ax1.set_title('Distribuição dos Tipos de Sonho', 
                     fontsize=14, fontweight='bold')
        
        # Gráfico de barras horizontais
        bars = ax2.barh(df['dream_type'], df['frequency'], 
                       color=colors[:len(df)], alpha=0.8)
        ax2.set_title('Frequência dos Tipos de Sonho', 
                     fontsize=14, fontweight='bold')
        ax2.set_xlabel('Número de Ocorrências')
        
        # Adiciona valores nas barras
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                    f'{int(width)}', ha='left', va='center')
        
        plt.tight_layout()
        
        # Salva o gráfico
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Gráfico de tipos de sonho salvo em: {save_path}")
        return save_path
    
    def create_cooccurrence_network(self, cooccurrence_data: Dict[Tuple[str, str], int],
                                   save_name: str = "cooccurrence_network.png") -> str:
        """
        Cria rede de co-ocorrência de palavras.
        
        Args:
            cooccurrence_data: Dicionário com pares de palavras e frequências
            save_name: Nome do arquivo para salvar
            
        Returns:
            Caminho do arquivo salvo
        """
        # Cria grafo
        G = nx.Graph()
        
        # Adiciona arestas com pesos
        for (word1, word2), weight in cooccurrence_data.items():
            if weight > 1:  # Filtra co-ocorrências muito raras
                G.add_edge(word1, word2, weight=weight)
        
        if len(G.nodes()) == 0:
            logger.warning("Nenhuma co-ocorrência significativa encontrada.")
            return ""
        
        plt.figure(figsize=(16, 12))
        
        # Layout do grafo
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Desenha nós
        node_sizes = [G.degree(node) * 300 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                              node_color=self.colors['primary'],
                              alpha=0.7)
        
        # Desenha arestas
        edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos, width=[w/2 for w in edge_weights],
                              alpha=0.5, edge_color=self.colors['neutral'])
        
        # Adiciona rótulos
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title('Rede de Co-ocorrência de Palavras Relacionadas a "Sonho"',
                 fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        
        # Salva o gráfico
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Rede de co-ocorrência salva em: {save_path}")
        return save_path
    
    def create_interactive_dashboard(self, contexts_df: pd.DataFrame,
                                   frequencies: Dict, patterns: Dict,
                                   save_name: str = "interactive_dashboard.html") -> str:
        """
        Cria dashboard interativo com Plotly.
        
        Args:
            contexts_df: DataFrame principal com contextos
            frequencies: Dicionário com análises de frequência
            patterns: Dicionário com análises de padrões
            save_name: Nome do arquivo HTML para salvar
            
        Returns:
            Caminho do arquivo salvo
        """
        # Cria subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Frequência de Palavras', 'Distribuição por Canto',
                           'Tipos de Sonho', 'Distribuição Temporal'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "scatter"}]]
        )
        
        # Gráfico 1: Frequência de palavras
        if 'by_word' in frequencies:
            word_freq = frequencies['by_word'].head(15)
            fig.add_trace(
                go.Bar(x=word_freq['word'], y=word_freq['frequency'],
                      name='Frequência', marker_color=self.colors['primary']),
                row=1, col=1
            )
        
        # Gráfico 2: Distribuição por canto
        if 'by_canto' in frequencies:
            canto_freq = frequencies['by_canto']
            fig.add_trace(
                go.Bar(x=canto_freq['canto'], y=canto_freq['frequency'],
                      name='Por Canto', marker_color=self.colors['secondary']),
                row=1, col=2
            )
        
        # Gráfico 3: Tipos de sonho
        if 'by_dream_type' in frequencies:
            dream_freq = frequencies['by_dream_type']
            fig.add_trace(
                go.Pie(labels=dream_freq['dream_type'], values=dream_freq['frequency'],
                      name='Tipos'),
                row=2, col=1
            )
        
        # Gráfico 4: Distribuição temporal
        if 'relative_position' in contexts_df.columns:
            fig.add_trace(
                go.Scatter(x=contexts_df['relative_position'], 
                          y=contexts_df.index,
                          mode='markers',
                          name='Posição no Texto',
                          marker=dict(color=self.colors['accent'])),
                row=2, col=2
            )
        
        # Atualiza layout
        fig.update_layout(
            title_text="Dashboard Interativo: Análise de Sonhos em Os Lusíadas",
            title_x=0.5,
            height=800,
            showlegend=False
        )
        
        # Salva dashboard
        save_path = os.path.join(self.output_dir, save_name)
        fig.write_html(save_path)
        
        logger.info(f"Dashboard interativo salvo em: {save_path}")
        return save_path
    
    def create_heatmap_analysis(self, word_canto_df: pd.DataFrame,
                               save_name: str = "heatmap_analysis.png") -> str:
        """
        Cria heatmap de palavras por canto.
        
        Args:
            word_canto_df: DataFrame com colunas 'word', 'canto', 'frequency'
            save_name: Nome do arquivo para salvar
            
        Returns:
            Caminho do arquivo salvo
        """
        # Cria matriz pivot
        pivot_table = word_canto_df.pivot(index='word', columns='canto', 
                                         values='frequency').fillna(0)
        
        plt.figure(figsize=(16, 10))
        
        # Cria heatmap
        sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd',
                   cbar_kws={'label': 'Frequência'})
        
        plt.title('Heatmap: Distribuição de Palavras por Canto',
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Canto', fontsize=12)
        plt.ylabel('Palavra', fontsize=12)
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        
        # Salva o heatmap
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Heatmap salvo em: {save_path}")
        return save_path
    
    def generate_all_visualizations(self, contexts_df: pd.DataFrame,
                                  frequencies: Dict, patterns: Dict) -> Dict[str, str]:
        """
        Gera todas as visualizações disponíveis.
        
        Args:
            contexts_df: DataFrame principal com contextos
            frequencies: Dicionário com análises de frequência
            patterns: Dicionário com análises de padrões
            
        Returns:
            Dicionário com caminhos dos arquivos gerados
        """
        generated_files = {}
        
        try:
            # Gráfico de frequência de palavras
            if 'by_word' in frequencies:
                path = self.plot_word_frequency(frequencies['by_word'])
                generated_files['word_frequency'] = path
            
            # Nuvem de palavras
            if not contexts_df.empty:
                text_data = ' '.join(contexts_df['context'].astype(str))
                path = self.create_wordcloud(text_data)
                generated_files['wordcloud'] = path
            
            # Distribuição por canto
            if 'by_canto' in frequencies:
                path = self.plot_canto_distribution(frequencies['by_canto'])
                generated_files['canto_distribution'] = path
            
            # Tipos de sonho
            if 'by_dream_type' in frequencies:
                path = self.plot_dream_types(frequencies['by_dream_type'])
                generated_files['dream_types'] = path
            
            # Rede de co-ocorrência
            if 'word_cooccurrence' in patterns:
                path = self.create_cooccurrence_network(patterns['word_cooccurrence'])
                if path:
                    generated_files['cooccurrence_network'] = path
            
            # Heatmap
            if 'by_word_canto' in frequencies:
                path = self.create_heatmap_analysis(frequencies['by_word_canto'])
                generated_files['heatmap'] = path
            
            # Dashboard interativo
            path = self.create_interactive_dashboard(contexts_df, frequencies, patterns)
            generated_files['interactive_dashboard'] = path
            
        except Exception as e:
            logger.error(f"Erro ao gerar visualizações: {e}")
        
        logger.info(f"Geradas {len(generated_files)} visualizações.")
        return generated_files

def create_visualization_report(generated_files: Dict[str, str], 
                              output_dir: str) -> str:
    """
    Cria relatório HTML com todas as visualizações.
    
    Args:
        generated_files: Dicionário com caminhos dos arquivos gerados
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
        <title>Relatório de Visualizações - Sonhos em Os Lusíadas</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #2E86AB; text-align: center; }
            h2 { color: #A23B72; border-bottom: 2px solid #A23B72; padding-bottom: 10px; }
            .visualization { margin: 30px 0; text-align: center; }
            img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; }
            .description { margin: 15px 0; font-style: italic; color: #666; }
        </style>
    </head>
    <body>
        <h1>Análise Visual: Tema "Sonho" em Os Lusíadas</h1>
        <p><strong>Projeto:</strong> Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa</p>
        <p><strong>Autor:</strong> Sistema de Análise Literária com IA</p>
        <p><strong>Data:</strong> """ + pd.Timestamp.now().strftime('%d/%m/%Y') + """</p>
    """
    
    # Adiciona cada visualização
    visualization_descriptions = {
        'word_frequency': 'Frequência das palavras mais comuns relacionadas ao tema "sonho"',
        'wordcloud': 'Nuvem de palavras destacando os termos mais relevantes',
        'canto_distribution': 'Distribuição das ocorrências ao longo dos cantos',
        'dream_types': 'Classificação dos tipos de sonho encontrados',
        'heatmap': 'Mapa de calor mostrando a relação entre palavras e cantos',
        'cooccurrence_network': 'Rede de co-ocorrência entre palavras relacionadas'
    }
    
    for key, path in generated_files.items():
        if key in visualization_descriptions and path.endswith('.png'):
            filename = os.path.basename(path)
            html_content += f"""
            <div class="visualization">
                <h2>{visualization_descriptions[key]}</h2>
                <img src="{filename}" alt="{visualization_descriptions[key]}">
                <div class="description">{visualization_descriptions[key]}</div>
            </div>
            """
    
    # Link para dashboard interativo
    if 'interactive_dashboard' in generated_files:
        dashboard_filename = os.path.basename(generated_files['interactive_dashboard'])
        html_content += f"""
        <div class="visualization">
            <h2>Dashboard Interativo</h2>
            <p><a href="{dashboard_filename}" target="_blank">Clique aqui para abrir o dashboard interativo</a></p>
            <div class="description">Dashboard com gráficos interativos para exploração detalhada dos dados</div>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    # Salva relatório
    report_path = os.path.join(output_dir, 'visualization_report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"Relatório de visualizações salvo em: {report_path}")
    return report_path

if __name__ == "__main__":
    # Exemplo de uso
    visualizer = DataVisualizer()
    
    # Carrega dados de exemplo (substitua pelos dados reais)
    contexts_df = pd.DataFrame()  # Carregue seus dados aqui
    frequencies = {}  # Carregue suas frequências aqui
    patterns = {}  # Carregue seus padrões aqui
    
    # Gera todas as visualizações
    generated_files = visualizer.generate_all_visualizations(contexts_df, frequencies, patterns)
    
    # Cria relatório
    report_path = create_visualization_report(generated_files, visualizer.output_dir)
    
    print(f"Visualizações geradas: {list(generated_files.keys())}")
    print(f"Relatório disponível em: {report_path}")
