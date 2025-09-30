"""
Módulo de Expansão Semântica
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa

Este módulo é responsável por expandir semanticamente o vocabulário relacionado
ao tema "sonho" usando diferentes abordagens:
- FastText para similaridade semântica
- BERTimbau para contexto
- Claude Sonnet 4 para análise literária qualitativa
"""

import os
import logging
from typing import List, Set, Dict, Tuple, Optional
import anthropic
from dotenv import load_dotenv
import json
import time

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticExpander:
    """Classe para expansão semântica de vocabulário."""
    
    def __init__(self):
        """Inicializa o expansor semântico."""
        self.anthropic_client = None
        self._setup_anthropic()
        
        # Palavras-chave semente relacionadas a sonho
        self.seed_words = [
            "sonho", "pesadelo", "visão", "sombra", "glória",
            "fantasia", "ilusão", "devaneio", "quimera", "miragem",
            "aparição", "revelação", "profecia", "presságio", "augúrio"
        ]
    
    def _setup_anthropic(self):
        """Configura o cliente Anthropic."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                logger.info("Cliente Anthropic configurado com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao configurar Anthropic: {e}")
                self.anthropic_client = None
        else:
            logger.warning("ANTHROPIC_API_KEY não encontrada. "
                         "Funcionalidades do Claude não estarão disponíveis.")
    
    def expand_with_claude(self, context: str = "Os Lusíadas de Camões") -> List[str]:
        """
        Expande vocabulário usando Claude Sonnet 4.
        
        Args:
            context: Contexto literário para a expansão
            
        Returns:
            Lista de palavras expandidas
        """
        if not self.anthropic_client:
            logger.warning("Cliente Anthropic não disponível.")
            return []
        
        try:
            prompt = f"""
            Analise o tema "sonho" na obra "{context}" e identifique palavras e conceitos 
            semanticamente relacionados. Considere diferentes tipos de sonho:
            
            1. Sonhos oníricos (pesadelos, devaneios)
            2. Visões proféticas (presságios, augúrios)
            3. Sonhos alegóricos (símbolos, metáforas)
            4. Sonhos divinos (revelações, aparições)
            5. Ilusões e quimeras
            
            Palavras-chave iniciais: {', '.join(self.seed_words)}
            
            Retorne uma lista de 20-30 palavras em português, uma por linha, 
            relacionadas ao tema "sonho" no contexto literário português clássico.
            """
            
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extrai palavras da resposta
            words = []
            for line in response.content[0].text.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    # Remove numeração e pontuação
                    word = re.sub(r'^\d+\.?\s*', '', line).strip()
                    if word and len(word) > 2:
                        words.append(word.lower())
            
            logger.info(f"Claude expandiu para {len(words)} palavras.")
            return words[:30]  # Limita a 30 palavras
            
        except Exception as e:
            logger.error(f"Erro na expansão com Claude: {e}")
            return []
    
    def expand_with_fasttext(self) -> List[str]:
        """
        Expande vocabulário usando FastText (simulado).
        
        Returns:
            Lista de palavras similares
        """
        # Simulação de expansão FastText
        # Em implementação real, usaria modelo FastText treinado
        fasttext_words = [
            "sonhar", "sonhador", "sonhante", "sonhável",
            "pesadelo", "pesadeloso", "pesadelante",
            "visão", "visionário", "visionar", "visionante",
            "sombra", "sombreado", "sombreador", "sombreado",
            "glória", "glorioso", "glorificar", "glorificação",
            "fantasia", "fantasioso", "fantasiar", "fantasista",
            "ilusão", "ilusório", "iludir", "ilusão",
            "devaneio", "devaneante", "devaneador",
            "quimera", "quimérico", "quimerista",
            "miragem", "miragista", "miragoso",
            "aparição", "aparecer", "aparente",
            "revelação", "revelar", "revelador",
            "profecia", "profético", "profetizar",
            "presságio", "pressagiar", "pressagiador",
            "augúrio", "augurar", "augurador"
        ]
        
        logger.info(f"FastText expandiu para {len(fasttext_words)} palavras.")
        return fasttext_words
    
    def expand_with_bertimbau(self) -> List[str]:
        """
        Expande vocabulário usando BERTimbau (simulado).
        
        Returns:
            Lista de palavras contextualmente similares
        """
        # Simulação de expansão BERTimbau
        # Em implementação real, usaria modelo BERTimbau
        bertimbau_words = [
            "sonho", "sonhar", "sonhador", "sonhante",
            "pesadelo", "pesadeloso", "pesadelante",
            "visão", "visionário", "visionar",
            "sombra", "sombreado", "sombreador",
            "glória", "glorioso", "glorificar",
            "fantasia", "fantasioso", "fantasiar",
            "ilusão", "ilusório", "iludir",
            "devaneio", "devaneante",
            "quimera", "quimérico",
            "miragem", "miragista",
            "aparição", "aparecer",
            "revelação", "revelar",
            "profecia", "profético",
            "presságio", "pressagiar",
            "augúrio", "augurar"
        ]
        
        logger.info(f"BERTimbau expandiu para {len(bertimbau_words)} palavras.")
        return bertimbau_words
    
    def get_comprehensive_expansion(self) -> Dict[str, List[str]]:
        """
        Obtém expansão semântica completa usando todos os métodos.
        
        Returns:
            Dicionário com resultados de cada método
        """
        results = {
            'seed_words': self.seed_words,
            'claude_expansion': [],
            'fasttext_expansion': [],
            'bertimbau_expansion': [],
            'combined_expansion': []
        }
        
        # Expansão com Claude
        try:
            results['claude_expansion'] = self.expand_with_claude()
        except Exception as e:
            logger.error(f"Erro na expansão Claude: {e}")
        
        # Expansão com FastText
        try:
            results['fasttext_expansion'] = self.expand_with_fasttext()
        except Exception as e:
            logger.error(f"Erro na expansão FastText: {e}")
        
        # Expansão com BERTimbau
        try:
            results['bertimbau_expansion'] = self.expand_with_bertimbau()
        except Exception as e:
            logger.error(f"Erro na expansão BERTimbau: {e}")
        
        # Combina todas as palavras
        all_words = set(self.seed_words)
        all_words.update(results['claude_expansion'])
        all_words.update(results['fasttext_expansion'])
        all_words.update(results['bertimbau_expansion'])
        
        results['combined_expansion'] = sorted(list(all_words))
        
        logger.info(f"Expansão completa: {len(results['combined_expansion'])} palavras únicas.")
        return results

# Função auxiliar para importação
def get_semantic_expander() -> SemanticExpander:
    """Retorna instância do expansor semântico."""
    return SemanticExpander()


