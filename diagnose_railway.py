#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO AVANÇADO RAILWAY
Verifica possíveis problemas que podem estar causando falha no deploy
"""

import requests
import time
import sys
from datetime import datetime

def test_url_with_details(url):
    """Testa URL com detalhes completos"""
    print(f"\n🔍 Testando: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"   📊 Status: {response.status_code}")
        print(f"   📏 Content-Length: {len(response.text)}")
        print(f"   🕒 Response Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            print(f"   ✅ SUCESSO!")
            if len(response.text) > 0:
                print(f"   📄 Primeiros 200 chars: {response.text[:200]}")
            return True
        elif response.status_code == 404:
            print(f"   ❌ 404 - Serviço não encontrado")
        elif response.status_code == 500:
            print(f"   💥 500 - Erro interno do servidor")
            print(f"   📄 Erro: {response.text[:500]}")
        elif response.status_code == 502:
            print(f"   🚫 502 - Bad Gateway (deploy pode estar falhando)")
        elif response.status_code == 503:
            print(f"   ⏳ 503 - Serviço indisponível (deploy em andamento?)")
        else:
            print(f"   ⚠️  Status inesperado: {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ TIMEOUT - Servidor não responde")
    except requests.exceptions.ConnectionError:
        print(f"   🔌 CONEXÃO FALHOU - URL pode estar incorreta")
    except Exception as e:
        print(f"   💥 ERRO: {e}")
    
    return False

def main():
    print("🚀 DIAGNÓSTICO AVANÇADO RAILWAY")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # URLs mais prováveis baseadas no padrão Railway
    urls_to_test = [
        "https://agente-twitter-production.up.railway.app",
        "https://agente-twitter-production.up.railway.app/status",
        "https://agente-twitter.up.railway.app", 
        "https://agente-twitter.up.railway.app/status",
        "https://drtrafego-agente-twitter.up.railway.app",
        "https://drtrafego-agente-twitter.up.railway.app/status",
        "https://bot-twitter.up.railway.app",
        "https://bot-twitter.up.railway.app/status"
    ]
    
    working_urls = []
    
    for url in urls_to_test:
        if test_url_with_details(url):
            working_urls.append(url)
        time.sleep(1)  # Evitar rate limit
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DO DIAGNÓSTICO")
    print("=" * 60)
    
    if working_urls:
        print(f"✅ URLs funcionando: {len(working_urls)}")
        for url in working_urls:
            print(f"   🟢 {url}")
    else:
        print("❌ NENHUMA URL FUNCIONANDO")
        print("\n🔧 POSSÍVEIS CAUSAS:")
        print("   1. 🏗️  Deploy ainda em andamento (>5min é anormal)")
        print("   2. 💥 Erro no build/runtime (verifique logs Railway)")
        print("   3. 🔑 Variáveis de ambiente faltando")
        print("   4. 🐍 Problema com Python/dependências")
        print("   5. 🌐 URL incorreta (verifique Dashboard)")
        print("   6. 💾 Problema de memória/recursos")
        
        print("\n📋 AÇÕES RECOMENDADAS:")
        print("   1. 🖥️  Acesse Railway Dashboard")
        print("   2. 📊 Verifique aba 'Deployments'")
        print("   3. 📝 Confira logs de build e runtime")
        print("   4. 🔍 Confirme URL pública correta")
        print("   5. ⚙️  Verifique variáveis de ambiente")
        print("   6. 🔄 Considere redeploy manual")

if __name__ == "__main__":
    main()