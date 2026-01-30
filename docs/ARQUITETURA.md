# Arquitetura

## Como Funciona (Alto Nível)

**Frontend** → Usuário coloca o texto → **Backend** → Limpa e processa → **IA (Groq)** → Retorna classificação + resposta sugerida

## Componentes

### Frontend (O que o usuário vê)

- HTML5 + CSS3 + JavaScript vanilla (sem frameworks pesados)
- Interface simples com dois campos: colar texto ou fazer upload de arquivo
- Mostra a classificação, confiança e resposta sugerida

### Backend (O motor)

**FastAPI** - Framework Python moderno e rápido.

A aplicação é dividida em camadas:
- **API** - Recebe requisições do usuário
- **Services** - Orquestra tudo (chama NLP, chama IA, monta resposta)
- **Utils** - Funções auxiliares (limpeza de texto, validações)
- **Core** - Configurações e prompts para a IA

Principais responsabilidades:
1. Recebe email em texto ou arquivo
2. Extrai texto (se PDF ou TXT)
3. Limpa e processa com NLP (remove stopwords, faz stemming)
4. Envia para a IA classificar
5. Gera uma resposta automática
6. Retorna tudo pro frontend

### IA (Groq API + Llama 3.1)

Usei o modelo Llama 3.1 70B do Groq. Por quê?
- Rápido (classifica em ~1 segundo)
- Excelente com português
- Gratuito para testes
- Modelo open source da Meta

## O Fluxo (Texto)

1. Usuário cola um email no frontend
2. Frontend valida (não está vazio? tem pelo menos 10 caracteres?)
3. Envia POST para `/api/classify-text`
4. Backend recebe, valida novamente com Pydantic
5. Passa pelo TextCleaner (NLTK) - remove stopwords, faz stemming
6. Envia para Groq/Llama: "Classifica esse email"
7. IA responde: PRODUTIVO ou IMPRODUTIVO + justificativa
8. Backend faz segunda chamada: "Gera uma resposta"
9. Monta JSON com tudo: classificação, confiança, resposta
10. Frontend recebe e mostra pro usuário

Upload de arquivo é basicamente igual, mas antes extrai o texto do .txt ou .pdf.

## Por que essas escolhas?

**FastAPI?** Framework Python rápido, com validação automática e documentação interativa grátis. Perfeito para APIs modernas e meu objeto de estudo mais forte.

**Groq/Llama?** Rápido (1-2s), bom com português, gratuito, open source. Melhor custo-benefício.

**NLP (NLTK)?** Limpa o texto antes de mandar pra IA. Remove ruído, foca em palavras importantes. Melhora precisão e economiza tokens.

**Vanilla JS?** Zero dependências = carrega rápido. Sem complicação.

**Arquitetura em camadas?** Cada parte tem uma responsabilidade. Fácil de testar, manter e expandir depois.

## Boas Práticas

- **Código limpo:** Nomes claros, funções pequenas, type hints por tudo
- **Erros:** Tratados em múltiplas camadas (frontend, Pydantic, serviços, API)
- **Segurança:** API key em variável de ambiente, arquivo .env no .gitignore, validação rigorosa
- **Logging:** Registra o que acontece para debugar depois

## Performance e Limites

**Tempos atuais:**
- Classificação: ~1-2 segundos
- Frontend: ~50KB (sem dependências pesadas)

**Limites:**
- Texto: 10.000 caracteres máximo
- Arquivo: 5MB máximo
- Timeout: 30 segundos por requisição
- Taxa: Groq limita requisições gratuitas (respeitado)

## O que posso fazer futuramente:

- Dashboard com estatísticas
- Persistência em banco de dados
- Feedback dos usuários para melhorar
- Integração com Gmail/Outlook (Foco principal)
- Modelos customizados por empresa

---

**Última atualização:** 30 de Janeiro de 2026
