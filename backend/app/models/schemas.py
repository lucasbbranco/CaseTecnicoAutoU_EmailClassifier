"""
Pydantic Schemas
================
Define modelos de dados para validação de requests e responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

# ==================== REQUEST MODELS ====================

class EmailTextRequest(BaseModel):
    """
    Schema para requisição de classificação de texto direto.
    """
    email_text: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Texto do email a ser classificado",
        example="Prezados, gostaria de solicitar o status da minha requisição #12345."
    )
    
    @validator('email_text')
    def validate_text(cls, v):
        """
        Valida o texto do email.
        """
        if not v or not v.strip():
            raise ValueError("O texto do email não pode estar vazio")
        return v.strip()


# ==================== RESPONSE MODELS ====================

class ClassificationResponse(BaseModel):
    """
    Schema para resposta de classificação.
    """
    success: bool = Field(
        ...,
        description="Indica se a classificação foi bem-sucedida"
    )
    
    classification: Optional[str] = Field(
        None,
        description="Categoria do email: PRODUTIVO ou IMPRODUTIVO",
        example="PRODUTIVO"
    )
    
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confiança da classificação (0.0 a 1.0)",
        example=0.95
    )
    
    justification: Optional[str] = Field(
        None,
        description="Justificativa da classificação",
        example="Email solicita atualização sobre caso em aberto"
    )
    
    suggested_response: Optional[str] = Field(
        None,
        description="Resposta automática sugerida",
        example="Prezado(a), recebemos sua solicitação e retornaremos em breve."
    )
    
    processing_time_ms: Optional[int] = Field(
        None,
        description="Tempo de processamento em milissegundos",
        example=1234
    )
    
    filename: Optional[str] = Field(
        None,
        description="Nome do arquivo processado (se aplicável)",
        example="email.txt"
    )
    
    error: Optional[str] = Field(
        None,
        description="Mensagem de erro (se houver)",
        example="Erro ao processar arquivo"
    )
    
    class Config:
        """
        Configuração do schema
        """
        schema_extra = {
            "example": {
                "success": True,
                "classification": "PRODUTIVO",
                "confidence": 0.95,
                "justification": "Email contém solicitação de suporte técnico",
                "suggested_response": "Prezado(a),\n\nRecebemos sua mensagem e estamos analisando sua solicitação. Retornaremos em breve.\n\nAtenciosamente,\nEquipe de Atendimento",
                "processing_time_ms": 1234,
                "filename": "email.txt"
            }
        }


class HealthCheckResponse(BaseModel):
    """
    Schema para resposta de health check.
    """
    status: str = Field(
        ...,
        description="Status da API",
        example="healthy"
    )
    
    service: str = Field(
        ...,
        description="Nome do serviço",
        example="Email Classifier API"
    )
    
    timestamp: float = Field(
        ...,
        description="Timestamp da verificação",
        example=1234567890.123
    )


class ErrorResponse(BaseModel):
    """
    Schema para resposta de erro.
    """
    success: bool = Field(
        False,
        description="Sempre False em erros"
    )
    
    error: str = Field(
        ...,
        description="Mensagem de erro",
        example="Arquivo muito grande"
    )
    
    detail: Optional[str] = Field(
        None,
        description="Detalhes adicionais do erro",
        example="O tamanho máximo permitido é 5MB"
    )