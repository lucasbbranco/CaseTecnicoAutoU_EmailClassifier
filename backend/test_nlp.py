"""
Teste do processamento NLP
"""
from app.utils.text_cleaner import TextCleaner

# Criar instância
cleaner = TextCleaner()

# Texto de teste
texto = """
Prezados,

Gostaria de solicitar o status da minha requisição #12345 que foi aberta na 
semana passada. Ainda não recebi nenhum retorno e o prazo está próximo do vencimento.

Aguardo retorno urgente.

Atenciosamente,
João Silva
"""

print("=" * 60)
print("TEXTO ORIGINAL:")
print("=" * 60)
print(texto)
print()

print("=" * 60)
print("LIMPEZA BÁSICA:")
print("=" * 60)
cleaned = cleaner.clean(texto)
print(cleaned)
print()

print("=" * 60)
print("PROCESSAMENTO NLP COMPLETO:")
print("=" * 60)
nlp_processed = cleaner.apply_nlp_preprocessing(texto)
print(nlp_processed)
print()

print("=" * 60)
print("ANÁLISE:")
print("=" * 60)
print(f"Original: {len(texto)} caracteres")
print(f"Limpeza: {len(cleaned)} caracteres")
print(f"NLP: {len(nlp_processed)} caracteres")
print(f"Redução: {((len(texto) - len(nlp_processed)) / len(texto) * 100):.1f}%")
