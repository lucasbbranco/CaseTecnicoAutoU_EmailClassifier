"""
FastAPI Main Application
========================
Aplicação principal que gerencia rotas, CORS e inicialização do servidor.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import logging
import os

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

# Servir arquivos estáticos do frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

# Montar diretórios estáticos apenas se existirem
if os.path.exists(frontend_path):
    assets_path = os.path.join(frontend_path, "assets")
    css_path = os.path.join(frontend_path, "css")
    js_path = os.path.join(frontend_path, "js")
    
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
    if os.path.exists(css_path):
        app.mount("/css", StaticFiles(directory=css_path), name="css")
    if os.path.exists(js_path):
        app.mount("/js", StaticFiles(directory=js_path), name="js")

# Rota raiz - servir o HTML do frontend
@app.get("/")
async def root():
    """
    Endpoint raiz - Retorna o arquivo HTML do frontend
    """
    html_file = os.path.join(frontend_path, "index.html") if os.path.exists(frontend_path) else None
    
    if html_file and os.path.exists(html_file):
        return FileResponse(html_file, media_type="text/html")
    else:
        # Fallback se o arquivo não existir
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Email Classifier</title>
            </head>
            <body>
                <h1>Email Classifier API</h1>
                <p>Frontend não configurado. Acesse <a href="/api/docs">/api/docs</a> para a documentação da API.</p>
            </body>
        </html>
        """)

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