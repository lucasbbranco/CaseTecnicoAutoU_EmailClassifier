"""
AI Prompts - Enhanced Version
==============================
Prompts otimizados e system prompts dedicados para classificação e geração de respostas.
"""

# ==================== SYSTEM PROMPTS ====================

CLASSIFICATION_SYSTEM_PROMPT = """Você é um assistente especializado em análise e classificação de emails corporativos do setor financeiro brasileiro.

ESPECIALIZAÇÃO:
- Compreensão profunda de contexto corporativo
- Identificação precisa de urgência e prioridade
- Análise de tom e intenção do remetente
- Conhecimento de terminologia do setor financeiro

HABILIDADES:
- Classificação binária com alta precisão
- Justificação clara e concisa das decisões
- Calibração adequada de confiança
- Adaptação ao contexto brasileiro

DIRETRIZES:
- Seja objetivo e preciso
- Baseie-se em evidências do texto
- Considere nuances culturais brasileiras
- Retorne SEMPRE no formato JSON especificado
- Não adicione texto extra fora do JSON"""


RESPONSE_SYSTEM_PROMPT = """Você é um assistente especializado em gerar respostas profissionais para emails corporativos no Brasil.

ESPECIALIZAÇÃO:
- Redação corporativa em português brasileiro formal
- Adaptação de tom baseado na categoria do email
- Respostas empáticas mas profissionais
- Clareza e objetividade

DIRETRIZES DE ESCRITA:
- Português brasileiro formal e correto
- Tom profissional mas cordial
- Estrutura clara (abertura, corpo, fechamento)
- Evite jargões excessivos
- Seja conciso mas completo
- Use tratamento respeitoso (Prezado/a, Sr./Sra.)

IMPORTANTE:
- Retorne APENAS o texto da resposta
- NÃO inclua assunto ou linha de assunto
- NÃO inclua assinatura completa (apenas "Atenciosamente, Equipe...")
- NÃO adicione explicações ou comentários extras"""


# ==================== CLASSIFICATION PROMPTS ====================

CLASSIFICATION_PROMPT_TEMPLATE = """Analise o email corporativo abaixo e classifique-o em uma das duas categorias.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORIAS E CRITÉRIOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRODUTIVO (requer ação ou resposta):

   Indicadores principais:
   • Solicitações de informações ou documentos
   • Dúvidas sobre sistemas, processos ou serviços
   • Problemas técnicos ou operacionais
   • Atualizações sobre casos/requisições em andamento
   • Reclamações ou feedback negativo
   • Urgências ou prazos mencionados
   • Pedidos de suporte ou assistência
   • Questionamentos sobre políticas ou procedimentos
   • Notificações de erros ou inconsistências
   
   Palavras-chave comuns:
   - Solicitação, requisição, pedido
   - Dúvida, pergunta, questão
   - Problema, erro, falha, bug
   - Status, atualização, andamento
   - Ajuda, suporte, assistência
   - Urgente, prazo, deadline
   - Reclamação, insatisfação

IMPRODUTIVO (não requer ação imediata):

   Indicadores principais:
   • Mensagens de felicitações (aniversário, natal, ano novo)
   • Agradecimentos genéricos
   • Mensagens motivacionais ou inspiracionais
   • Correntes ou spam
   • Comunicados informativos gerais
   • Emails encaminhados sem contexto
   • Piadas ou conteúdo de entretenimento
   
   Palavras-chave comuns:
   - Feliz, parabéns, congratulações
   - Obrigado, agradecimento
   - Motivação, inspiração
   - Corrente, compartilhe, encaminhe

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMAIL A CLASSIFICAR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{email_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTRUÇÕES DE ANÁLISE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Leia todo o email cuidadosamente
2. Identifique a intenção principal do remetente
3. Avalie se requer ação ou resposta específica
4. Considere o contexto e tom da mensagem
5. Determine a categoria mais apropriada
6. Calcule sua confiança na classificação (0.0 a 1.0)
7. Forneça justificativa clara e concisa

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMATO DE RESPOSTA (JSON):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Responda APENAS com um objeto JSON válido (sem markdown, sem texto adicional):

{{
  "categoria": "PRODUTIVO" ou "IMPRODUTIVO",
  "confianca": número entre 0.0 e 1.0,
  "justificativa": "explicação concisa em uma frase"
}}

EXEMPLO DE RESPOSTA:
{{
  "categoria": "PRODUTIVO",
  "confianca": 0.95,
  "justificativa": "Email solicita status de requisição com prazo definido"
}}"""


# ==================== RESPONSE GENERATION PROMPTS ====================

