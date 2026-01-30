import sys
import os

# Adiciona o diretório raiz ao Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Configura NLTK para usar /tmp (Vercel permite escrever aqui)
os.environ['NLTK_DATA'] = '/tmp/nltk_data'

# Baixa dados do NLTK para /tmp
try:
    import nltk
    nltk.data.path.append('/tmp/nltk_data')
    nltk.download('punkt', download_dir='/tmp/nltk_data', quiet=True)
    nltk.download('stopwords', download_dir='/tmp/nltk_data', quiet=True)
    nltk.download('rslp', download_dir='/tmp/nltk_data', quiet=True)
    nltk.download('punkt_tab', download_dir='/tmp/nltk_data', quiet=True)
except Exception as e:
    print(f"Aviso NLTK: {e}")
    pass

from backend.app.main import app

__all__ = ["app"]
