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
from dotenv import load_dotenv
import json
import time
import re

# Importação opcional do OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticExpander:
    """Classe para expansão semântica de vocabulário."""
    
    def __init__(self):
        """Inicializa o expansor semântico."""
        self.openai_client = None
        self._setup_openai()
        
        # Palavras-chave semente relacionadas a sonho
        self.seed_words = [
            "sonho", "pesadelo", "visão", "sombra", "glória",
            "fantasia", "ilusão", "devaneio", "quimera", "miragem",
            "aparição", "revelação", "profecia", "presságio", "augúrio"
        ]
    
    def _setup_openai(self):
        """Configura o cliente OpenAI."""
        if not OPENAI_AVAILABLE:
            logger.warning("Biblioteca OpenAI não instalada. "
                         "Funcionalidades da OpenAI não estarão disponíveis.")
            self.openai_client = None
            return
            
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            try:
                openai.api_key = api_key
                self.openai_client = openai
                logger.info("Cliente OpenAI configurado com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao configurar OpenAI: {e}")
                self.openai_client = None
        else:
            logger.warning("OPENAI_API_KEY não encontrada. "
                         "Funcionalidades da OpenAI não estarão disponíveis.")
            self.openai_client = None
    
    def expand_with_openai(self, context: str = "Os Lusíadas de Camões") -> Dict[str, List[str]]:
        """
        Expande vocabulário usando OpenAI GPT-4 com prompt especializado.
        
        Args:
            context: Contexto literário para a expansão
            
        Returns:
            Dicionário com termos categorizados
        """
        if not self.openai_client:
            logger.warning("Cliente OpenAI não disponível.")
            return {}
        
        try:
            prompt = f"""Você é um especialista em filologia e literatura portuguesa, com foco no período clássico e na obra "Os Lusíadas" de Camões. Sua tarefa é expandir um vocabulário sobre o tema "sonho" para análise literária.

**Contexto:** A análise incide sobre "{context}". O conceito de "sonho" deve ser interpretado de forma ampla, abrangendo não apenas o ato de sonhar, mas também visões, profecias, ilusões e estados alterados de consciência que Camões utiliza como recurso poético e narrativo.

**Instruções:**
1.  **Expanda o Vocabulário:** Com base nas palavras-chave seminais abaixo, gere uma lista de 30 a 40 termos e expressões semanticamente relacionados que sejam pertinentes ao português arcaico e ao estilo de Camões.
2.  **Categorize os Termos:** Organize os termos gerados nas seguintes categorias, com base em seu significado primário no contexto da obra:
    *   `onírico`: Termos ligados ao sono, sonhos e pesadelos.
    *   `profético`: Termos ligados a visões, profecias, presságios e revelações.
    *   `alegórico`: Termos ligados a símbolos, metáforas, fantasias e ilusões.
    *   `divino`: Termos que descrevem manifestações ou intervenções de divindades.
    *   `figurativo`: Termos onde "sonho" é usado como ambição ou desejo.
3.  **Inclua Variações:** Adicione variações morfológicas (e.g., `sonho`, `sonhar`, `sonhava`) e sinônimos arcaicos.

**Palavras-chave Seminais:**
`{', '.join(self.seed_words)}`

**Formato da Resposta:**
Responda **exclusivamente** com um objeto JSON. Não inclua nenhuma outra explicação ou texto. O JSON deve ter a seguinte estrutura:

```json
{{
  "onírico": ["sonho", "sonhar", "pesadelo", "dormir", "adormecer", "despertar"],
  "profético": ["visão", "profecia", "revelação", "oráculo", "presságio", "augúrio"],
  "alegórico": ["sombra", "fantasia", "ilusão", "metáfora", "símbolo", "alegoria"],
  "divino": ["glória", "divino", "celestial", "aparição", "milagre"],
  "figurativo": ["aspiração", "ambição", "desejo", "cobiça"]
}}
```"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=1500,
                temperature=0.1,  # Baixa temperatura para consistência
                response_format={"type": "json_object"}
            )
            
            # Parse da resposta JSON
            response_text = response.choices[0].message.content
            result = json.loads(response_text)
            
            # Validação das categorias
            expected_categories = ['onírico', 'profético', 'alegórico', 'divino', 'figurativo']
            validated_result = {}
            
            for category in expected_categories:
                if category in result and isinstance(result[category], list):
                    # Filtra termos válidos (não vazios, tamanho > 2)
                    valid_terms = [term.strip().lower() for term in result[category] 
                                  if isinstance(term, str) and len(term.strip()) > 2]
                    validated_result[category] = valid_terms[:10]  # Limita a 10 por categoria
                else:
                    validated_result[category] = []
            
            total_terms = sum(len(terms) for terms in validated_result.values())
            logger.info(f"OpenAI expandiu para {total_terms} termos em {len(validated_result)} categorias.")
            return validated_result
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON da resposta OpenAI: {e}")
            return {}
        except Exception as e:
            logger.error(f"Erro na expansão com OpenAI: {e}")
            return {}
    
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
    
    def get_comprehensive_expansion(self) -> Dict[str, any]:
        """
        Obtém expansão semântica completa usando todos os métodos.
        
        Returns:
            Dicionário com resultados de cada método
        """
        results = {
            'seed_words': self.seed_words,
            'openai_expansion_categorized': {},
            'fasttext_expansion': [],
            'bertimbau_expansion': [],
            'combined_expansion': []
        }
        
        # Expansão com OpenAI (categorizada)
        try:
            openai_result = self.expand_with_openai()
            results['openai_expansion_categorized'] = openai_result
            # Para compatibilidade, também cria lista plana
            openai_flat = []
            for category_terms in openai_result.values():
                openai_flat.extend(category_terms)
            results['openai_expansion'] = openai_flat
        except Exception as e:
            logger.error(f"Erro na expansão OpenAI: {e}")
            results['openai_expansion'] = []
        
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
        all_words.update(results.get('openai_expansion', []))
        all_words.update(results['fasttext_expansion'])
        all_words.update(results['bertimbau_expansion'])
        
        results['combined_expansion'] = sorted(list(all_words))
        
        # Adiciona métricas
        results['statistics'] = {
            'total_unique_terms': len(results['combined_expansion']),
            'openai_terms': len(results.get('openai_expansion', [])),
            'fasttext_terms': len(results['fasttext_expansion']),
            'bertimbau_terms': len(results['bertimbau_expansion']),
            'seed_terms': len(self.seed_words)
        }
        
        logger.info(f"Expansão completa: {len(results['combined_expansion'])} palavras únicas.")
        return results

# Função auxiliar para importação
def get_semantic_expander() -> SemanticExpander:
    """Retorna instância do expansor semântico."""
    return SemanticExpander()


