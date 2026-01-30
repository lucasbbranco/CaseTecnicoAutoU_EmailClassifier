"""
Email Classifier Service - Simplified Version
===========================================
Serviço simplificado para classificação de emails usando Groq API.
Remove código não utilizado: métricas, cache, validações complexas.
"""

from groq import Groq
from typing import Dict, Any
import json
import logging
import time
from datetime import datetime

# Importar configurações e utilitários
from backend.app.core.config import settings
from backend.app.core.prompts import (
    get_classification_prompt,
    get_response_generation_prompt,
    CLASSIFICATION_SYSTEM_PROMPT,
    RESPONSE_SYSTEM_PROMPT
)
from backend.app.utils.text_cleaner import TextCleaner

# Configurar logger
logger = logging.getLogger(__name__)


class EmailClassifier:
    """
    Classificador simplificado de emails.
    
    Attributes:
        client: Cliente Groq API
        text_cleaner: Utilitário de limpeza de texto
        retry_attempts: Número de tentativas em caso de falha
    """
    
    def __init__(self, retry_attempts: int = 3):
        """
        Inicializa o classificador.
        
        Args:
            retry_attempts: Número de tentativas em caso de falha
        """
        # Verificar configuração da API key
        if not settings.GROQ_API_KEY:
            logger.warning(
                "GROQ_API_KEY não configurada. "
                "Usando modo de simulação para desenvolvimento."
            )
            self.client = None
        else:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("Cliente Groq inicializado com sucesso")
        
        # Inicializar componentes
        self.text_cleaner = TextCleaner()
        self.retry_attempts = retry_attempts
        
        logger.info(f"EmailClassifier inicializado (retries={retry_attempts})")
    
    
    async def classify_email(self, email_text: str) -> Dict[str, Any]:
        """
        Classifica um email e gera resposta automática.
        
        Args:
            email_text: Texto do email a ser classificado
            
        Returns:
            Dict contendo:
                - success: bool
                - classification: str (PRODUTIVO ou IMPRODUTIVO)
                - confidence: float (0.0 a 1.0)
                - justification: str
                - suggested_response: str
                - processing_time_ms: int
                - error: str (se houver erro)
        """
        start_time = time.time()
        
        try:
            # 1. Validação básica
            if not email_text or len(email_text.strip()) < 10:
                return {
                    "success": False,
                    "error": "O texto do email deve ter pelo menos 10 caracteres"
                }
            
            if len(email_text) > 10000:
                return {
                    "success": False,
                    "error": "O texto excede o limite de 10.000 caracteres"
                }
            
            # 2. Aplicar processamento NLP completo
            # Extrai conteúdo principal primeiro (remove assinatura)
            cleaned_text = self.text_cleaner.extract_main_content(email_text)
            # Aplica NLP: tokenização, remoção de stop words, stemming
            nlp_text = self.text_cleaner.apply_nlp_preprocessing(cleaned_text)
            
            logger.info(f"Texto processado com NLP: {len(nlp_text)} caracteres")
            
            # 3. Se não há cliente configurado, simular
            if not self.client:
                result = self._simulate_classification(nlp_text)
                processing_time = time.time() - start_time
                result["processing_time_ms"] = int(processing_time * 1000)
                return result
            
            # 4. Classificar com a API (usando texto processado com NLP)
            classification_result = await self._classify_with_retry(nlp_text)
            
            # 5. Gerar resposta automática (usando texto original, não NLP)
            suggested_response = await self._generate_response_with_retry(
                email_text,
                classification_result["categoria"]
            )
            
            # 6. Montar resultado final
            processing_time = time.time() - start_time
            
            result = {
                "success": True,
                "classification": classification_result["categoria"],
                "confidence": classification_result["confianca"],
                "justification": classification_result["justificativa"],
                "suggested_response": suggested_response,
                "processing_time_ms": int(processing_time * 1000),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(
                f"Classificação concluída: {result['classification']} "
                f"({result['confidence']:.2%}) em {result['processing_time_ms']}ms"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na classificação: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": f"Erro ao processar email: {str(e)}",
                "processing_time_ms": int((time.time() - start_time) * 1000)
            }
    
    
    async def _classify_with_retry(self, email_text: str) -> Dict[str, Any]:
        """
        Classifica email com retry logic.
        
        Args:
            email_text: Texto limpo do email
            
        Returns:
            Dict com categoria, confiança e justificativa
        """
        last_error = None
        
        for attempt in range(1, self.retry_attempts + 1):
            try:
                logger.info(f"Tentativa de classificação {attempt}/{self.retry_attempts}")
                
                # Montar prompt
                prompt = get_classification_prompt(email_text)
                
                # Chamar API Groq
                response = self.client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": CLASSIFICATION_SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=settings.AI_TEMPERATURE,
                    max_tokens=settings.AI_MAX_TOKENS,
                    timeout=settings.AI_TIMEOUT
                )
                
                # Extrair e parsear resposta
                result_text = response.choices[0].message.content.strip()
                logger.debug(f"Resposta da IA: {result_text[:200]}...")
                
                # Limpar e parsear JSON
                result_text = self._clean_json_response(result_text)
                result = json.loads(result_text)
                
                # Validar resultado
                if not self._validate_classification_result(result):
                    raise ValueError("Resposta da IA em formato inválido")
                
                # Normalizar categoria
                result["categoria"] = result["categoria"].upper()
                
                logger.info(f"Classificação bem-sucedida na tentativa {attempt}")
                return result
                
            except json.JSONDecodeError as e:
                last_error = f"Erro ao parsear JSON: {str(e)}"
                logger.warning(f"{last_error}")
                
                if attempt < self.retry_attempts:
                    time.sleep(1 * attempt)
                    continue
                    
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Tentativa {attempt} falhou: {last_error}")
                
                if attempt < self.retry_attempts:
                    time.sleep(1 * attempt)
                    continue
        
        raise Exception(f"Falha após {self.retry_attempts} tentativas: {last_error}")
    
    
    async def _generate_response_with_retry(
        self,
        email_text: str,
        categoria: str
    ) -> str:
        """
        Gera resposta automática com retry logic.
        
        Args:
            email_text: Texto original do email
            categoria: Categoria classificada
            
        Returns:
            str: Resposta sugerida
        """
        for attempt in range(1, self.retry_attempts + 1):
            try:
                # Montar prompt
                prompt = get_response_generation_prompt(email_text, categoria)
                
                # Chamar API Groq
                response = self.client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": RESPONSE_SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.5,
                    max_tokens=300,
                    timeout=settings.AI_TIMEOUT
                )
                
                # Extrair resposta
                suggested_response = response.choices[0].message.content.strip()
                
                # Validar que não está vazia
                if len(suggested_response) < 20:
                    raise ValueError("Resposta muito curta")
                
                logger.info("Resposta gerada com sucesso")
                return suggested_response
                
            except Exception as e:
                logger.warning(
                    f"Tentativa {attempt} de gerar resposta falhou: {str(e)}"
                )
                
                if attempt < self.retry_attempts:
                    time.sleep(0.5 * attempt)
                    continue
        
        # Fallback: retornar resposta padrão
        logger.warning("Usando resposta padrão como fallback")
        return self._get_default_response(categoria)
    
    
    def _clean_json_response(self, text: str) -> str:
        """Limpa resposta da IA para extrair JSON válido."""
        text = text.replace("```json", "").replace("```", "")
        start_idx = text.find("{")
        end_idx = text.rfind("}") + 1
        
        if start_idx != -1 and end_idx != 0:
            text = text[start_idx:end_idx]
        
        return text.strip()
    
    
    def _validate_classification_result(self, result: Dict) -> bool:
        """Valida resultado da classificação."""
        required_keys = ["categoria", "confianca", "justificativa"]
        
        if not all(key in result for key in required_keys):
            return False
        
        if result["categoria"] not in ["PRODUTIVO", "IMPRODUTIVO", "produtivo", "improdutivo"]:
            return False
        
        if not isinstance(result["confianca"], (int, float)):
            return False
        
        if not (0 <= result["confianca"] <= 1):
            return False
        
        return True
    
    
    def _get_default_response(self, categoria: str) -> str:
        """Retorna resposta padrão baseada na categoria."""
        if categoria.upper() == "PRODUTIVO":
            return (
                "Prezado(a),\n\n"
                "Recebemos sua mensagem e estamos analisando sua solicitação. "
                "Nossa equipe retornará em breve com uma resposta detalhada.\n\n"
                "Caso tenha dúvidas adicionais, não hesite em entrar em contato.\n\n"
                "Atenciosamente,\n"
                "Equipe de Atendimento"
            )
        else:
            return (
                "Olá,\n\n"
                "Agradecemos pela sua mensagem!\n\n"
                "Atenciosamente,\n"
                "Equipe de Atendimento"
            )
    
    
    def _simulate_classification(self, email_text: str) -> Dict[str, Any]:
        """
        Simula classificação quando API key não está configurada.
        APENAS PARA DESENVOLVIMENTO/TESTES.
        """
        logger.warning("MODO SIMULAÇÃO ATIVO (configure GROQ_API_KEY)")
        
        email_lower = email_text.lower()
        
        keywords_produtivo = [
            "solicitação", "solicitacao", "dúvida", "duvida",
            "problema", "suporte", "ajuda", "status",
            "atualização", "atualizacao", "erro", "falha",
            "requisição", "requisicao", "reclamação", "reclamacao"
        ]
        
        keywords_improdutivo = [
            "parabéns", "parabens", "feliz", "obrigado",
            "agradecimento", "natal", "aniversário", "aniversario",
            "motivacional", "inspiração", "inspiracao"
        ]
        
        produtivo_score = sum(1 for kw in keywords_produtivo if kw in email_lower)
        improdutivo_score = sum(1 for kw in keywords_improdutivo if kw in email_lower)
        
        if produtivo_score > improdutivo_score:
            categoria = "PRODUTIVO"
            confianca = min(0.6 + (produtivo_score * 0.1), 0.95)
            justificativa = "Email contém indicadores de solicitação ou problema"
        elif improdutivo_score > produtivo_score:
            categoria = "IMPRODUTIVO"
            confianca = min(0.6 + (improdutivo_score * 0.1), 0.95)
            justificativa = "Email contém mensagem não-urgente ou social"
        else:
            categoria = "PRODUTIVO"
            confianca = 0.5
            justificativa = "Classificação padrão por incerteza (modo simulação)"
        
        return {
            "success": True,
            "classification": categoria,
            "confidence": confianca,
            "justification": f"{justificativa} [SIMULAÇÃO]",
            "suggested_response": self._get_default_response(categoria),
            "timestamp": datetime.utcnow().isoformat()
        }
