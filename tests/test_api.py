"""
Test Script - Email Classifier
===============================
Script para testar o classificador de emails localmente.

USO:
    python test_classifier.py
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import List, Dict

# Adicionar pasta backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.classifier_enhanced import EmailClassifier
from app.core.config import settings


# ==================== EMAILS DE TESTE ====================

TEST_EMAILS = [
    {
        "id": 1,
        "categoria_esperada": "PRODUTIVO",
        "texto": """Prezada Equipe de Suporte,

Gostaria de solicitar uma atualização sobre a requisição #12345 que abri na última segunda-feira.

A solicitação refere-se à correção de um erro no sistema de pagamentos que está impedindo o processamento de transações acima de R$ 10.000,00.

Aguardo retorno com urgência.

Atenciosamente,
João Silva"""
    },
    {
        "id": 2,
        "categoria_esperada": "PRODUTIVO",
        "texto": """Olá,

Estou tentando gerar o relatório de transações mas recebo erro: "Timeout - operação não concluída".

Já tentei limpar cache e usar outro navegador, mas nada funcionou. Vocês podem me ajudar?

Preciso enviar esse relatório para a diretoria até amanhã.

Maria Santos"""
    },
    {
        "id": 3,
        "categoria_esperada": "PRODUTIVO",
        "texto": """Prezados,

Venho registrar minha insatisfação com o atendimento recebido no último sábado.

O atendente encerrou o chat sem resolver minha questão e até agora não recebi retorno.

Exijo posicionamento formal e resolução do problema de acesso à minha conta.

Paula Oliveira"""
    },
    {
        "id": 4,
        "categoria_esperada": "IMPRODUTIVO",
        "texto": """Olá equipe,

Passando apenas para desejar a todos um Feliz Ano Novo repleto de realizações!

Que 2026 seja incrível para todos nós.

Um abraço,
Carlos"""
    },
    {
        "id": 5,
        "categoria_esperada": "IMPRODUTIVO",
        "texto": """Equipe,

Apenas gostaria de agradecer pela ajuda de ontem. Vocês são incríveis!

Muito obrigada por tudo!

Ana Paula"""
    },
    {
        "id": 6,
        "categoria_esperada": "IMPRODUTIVO",
        "texto": """MENSAGEM DA SEMANA

"O único lugar onde sucesso vem antes de trabalho é no dicionário."

Lembre-se: cada dia é uma nova oportunidade!

Foco nos objetivos!
Você é capaz de tudo!

