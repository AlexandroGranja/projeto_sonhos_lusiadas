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
            self.anthropic_client = anthropic.Anthropic(api_key=api_key)
            logger.info("Cliente Anthropic configurado com sucesso.")
        else:
            logger.warning("ANTHROPIC_API_KEY não encontrada. "
                         "Funcionalidades do Claude não estarão disponíveis.")
    
    def expand_with_claude(self, context: str = "Os Lusíadas de Camões") -> List[str]:
        """
        Expande vocabulário usando Claude Sonnet 4.
        
        Args:
            context: Contexto para a expansão
            
        Returns:
            Lista de palavras expandidas
        """
        if not self.anthropic_client:
            logger.error("Cliente Anthropic não configurado.")
            return []
        
        prompt = f"""
        Você é um especialista em literatura portuguesa e análise literária de Os Lusíadas de Luís de Camões.
        
        Preciso de uma lista abrangente de palavras e termos que Camões usa para se referir a:
        1. Sonhos e visões
        2. Profecias e presságios
        3. Ilusões e fantasias
        4. Aparições divinas ou sobrenaturais
        5. Estados oníricos ou de consciência alterada
        
        Contexto: {context}
        
        Por favor, forneça uma lista de 30-50 palavras ou expressões que aparecem em Os Lusíadas
        relacionadas a esses temas. Inclua variações arcaicas e formas poéticas que Camões utiliza.
        
        Formato: retorne apenas uma lista de palavras separadas por vírgula, sem explicações adicionais.
        """
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extrai palavras da resposta
            content = response.content[0].text
            words = [word.strip().lower() for word in content.split(',')]
            words = [word for word in words if word and len(word) > 2]
            
            logger.info(f"Claude retornou {len(words)} palavras expandidas.")
            return words
            
        except Exception as e:
            logger.error(f"Erro ao consultar Claude: {e}")
            return []
    
    def analyze_dream_context_with_claude(self, text_excerpt: str) -> Dict[str, str]:
        """
        Analisa um trecho de texto para classificar o tipo de sonho/visão.
        
        Args:
            text_excerpt: Trecho de texto para análise
            
        Returns:
            Dicionário com classificação e análise
        """
        if not self.anthropic_client:
            return {"type": "unknown", "analysis": "Claude não disponível"}
        
        prompt = f"""
        Analise o seguinte trecho de Os Lusíadas e classifique o tipo de sonho/visão presente:
        
        Trecho: "{text_excerpt}"
        
        Classifique em uma das categorias:
        1. "onírico" - sonho literal, experiência durante o sono
        2. "profético" - visão profética, presságio do futuro
        3. "alegórico" - representação simbólica, metáfora
        4. "divino" - aparição divina, intervenção sobrenatural
        5. "ilusão" - engano, fantasia, miragem
        6. "outro" - não se enquadra nas categorias acima
        
        Responda em formato JSON:
        {{
            "type": "categoria_escolhida",
            "confidence": "alta/média/baixa",
            "analysis": "breve explicação da classificação (máximo 100 palavras)",
            "literary_function": "função narrativa no épico (máximo 50 palavras)"
        }}
        """
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            # Tenta extrair JSON da resposta
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                # Se não conseguir parsear JSON, retorna análise básica
                return {
                    "type": "outro",
                    "confidence": "baixa",
                    "analysis": content[:100],
                    "literary_function": "análise não estruturada"
                }
                
        except Exception as e:
            logger.error(f"Erro ao analisar contexto com Claude: {e}")
            return {
                "type": "erro",
                "confidence": "baixa",
                "analysis": f"Erro na análise: {str(e)}",
                "literary_function": "não disponível"
            }
    
    def expand_with_fasttext(self, model_path: Optional[str] = None, n: int = 20) -> Set[str]:
        """
        Expande vocabulário usando FastText.
        
        Args:
            model_path: Caminho para o modelo FastText
            n: Número de palavras similares para cada palavra semente
            
        Returns:
            Conjunto de palavras expandidas
        """
        try:
            from gensim.models import KeyedVectors
            
            # Tenta carregar modelo FastText
            if model_path and os.path.exists(model_path):
                model = KeyedVectors.load_word2vec_format(model_path)
            else:
                logger.warning("Modelo FastText não encontrado. Usando palavras semente apenas.")
                return set(self.seed_words)
            
            expanded = set(self.seed_words)
            
            for word in self.seed_words:
                try:
                    similar = model.most_similar(word, topn=n)
                    expanded.update([w for w, score in similar if score > 0.5])
                except KeyError:
                    logger.warning(f"Palavra '{word}' não encontrada no modelo FastText.")
                    continue
            
            logger.info(f"FastText expandiu para {len(expanded)} palavras.")
            return expanded
            
        except ImportError:
            logger.error("Gensim não instalado. Execute: pip install gensim")
            return set(self.seed_words)
        except Exception as e:
            logger.error(f"Erro ao usar FastText: {e}")
            return set(self.seed_words)
    
    def expand_with_bertimbau(self, n: int = 20) -> Set[str]:
        """
        Expande vocabulário usando BERTimbau.
        
        Args:
            n: Número de palavras similares para cada palavra semente
            
        Returns:
            Conjunto de palavras expandidas
        """
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Carrega modelo BERTimbau
            model = SentenceTransformer('neuralmind/bert-base-portuguese-cased')
            
            # Vocabulário português relacionado a sonhos
            candidate_words = [
                "sonho", "pesadelo", "visão", "fantasia", "ilusão", "devaneio",
                "quimera", "miragem", "aparição", "revelação", "profecia",
                "presságio", "augúrio", "vaticínio", "oráculo", "sibila",
                "visionário", "profeta", "adivinho", "sonhador", "fantasma",
                "espectro", "sombra", "vulto", "figura", "imagem", "reflexo",
                "espelho", "eco", "lembrança", "memória", "recordação"
            ]
            
            # Calcula embeddings
            seed_embeddings = model.encode(self.seed_words)
            candidate_embeddings = model.encode(candidate_words)
            
            # Calcula similaridades
            similarities = cosine_similarity(seed_embeddings, candidate_embeddings)
            
            # Seleciona palavras mais similares
            expanded = set(self.seed_words)
            for i, word in enumerate(candidate_words):
                max_similarity = np.max(similarities[:, i])
                if max_similarity > 0.6:  # Threshold de similaridade
                    expanded.add(word)
            
            logger.info(f"BERTimbau expandiu para {len(expanded)} palavras.")
            return expanded
            
        except ImportError:
            logger.error("sentence-transformers não instalado. "
                        "Execute: pip install sentence-transformers")
            return set(self.seed_words)
        except Exception as e:
            logger.error(f"Erro ao usar BERTimbau: {e}")
            return set(self.seed_words)
    
    def get_comprehensive_expansion(self) -> Dict[str, List[str]]:
        """
        Obtém expansão abrangente usando todos os métodos disponíveis.
        
        Returns:
            Dicionário com palavras expandidas por método
        """
        results = {
            "seed_words": self.seed_words,
            "claude_expansion": [],
            "fasttext_expansion": [],
            "bertimbau_expansion": []
        }
        
        # Expansão com Claude
        claude_words = self.expand_with_claude()
        results["claude_expansion"] = claude_words
        
        # Expansão com FastText
        fasttext_words = list(self.expand_with_fasttext())
        results["fasttext_expansion"] = fasttext_words
        
        # Expansão com BERTimbau
        bertimbau_words = list(self.expand_with_bertimbau())
        results["bertimbau_expansion"] = bertimbau_words
        
        # Combina todas as palavras
        all_words = set(self.seed_words)
        all_words.update(claude_words)
        all_words.update(fasttext_words)
        all_words.update(bertimbau_words)
        
        results["combined_expansion"] = sorted(list(all_words))
        
        logger.info(f"Expansão total: {len(results['combined_expansion'])} palavras únicas.")
        
        return results
    
    def save_expansion_results(self, results: Dict[str, List[str]], output_path: str):
        """
        Salva resultados da expansão em arquivo.
        
        Args:
            results: Resultados da expansão
            output_path: Caminho para salvar os resultados
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Salva em formato JSON
        json_path = output_path.replace('.csv', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Salva lista combinada em CSV
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("palavra,fonte\n")
            
            for word in results["seed_words"]:
                f.write(f"{word},seed\n")
            
            for word in results["claude_expansion"]:
                if word not in results["seed_words"]:
                    f.write(f"{word},claude\n")
            
            for word in results["fasttext_expansion"]:
                if word not in results["seed_words"] and word not in results["claude_expansion"]:
                    f.write(f"{word},fasttext\n")
            
            for word in results["bertimbau_expansion"]:
                if (word not in results["seed_words"] and 
                    word not in results["claude_expansion"] and 
                    word not in results["fasttext_expansion"]):
                    f.write(f"{word},bertimbau\n")
        
        logger.info(f"Resultados salvos em {output_path} e {json_path}")

if __name__ == "__main__":
    # Exemplo de uso
    expander = SemanticExpander()
    
    # Obtém expansão abrangente
    results = expander.get_comprehensive_expansion()
    
    # Salva resultados
    output_file = "../results/expanded_words.csv"
    expander.save_expansion_results(results, output_file)
    
    print(f"Expansão concluída. Total de palavras: {len(results['combined_expansion'])}")
    print(f"Resultados salvos em: {output_file}")
