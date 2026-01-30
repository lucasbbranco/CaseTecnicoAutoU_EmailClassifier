"""
FastAPI Main Application
========================
Aplicação principal que gerencia rotas, CORS e inicialização do servidor.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Importar rotas
from backend.app.api.routes import router

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="Email Classifier API",
    description="API para classificação automática de emails usando IA",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger UI
    redoc_url="/api/redoc"  # ReDoc
)

# Configurar CORS (permitir requisições do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas da API
app.include_router(router, prefix="/api")

# Rota raiz (health check)
@app.get("/")
async def root():
    """
    Endpoint raiz - Health check da API
    """
    return {
        "status": "online",
        "message": "Email Classifier API está funcionando!",
        "docs": "/api/docs"
    }

# Handler global de erros
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Captura erros não tratados e retorna resposta padronizada
    """
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Erro interno do servidor",
            "detail": str(exc)
        }
    )

# Evento de inicialização
@app.on_event("startup")
async def startup_event():
    """
    Executado quando a aplicação inicia
    """
    logger.info("Iniciando Email Classifier API...")
    logger.info("Sistema de classificação pronto!")

# Evento de encerramento
@app.on_event("shutdown")
async def shutdown_event():
    """
    Executado quando a aplicação é encerrada
    """
    logger.info("Encerrando Email Classifier API...")