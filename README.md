# 📧 Email Classifier - Classificação Inteligente de Emails com IA

Sistema de classificação automática de emails corporativos utilizando IA (Llama 3.1 via Groq) para identificar emails produtivos (que requerem ação) e improdutivos (mensagens sociais/informativas).

## 🎯 Funcionalidades

- **Classificação Automática**: Identifica se um email é PRODUTIVO ou IMPRODUTIVO
- **Análise com IA**
- **Processamento NLP**: Tokenização, stemming e remoção de stopwords em português
- **Resposta Automática**: Gera sugestão de resposta contextualizada
- **Upload de Arquivos**: Suporta .txt e .pdf
- **Interface Profissional**: UI limpa e responsiva
- **API RESTful**: Backend FastAPI

## 🚀 Tecnologias

### Backend
- **FastAPI**: Framework web moderno e rápido
- **Groq AI**: API para LLMs (Llama 3.1)
- **NLTK**: Processamento de Linguagem Natural (NLP)
- **PyPDF2**: Extração de texto de PDFs
- **Pydantic**: Validação de dados

### Frontend
- **HTML/CSS**: Interface responsiva
- **JavaScript**: Sem dependências externas
- **Design Moderno**: Gradient, animações

## 📋 Pré-requisitos

- Python 3.8+
- Conta Groq (para obter API key)
- Navegador moderno

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd "Case Técnico AutoU"
```

### 2. Configure o Backend

```bash
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua API key
# GROQ_API_KEY=sua_key_aqui
```

**📝 Como obter a API Key do Groq:**
1. Acesse: https://console.groq.com/keys
2. Crie uma conta (gratuita)
3. Gere uma nova API key
4. Cole no arquivo `.env`

### 4. Inicie o Backend

```bash
# Na pasta backend:
uvicorn app.main:app --reload

# O servidor estará rodando em: http://localhost:8000
# Documentação da API: http://localhost:8000/docs
```

### 5. Abra o Frontend

```bash
# Abrir um servidor local:
cd ../frontend
python -m http.server 3000

# Acesse: http://localhost:3000
```

## 🔧 Configuração

### Arquivo .env

```env
# API Key do Groq (OBRIGATÓRIO)
GROQ_API_KEY=your_groq_api_key_here

# Configurações do Modelo
GROQ_MODEL=llama-3.1-8b-instant
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=500
AI_TIMEOUT=30
```

### Variáveis Disponíveis

- `GROQ_API_KEY`: Sua chave de API do Groq (**obrigatório**)
- `GROQ_MODEL`: Modelo a ser usado (padrão: llama-3.1-8b-instant)
- `AI_TEMPERATURE`: Criatividade da IA (0.0-1.0, padrão: 0.3)
- `AI_MAX_TOKENS`: Limite de tokens na resposta (padrão: 500)
- `AI_TIMEOUT`: Timeout em segundos (padrão: 30)

## 🎮 Como Usar (Localmente)

### Via Interface Web

1. Abra `http://localhost:3000` no navegador
2. Escolha uma das opções:
   - **Upload de Arquivo**: Arraste um .txt ou .pdf
   - **Colar Texto**: Cole o conteúdo do email
3. Clique em "Classificar Email"
4. Visualize:
   - Categoria (PRODUTIVO/IMPRODUTIVO)
   - Nível de confiança
   - Justificativa da classificação
   - Resposta automática sugerida

### Via API (cURL)

```bash
# Classificar texto direto
curl -X POST http://localhost:8000/api/classify-text \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Prezados, gostaria de solicitar o status da requisição #12345"
  }'

# Upload de arquivo
curl -X POST http://localhost:8000/api/classify-file \
  -F "file=@email.txt"
```


## 📊 Exemplos de Classificação

### Email PRODUTIVO
```
"Prezados, estou com um problema no sistema de pagamentos. 
O erro persiste desde ontem e preciso de suporte urgente."

→ PRODUTIVO (95% confiança)
Justificativa: Email relata problema técnico e solicita suporte urgente
```

### Email IMPRODUTIVO
```
"Olá equipe! Feliz Natal a todos! Que 2026 seja repleto de 
sucesso e realizações para nossa equipe."

→ IMPRODUTIVO (98% confiança)
Justificativa: Mensagem de felicitação sazonal sem necessidade de ação
```
### Possui mais testes inclusos nos arquivos.

## 🧪 Testes

```bash
# Executar testes
cd backend
python -m pytest tests/

# Ou use o script de teste incluído
python tests/test_api.py
```

## 📖 Documentação da API

Acesse `http://localhost:8000/docs` para ver a documentação interativa (Swagger UI) com todos os endpoints disponíveis.

### Endpoints Principais

- `GET /api/health` - Health check
- `POST /api/classify-text` - Classifica texto direto
- `POST /api/classify-file` - Classifica arquivo (.txt ou .pdf)

## 🔒 Segurança

⚠️ **IMPORTANTE:**

- **NUNCA** commite o arquivo `.env` no Git
- **NUNCA** exponha sua `GROQ_API_KEY` publicamente
- Use `.env.example` como template
- Revogue e regenere keys se expostas acidentalmente


## 🚢 Deploy

### Feito em Vercel

Para usar a aplicação online, sem necessidade de instalação local, acesse:
[Email Classifier](https://case-tecnico-auto-u-email-classifie.vercel.app).

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

Desenvolvido como case técnico para demonstração de habilidades em:
- Desenvolvimento Full Stack
- Integração com APIs de IA
- Processamento de Linguagem Natural
- Clean Code e Boas Práticas

## 🙏 Agradecimentos

Um agradecimento especial à **[AutoU](https://www.autou.io)** por propor este desafio inspirador. Este case técnico foi uma oportunidade excepcional de explorar tópicos fascinantes como integração com IA, processamento de linguagem natural e arquitetura de software moderna. A proposta de um classificador de emails com contexto corporativo brasileiro foi tanto desafiadora quanto significativa.

---

⭐ Se este projeto foi útil de alguma forma, considere dar uma estrela!