Compartilhe com amigos!"""
    }
]


# ==================== FUNÇÕES DE TESTE ====================

def print_separator(char="=", length=80):
    """Imprime linha separadora"""
    print(char * length)


def print_header(text: str):
    """Imprime cabeçalho formatado"""
    print_separator()
    print(f" {text}")
    print_separator()


def print_email(email: Dict):
    """Imprime email formatado"""
    print(f"\nEMAIL #{email['id']} (Esperado: {email['categoria_esperada']})")
    print("-" * 80)
    print(email['texto'][:200] + "..." if len(email['texto']) > 200 else email['texto'])
    print("-" * 80)


def print_result(result: Dict, email: Dict):
    """Imprime resultado da classificação"""
    if not result.get("success"):
        print(f"\nERRO: {result.get('error')}")
        return
    
    classification = result["classification"]
    confidence = result["confidence"]
    expected = email["categoria_esperada"]
    
    # Verificar se acertou
    correct = classification == expected
    status = "[OK]" if correct else "[ERRO]"
    
    print(f"\n{status} RESULTADO:")
    print(f"   Classificação: {classification}")
    print(f"   Confiança: {confidence:.1%}")
    print(f"   Justificativa: {result['justification']}")
    print(f"   Tempo: {result['processing_time_ms']}ms")
    
    if result.get("cached"):
        print(f"   (Resultado do cache)")
    
    print(f"\nRESPOSTA SUGERIDA:")
    print("-" * 80)
    response_lines = result["suggested_response"].split('\n')
    for line in response_lines[:10]:  # Primeiras 10 linhas
        print(f"   {line}")
    if len(response_lines) > 10:
        print("   ...")
    print("-" * 80)


async def test_single_email(classifier: EmailClassifier, email: Dict):
    """Testa um único email"""
    print_email(email)
    
    result = await classifier.classify_email(email["texto"])
    
    print_result(result, email)
    
    return result


async def test_all_emails(classifier: EmailClassifier):
    """Testa todos os emails"""
    results = []
    correct_count = 0
    
    for email in TEST_EMAILS:
        result = await test_single_email(classifier, email)
        
        if result.get("success"):
            results.append(result)
            if result["classification"] == email["categoria_esperada"]:
                correct_count += 1
        
        print("\n")
        await asyncio.sleep(0.5)  # Pequeno delay entre requisições
    
    return results, correct_count


def print_summary(results: List[Dict], correct_count: int, metrics: Dict):
    """Imprime resumo dos testes"""
    print_header("RESUMO DOS TESTES")
    
    total = len(TEST_EMAILS)
    accuracy = (correct_count / total * 100) if total > 0 else 0
    
    print(f"\nESTATÍSTICAS:")
    print(f"   Total de emails testados: {total}")
    print(f"   Classificações corretas: {correct_count}")
    print(f"   Acurácia: {accuracy:.1f}%")
    
    if results:
        avg_confidence = sum(r["confidence"] for r in results) / len(results)
        avg_time = sum(r["processing_time_ms"] for r in results) / len(results)
        
        print(f"   Confiança média: {avg_confidence:.1%}")
        print(f"   Tempo médio: {avg_time:.0f}ms")
    
    print(f"\nMÉTRICAS DO CLASSIFICADOR:")
    for key, value in metrics.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}: {value}")
    
    print_separator()


async def test_cache_functionality(classifier: EmailClassifier):
    """Testa funcionalidade de cache"""
    print_header("TESTE DE CACHE")
    
    email = TEST_EMAILS[0]
    
    print("\n1. Primeira requisição (sem cache):")
    result1 = await classifier.classify_email(email["texto"])
    time1 = result1.get("processing_time_ms", 0)
    cached1 = result1.get("cached", False)
    print(f"   Tempo: {time1}ms | Cached: {cached1}")
    
    print("\n2. Segunda requisição (deve usar cache):")
    result2 = await classifier.classify_email(email["texto"])
    time2 = result2.get("processing_time_ms", 0)
    cached2 = result2.get("cached", False)
    print(f"   Tempo: {time2}ms | Cached: {cached2}")
    
    if cached2:
        speedup = time1 / time2 if time2 > 0 else 0
        print(f"\n   [OK] Cache funcionando! {speedup:.1f}x mais rápido")
    else:
        print(f"\n   [AVISO] Cache não detectado")
    
    print_separator()


async def test_error_handling(classifier: EmailClassifier):
    """Testa tratamento de erros"""
    print_header("TESTE DE TRATAMENTO DE ERROS")
    
    test_cases = [
        {"name": "Texto vazio", "text": ""},
        {"name": "Texto muito curto", "text": "Oi"},
        {"name": "Apenas espaços", "text": "   \n   \n   "},
    ]
    
    for case in test_cases:
        print(f"\nTestando: {case['name']}")
        result = await classifier.classify_email(case["text"])
        
        if not result.get("success"):
            print(f"   [OK] Erro capturado: {result.get('error')}")
        else:
            print(f"   [AVISO] Deveria ter falhado mas passou")
    
    print_separator()


# ==================== MAIN ====================

async def main():
    """Função principal"""
    print_header("EMAIL CLASSIFIER - SCRIPT DE TESTE")
    
    # Verificar configuração
    if not settings.GROQ_API_KEY:
        print("\n[AVISO] GROQ_API_KEY não configurada!")
        print("[INFO] O classificador rodará em MODO SIMULAÇÃO")
        print("[INFO] Para usar a API real, configure a variável de ambiente\n")
        input("Pressione ENTER para continuar...")
    
    # Inicializar classificador
    print("\nInicializando classificador...")
    classifier = EmailClassifier(cache_enabled=True, retry_attempts=3)
    
    # Testes principais
    print("\n\n")
    print_header("TESTE 1: CLASSIFICAÇÃO DE EMAILS")
    results, correct_count = await test_all_emails(classifier)
    
    # Teste de cache
    print("\n\n")
    await test_cache_functionality(classifier)
    
    # Teste de erros
    print("\n\n")
    await test_error_handling(classifier)
    
    # Resumo final
    print("\n\n")
    metrics = classifier.get_metrics()
    print_summary(results, correct_count, metrics)
    
    print("\nTestes concluídos!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[AVISO] Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n\n[ERRO] Erro ao executar testes: {str(e)}")
        import traceback
        traceback.print_exc()