"""
Módulo de Validação com Gemini
Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa

Este módulo implementa validação cruzada usando Google Gemini como modelo secundário,
conforme solicitado pela cliente para maior confiabilidade na análise.
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiValidator:
    """Validador usando Google Gemini para validação cruzada."""
    
    def __init__(self):
        """Inicializa o validador Gemini."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-1.5-flash"
        self.available = bool(self.api_key)
        
        if not self.available:
            logger.warning("GEMINI_API_KEY não encontrada. Validação Gemini não estará disponível.")
        else:
            logger.info("Validador Gemini configurado com sucesso.")
    
    def validate_classification(self, context: str, classification: str, 
                              confidence: float) -> Dict[str, Any]:
        """
        Valida classificação usando Gemini.
        
        Args:
            context: Contexto do sonho
            classification: Classificação atribuída
            confidence: Confiança da classificação
            
        Returns:
            Dicionário com validação
        """
        if not self.available:
            return {
                'validated': False,
                'reason': 'Gemini não disponível',
                'original_classification': classification,
                'original_confidence': confidence
            }
        
        try:
            prompt = self._create_validation_prompt(context, classification)
            response = self._call_gemini_api(prompt)
            
            if response:
                validation_result = self._parse_validation_response(response)
                return {
                    'validated': True,
                    'original_classification': classification,
                    'original_confidence': confidence,
                    'gemini_classification': validation_result.get('classification', classification),
                    'gemini_confidence': validation_result.get('confidence', confidence),
                    'gemini_reasoning': validation_result.get('reasoning', ''),
                    'agreement': validation_result.get('classification', classification) == classification,
                    'confidence_difference': abs(validation_result.get('confidence', confidence) - confidence)
                }
            else:
                return {
                    'validated': False,
                    'reason': 'Erro na resposta do Gemini',
                    'original_classification': classification,
                    'original_confidence': confidence
                }
                
        except Exception as e:
            logger.error(f"Erro na validação Gemini: {e}")
            return {
                'validated': False,
                'reason': f'Erro: {str(e)}',
                'original_classification': classification,
                'original_confidence': confidence
            }
    
    def _create_validation_prompt(self, context: str, classification: str) -> str:
        """
        Cria prompt para validação no Gemini.
        
        Args:
            context: Contexto do sonho
            classification: Classificação a validar
            
        Returns:
            Prompt formatado
        """
        return f"""
Analise o seguinte contexto de "Os Lusíadas" de Camões e valide a classificação fornecida:

CONTEXTO: "{context}"

CLASSIFICAÇÃO ATUAL: {classification}

As categorias possíveis são:
1. "onírico" - sonhos, pesadelos, devaneios, estados de sono
2. "profético" - visões, presságios, augúrios, revelações sobre o futuro
3. "alegórico" - símbolos, metáforas, alegorias relacionadas a sonhos
4. "divino" - revelações, aparições divinas, manifestações sobrenaturais
5. "ilusório" - ilusões, quimeras, miragens, falsas aparências

Responda em formato JSON:
{{
    "classification": "categoria_correta",
    "confidence": 0.95,
    "reasoning": "explicação_do_raciocínio",
    "agreement": true/false
}}

Considere o contexto literário português clássico e a obra de Camões.
"""
    
    def _call_gemini_api(self, prompt: str) -> Optional[Dict]:
        """
        Chama a API do Gemini.
        
        Args:
            prompt: Prompt para enviar
            
        Returns:
            Resposta da API ou None
        """
        try:
            url = f"{self.base_url}/models/{self.model}:generateContent"
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 1000,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and result['candidates']:
                content = result['candidates'][0]['content']['parts'][0]['text']
                return {'content': content}
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na chamada da API Gemini: {e}")
            return None
    
    def _parse_validation_response(self, response: Dict) -> Dict[str, Any]:
        """
        Analisa resposta do Gemini.
        
        Args:
            response: Resposta da API
            
        Returns:
            Dicionário com dados validados
        """
        try:
            content = response.get('content', '')
            
            # Tenta extrair JSON da resposta
            json_match = self._extract_json_from_text(content)
            if json_match:
                return json_match
            
            # Fallback: análise simples do texto
            return self._parse_text_response(content)
            
        except Exception as e:
            logger.error(f"Erro ao analisar resposta Gemini: {e}")
            return {
                'classification': 'onírico',
                'confidence': 0.5,
                'reasoning': 'Erro na análise da resposta',
                'agreement': False
            }
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """
        Extrai JSON do texto de resposta.
        
        Args:
            text: Texto da resposta
            
        Returns:
            JSON extraído ou None
        """
        try:
            # Procura por JSON na resposta
            import re
            json_pattern = r'\{[^{}]*"classification"[^{}]*\}'
            match = re.search(json_pattern, text, re.DOTALL)
            
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao extrair JSON: {e}")
            return None
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """
        Analisa resposta em texto puro.
        
        Args:
            text: Texto da resposta
            
        Returns:
            Dicionário com dados analisados
        """
        text_lower = text.lower()
        
        # Identifica classificação
        classifications = ['onírico', 'profético', 'alegórico', 'divino', 'ilusório']
        found_classification = 'onírico'
        
        for classification in classifications:
            if classification in text_lower:
                found_classification = classification
                break
        
        # Estima confiança baseada em palavras-chave
        confidence_indicators = {
            'muito': 0.9,
            'bastante': 0.8,
            'razoavelmente': 0.7,
            'possivelmente': 0.6,
            'talvez': 0.5
        }
        
        confidence = 0.7  # Default
        for indicator, conf_value in confidence_indicators.items():
            if indicator in text_lower:
                confidence = conf_value
                break
        
        return {
            'classification': found_classification,
            'confidence': confidence,
            'reasoning': text[:200] + '...' if len(text) > 200 else text,
            'agreement': True
        }
    
    def validate_batch(self, contexts: List[Dict]) -> List[Dict]:
        """
        Valida lote de contextos.
        
        Args:
            contexts: Lista de contextos para validar
            
        Returns:
            Lista de contextos validados
        """
        validated_contexts = []
        
        for context in contexts:
            validation = self.validate_classification(
                context.get('context', ''),
                context.get('classification', 'onírico'),
                context.get('confidence', 0.5)
            )
            
            # Adiciona validação ao contexto original
            context['gemini_validation'] = validation
            validated_contexts.append(context)
        
        return validated_contexts
    
    def get_validation_summary(self, validated_contexts: List[Dict]) -> Dict[str, Any]:
        """
        Gera resumo da validação.
        
        Args:
            validated_contexts: Contextos validados
            
        Returns:
            Resumo da validação
        """
        if not validated_contexts:
            return {'total': 0, 'validated': 0, 'agreement_rate': 0.0}
        
        total = len(validated_contexts)
        validated = sum(1 for ctx in validated_contexts 
                       if ctx.get('gemini_validation', {}).get('validated', False))
        agreements = sum(1 for ctx in validated_contexts 
                        if ctx.get('gemini_validation', {}).get('agreement', False))
        
        agreement_rate = agreements / validated if validated > 0 else 0.0
        
        return {
            'total_contexts': total,
            'validated_contexts': validated,
            'agreement_rate': round(agreement_rate, 3),
            'validation_available': self.available
        }

def create_gemini_validator() -> GeminiValidator:
    """Cria instância do validador Gemini."""
    return GeminiValidator()

