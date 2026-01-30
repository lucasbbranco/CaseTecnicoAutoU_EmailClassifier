"""
File Processor Service
======================
Serviço responsável por processar e extrair texto de arquivos (.txt e .pdf).
"""

from fastapi import UploadFile, HTTPException
import PyPDF2
import io
import logging
from typing import Optional

# Importar configurações
from backend.app.core.config import settings

# Configurar logger
logger = logging.getLogger(__name__)


class FileProcessor:
    """
    Classe responsável por processar uploads de arquivos e extrair texto.
    """
    
    def __init__(self):
        """
        Inicializa o processador de arquivos
        """
        self.max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        logger.info(f"FileProcessor inicializado (max: {settings.MAX_FILE_SIZE_MB}MB)")
    
    async def process_file(self, file: UploadFile) -> str:
        """
        Processa um arquivo e extrai seu texto.
        
        Args:
            file: Arquivo enviado via upload
            
        Returns:
            str: Texto extraído do arquivo
            
        Raises:
            HTTPException: Se houver erro no processamento
        """
        try:
            # Ler conteúdo do arquivo
            content = await file.read()
            
            # Validar tamanho
            if len(content) > self.max_size_bytes:
                raise HTTPException(
                    status_code=400,
                    detail=f"Arquivo muito grande. Máximo: {settings.MAX_FILE_SIZE_MB}MB"
                )
            
            # Processar baseado na extensão
            if file.filename.endswith('.txt'):
                text = await self._process_txt(content)
            elif file.filename.endswith('.pdf'):
                text = await self._process_pdf(content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Formato não suportado. Use .txt ou .pdf"
                )
            
            logger.info(f"Arquivo processado: {len(text)} caracteres extraídos")
            return text
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar arquivo: {str(e)}"
            )
    
    
    async def _process_txt(self, content: bytes) -> str:
        """
        Processa arquivo .txt e extrai texto.
        
        Args:
            content: Conteúdo binário do arquivo
            
        Returns:
            str: Texto extraído
        """
        try:
            # Tentar decodificar com UTF-8
            text = content.decode('utf-8')
            logger.info("Arquivo .txt decodificado com UTF-8")
            return text.strip()
            
        except UnicodeDecodeError:
            try:
                # Tentar com latin-1 se UTF-8 falhar
                text = content.decode('latin-1')
                logger.info("Arquivo .txt decodificado com Latin-1")
                return text.strip()
            except Exception as e:
                logger.error(f"Erro ao decodificar .txt: {str(e)}")
                raise ValueError("Não foi possível decodificar o arquivo .txt")
    
    
    async def _process_pdf(self, content: bytes) -> str:
        """
        Processa arquivo .pdf e extrai texto.
        
        Args:
            content: Conteúdo binário do arquivo
            
        Returns:
            str: Texto extraído
        """
        try:
            # Criar objeto BytesIO para PyPDF2
            pdf_file = io.BytesIO(content)
            
            # Ler PDF
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Verificar se o PDF tem páginas
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                raise ValueError("PDF não contém páginas")
            
            logger.info(f"PDF com {num_pages} página(s)")
            
            # Extrair texto de todas as páginas
            text_parts = []
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            # Juntar texto de todas as páginas
            full_text = "\n".join(text_parts).strip()
            
            if not full_text:
                raise ValueError("Não foi possível extrair texto do PDF")
            
            logger.info(f"Texto extraído do PDF: {len(full_text)} caracteres")
            return full_text
            
        except Exception as e:
            logger.error(f"Erro ao processar PDF: {str(e)}")
            raise ValueError(f"Erro ao processar PDF: {str(e)}")
    
    
    def validate_file_type(self, filename: str) -> bool:
        """
        Valida se o tipo de arquivo é suportado.
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            bool: True se válido
        """
        return filename.endswith(('.txt', '.pdf'))