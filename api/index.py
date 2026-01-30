import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Importa a app
from backend.app.main import app

# Vercel precisa de 'app' ou 'handler'
handler = app
