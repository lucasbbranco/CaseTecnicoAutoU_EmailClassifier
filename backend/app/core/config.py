"""
Configuration Settings
======================
Gerencia todas as configurações e variáveis de ambiente da aplicação.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """
    Classe de configurações da aplicação.
    Carrega variáveis de ambiente do arquivo .env
    """
    
    # Informações da aplicação
    APP_NAME: str = "Email Classifier API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API de IA (Groq)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"  # Modelo padrão
    GROQ_API_BASE: str = "https://api.groq.com/openai/v1"
    
    # Configurações de processamento
    MAX_FILE_SIZE_MB: int = 5  # Tamanho máximo de arquivo em MB
    MAX_TEXT_LENGTH: int = 10000  # Comprimento máximo de texto
    
    # Configurações de IA
    AI_TEMPERATURE: float = 0.3  # Temperatura para respostas mais consistentes
    AI_MAX_TOKENS: int = 500  # Máximo de tokens na resposta
    AI_TIMEOUT: int = 30  # Timeout em segundos
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]  # Em produção, especificar domínios
    
    class Config:
        """
        Configuração do Pydantic Settings
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna instância singleton das configurações.
    Usa cache para evitar recarregar em cada chamada.
    
    Returns:
        Settings: Objeto de configurações
    """
    return Settings()


# Instância global das configurações
settings = get_settings()

# Validação: Verificar se a API key está configurada
if not settings.GROQ_API_KEY:
    print("[AVISO] GROQ_API_KEY não configurada!")
    print("[INFO] Configure a variável de ambiente ou arquivo .env")