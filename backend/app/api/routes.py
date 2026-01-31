"""
API Routes
==========
Define todos os endpoints da API de classificação de emails.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
import logging
import time

# Importar serviços e models
from backend.app.services.classifier import EmailClassifier
from backend.app.services.file_processor import FileProcessor
from backend.app.models.schemas import EmailTextRequest, ClassificationResponse

# Configurar logger
logger = logging.getLogger(__name__)

# Criar router
router = APIRouter()

# Instanciar serviços
classifier = EmailClassifier()
file_processor = FileProcessor()

# ==================== ENDPOINTS ====================

@router.get("/health")
async def health_check():
    """
    Health check - verifica se a API está funcionando
    
    Returns:
        dict: Status da API
    """
    return {
        "status": "healthy",
        "service": "Email Classifier API",
        "timestamp": time.time()
    }


@router.post("/classify-text", response_model=ClassificationResponse)
async def classify_text(request: EmailTextRequest):
    """
    Classifica um email enviado como texto direto
    
    Args:
        request: Objeto com o texto do email
        
    Returns:
        ClassificationResponse: Resultado da classificação
    """
    try:
        start_time = time.time()
        logger.info("Recebida requisição de classificação de texto")
        
        # Validar texto
        if not request.email_text or len(request.email_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="O texto do email não pode estar vazio"
            )
        
        # Validar tamanho mínimo
        if len(request.email_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="O texto deve ter pelo menos 10 caracteres"
            )
        
        # Classificar email
        result = await classifier.classify_email(request.email_text)
        
        # Calcular tempo de processamento
        processing_time = int((time.time() - start_time) * 1000)
        result["processing_time_ms"] = processing_time
        
        logger.info(f"Classificação concluída em {processing_time}ms")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao classificar texto: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar classificação: {str(e)}"
        )


@router.post("/classify-file", response_model=ClassificationResponse)
async def classify_file(file: UploadFile = File(...)):
    """
    Classifica um email enviado como arquivo (.txt ou .pdf)
    
    Args:
        file: Arquivo de email (.txt ou .pdf)
        
    Returns:
        ClassificationResponse: Resultado da classificação
    """
    try:
        start_time = time.time()
        logger.info(f"Recebido arquivo: {file.filename}")
        
        # Validar tipo de arquivo
        if not file.filename.endswith(('.txt', '.pdf')):
            raise HTTPException(
                status_code=400,
                detail="Apenas arquivos .txt e .pdf são permitidos"
            )
        
        # Processar arquivo e extrair texto
        email_text = await file_processor.process_file(file)
        
        if not email_text or len(email_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível extrair texto do arquivo"
            )
        
        # Classificar email
        result = await classifier.classify_email(email_text)
        
        # Calcular tempo de processamento
        processing_time = int((time.time() - start_time) * 1000)
        result["processing_time_ms"] = processing_time
        result["filename"] = file.filename
        
        logger.info(f"Arquivo processado em {processing_time}ms")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )


@router.get("/test")
async def test_endpoint():
    """
    Endpoint de teste para verificar conectividade
    
    Returns:
        dict: Mensagem de teste
    """
    return {
        "message": "API está funcionando corretamente!",
        "endpoints": [
            "/api/health",
            "/api/classify-text",
            "/api/classify-file",
            "/api/test"
        ]
    }