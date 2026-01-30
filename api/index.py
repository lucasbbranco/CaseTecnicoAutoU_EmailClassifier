import sys
import os

# Adiciona o diretório raiz ao Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Baixa dados do NLTK (necessário no primeiro run)
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('rslp', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    pass

from backend.app.main import app

__all__ = ["app"]