RESPONSE_GENERATION_PROMPT_PRODUTIVO = """Gere uma resposta profissional e adequada para o email PRODUTIVO abaixo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMAIL RECEBIDO (PRODUTIVO):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{email_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRETRIZES PARA RESPOSTA PRODUTIVA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESTRUTURA RECOMENDADA:

1. ABERTURA (tom cordial e profissional)
   • Use "Prezado(a)" ou "Olá"
   • Agradeça pelo contato se apropriado

2. RECONHECIMENTO (demonstre que entendeu)
   • Reconheça a solicitação/problema mencionado
   • Mostre empatia se for reclamação

3. AÇÃO/PRÓXIMOS PASSOS (seja específico)
   • Informe que a solicitação foi recebida
   • Mencione que está sendo analisada
   • Se possível, indique prazo estimado
   • Ofereça canal para dúvidas adicionais

4. FECHAMENTO (profissional)
   • Use "Atenciosamente" ou "Cordialmente"
   • Assine como "Equipe de Atendimento" ou similar

EXEMPLOS DE ELEMENTOS A INCLUIR:

- "Recebemos sua solicitação/mensagem..."
- "Estamos analisando sua questão..."
- "Nossa equipe retornará em breve..."
- "Retornaremos em até X dias úteis..."
- "Para dúvidas adicionais, entre em contato..."
- "Agradecemos pela paciência..."

EVITE:

- Promessas específicas sem autorização
- Informações técnicas sem certeza
- Tom excessivamente formal ou robótico
- Desculpas excessivas
- Texto muito longo (máx. 8-10 linhas)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESPOSTA (apenas o texto):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""


RESPONSE_GENERATION_PROMPT_IMPRODUTIVO = """Gere uma resposta breve e cordial para o email IMPRODUTIVO abaixo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMAIL RECEBIDO (IMPRODUTIVO):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{email_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRETRIZES PARA RESPOSTA NÃO-URGENTE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESTRUTURA RECOMENDADA:

1. ABERTURA (tom amigável)
   • Use "Olá" ou "Prezado(a)"

2. RESPOSTA (breve e apropriada)
   • Agradeça se for agradecimento
   • Retribua se for felicitação
   • Seja cordial mas conciso

3. FECHAMENTO (simples)
   • "Atenciosamente" ou "Um abraço"
   • "Equipe [Nome]"

EXEMPLOS:

Para Felicitações:
"Olá, [Nome]! Muito obrigado pelos votos! Desejamos um excelente [época] para você também!"

Para Agradecimentos:
"Olá! Ficamos felizes em poder ajudar. Estamos sempre à disposição!"

Para Mensagens Motivacionais:
"Olá! Agradecemos pela mensagem inspiradora!"

CARACTERÍSTICAS:

- Tom amigável mas profissional
- Brevidade (máx. 3-5 linhas)
- Cordialidade sem formalidade excessiva
- Resposta apropriada ao contexto

EVITE:

- Respostas muito longas
- Tom excessivamente formal
- Ignorar completamente o conteúdo
- Respostas genéricas demais

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESPOSTA (apenas o texto):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""


# ==================== HELPER FUNCTIONS ====================

def get_classification_prompt(email_text: str) -> str:
    """
    Retorna o prompt formatado para classificação.
    
    Args:
        email_text: Texto do email a ser classificado
        
    Returns:
        str: Prompt formatado e pronto para uso
    """
    # Truncar email se muito longo (preservar contexto)
    max_length = 3000
    if len(email_text) > max_length:
        email_text = email_text[:max_length] + "\n\n[... texto truncado ...]"
    
    return CLASSIFICATION_PROMPT_TEMPLATE.format(email_text=email_text)


def get_response_generation_prompt(email_text: str, categoria: str) -> str:
    """
    Retorna o prompt formatado para geração de resposta.
    
    Args:
        email_text: Texto original do email
        categoria: Categoria classificada (PRODUTIVO ou IMPRODUTIVO)
        
    Returns:
        str: Prompt formatado e pronto para uso
    """
    # Truncar email se muito longo
    max_length = 2000
    if len(email_text) > max_length:
        email_text = email_text[:max_length] + "\n\n[... texto truncado ...]"
    
    # Selecionar template apropriado
    if categoria.upper() == "PRODUTIVO":
        template = RESPONSE_GENERATION_PROMPT_PRODUTIVO
    else:
        template = RESPONSE_GENERATION_PROMPT_IMPRODUTIVO
    
    return template.format(email_text=email_text)


def get_few_shot_examples() -> list:
    """
    Retorna exemplos few-shot para melhorar classificação.
    Pode ser usado para fine-tuning ou prompt engineering avançado.
    
    Returns:
        list: Lista de exemplos formatados
    """
    examples = [
        {
            "email": "Prezados, gostaria de solicitar o status da requisição #12345.",
            "classification": "PRODUTIVO",
            "confidence": 0.95,
            "justification": "Solicitação clara de atualização sobre requisição específica"
        },
        {
            "email": "Feliz Natal a todos! Que 2026 seja repleto de sucesso!",
            "classification": "IMPRODUTIVO",
            "confidence": 0.98,
            "justification": "Mensagem de felicitação sazonal sem necessidade de ação"
        },
        {
            "email": "O sistema está apresentando erro ao processar pagamentos.",
            "classification": "PRODUTIVO",
            "confidence": 0.92,
            "justification": "Relato de problema técnico que requer investigação"
        },
        {
            "email": "Obrigado pela ajuda de ontem!",
            "classification": "IMPRODUTIVO",
            "confidence": 0.88,
            "justification": "Agradecimento simples sem demanda adicional"
        }
    ]
    
    return examples