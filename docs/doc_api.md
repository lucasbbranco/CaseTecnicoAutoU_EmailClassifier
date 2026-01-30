# 📡 API - Referência Rápida

## Base URL
- **Dev:** `http://localhost:8000`
- **Prod:** `https://seu-dominio.vercel.app`

## Endpoints

### GET /api/health
Health check da API.

**Resposta (200):**
```json
{"status": "healthy", "service": "Email Classifier API"}
```

---

### POST /api/classify-text
Classifica email via texto direto.

**Body:**
```json
{"email_text": "string (min: 10, max: 10000)"}
```

**Resposta Exemplo (200):**
```json
{
  "success": true,
  "classification": "PRODUTIVO | IMPRODUTIVO",
  "confidence": 0.95,
  "justification": "string",
  "suggested_response": "string",
  "processing_time_ms": 1234
}
```

---

### POST /api/classify-file
Classifica email via upload (.txt ou .pdf).

**Body:** `multipart/form-data`
- `file`: Arquivo (.txt ou .pdf, máx 5MB)

**Resposta (200):** Mesmo formato que classify-text, com `filename` adicional

```bash
  -F "file=@email.txt"
```

---

## Validações

| Campo | Limite |
|-------|--------|
| email_text | 10 - 10.000 caracteres |
| arquivo | .txt ou .pdf, máx 5MB |
| timeout | 30 segundos |

## Status HTTP

| Código | Significado |
|--------|------------|
| 200 | Sucesso |
| 400 | Dados inválidos |
| 500 | Erro interno |

## Documentação Interativa

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

**v1.0.0** | Última atualização: 30 de Janeiro de 2026
