"""
Text Cleaner Utility with NLP
==============================
Utilitário para limpeza e normalização de texto de emails com NLP.
Inclui: remoção de stop words, stemming e tokenização.
"""

import re
import logging
import nltk
from typing import List

# Configurar logger
logger = logging.getLogger(__name__)

# Download de recursos do NLTK (executar uma vez)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    logger.info("Baixando recursos do NLTK...")
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('rslp', quiet=True)
    logger.info("Recursos do NLTK baixados")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer


class TextCleaner:
    """Classe responsável por limpar e normalizar texto de emails com NLP."""
    
    def __init__(self):
        """Inicializa o TextCleaner com recursos de NLP."""
        self.stop_words = set(stopwords.words('portuguese'))
        self.stemmer = RSLPStemmer()
        logger.info("TextCleaner inicializado com NLP (português)")
    
    def clean(self, text: str) -> str:
        """Limpa e normaliza o texto do email."""
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'([.,!?;:])\s+', r'\1 ', text)
        text = text.strip()
        
        logger.info(f"Texto limpo: {len(text)} caracteres")
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokeniza o texto em palavras individuais."""
        try:
            tokens = word_tokenize(text.lower(), language='portuguese')
            logger.info(f"Tokenização: {len(tokens)} tokens")
            return tokens
        except Exception as e:
            logger.warning(f"Erro na tokenização: {e}")
            return text.lower().split()
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stop words dos tokens."""
        filtered_tokens = [
            token for token in tokens 
            if token.isalnum() and token not in self.stop_words
        ]
        removed_count = len(tokens) - len(filtered_tokens)
        logger.info(f"Stop words removidas: {removed_count}")
        return filtered_tokens
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Aplica stemming nos tokens."""
        stemmed = [self.stemmer.stem(token) for token in tokens]
        logger.info(f"Stemming aplicado: {len(stemmed)} tokens")
        return stemmed
    
    def apply_nlp_preprocessing(self, text: str) -> str:
        """
        Aplica pipeline completo de NLP:
        1. Limpeza básica
        2. Tokenização
        3. Remoção de stop words
        4. Stemming
        5. Reconstrução do texto
        """
        if not text:
            return ""
        
        logger.info("Iniciando processamento NLP...")
        cleaned = self.clean(text)
        tokens = self.tokenize(cleaned)
        tokens = self.remove_stopwords(tokens)
        tokens = self.stem_tokens(tokens)
        processed_text = ' '.join(tokens)
        logger.info(f"NLP completo: {len(processed_text)} caracteres finais")
        return processed_text
    
    def extract_main_content(self, text: str) -> str:
        """Extrai o conteúdo principal, removendo assinaturas."""
        signature_markers = [
            r'\n--\s*\n',
            r'\nAtenciosamente,',
            r'\nAtt,',
            r'\nCordialmente,',
            r'\n___+',
            r'\nEnviado do meu',
            r'\nSent from my',
        ]
        
        for marker in signature_markers:
            match = re.search(marker, text, re.IGNORECASE)
            if match:
                return text[:match.start()].strip()
        
        return text
