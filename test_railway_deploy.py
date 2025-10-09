#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Deploy Railway - Versão Definitiva
Verifica se o bot está funcionando no Railway após o deploy
"""

import requests
import json
import time
from datetime import datetime

def test_railway_urls():
    """Testa URLs comuns do Railway"""
    
    # URLs possíveis do Railway
    possible_urls = [
        "https://agente-twitter-production.up.railway.app",
        "https://agente-twitter-production-1234.up.railway.app",
        "https://agente-twitter.up.railway.app",
        "https://drtrafego-agente-twitter.up.railway.app",
        "https://bot-twitter.up.railway.app"
    ]
    
    print("🚀 TESTE DE DEPLOY RAILWAY - VERSÃO DEFINITIVA")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print()
    
    working_urls = []
    
    for url in possible_urls:
        print(f"🔍 Testando: {url}")
        
        try:
            # Teste de conectividade
            response = requests.get(url, timeout=10)
            
            print(f"   📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ SUCESSO! Bot funcionando")
                    print(f"   🤖 Bot Running: {data.get('bot_running', 'N/A')}")
                    print(f"   📈 Daily Posts: {data.get('daily_posts', 'N/A')}/{data.get('daily_limit', 'N/A')}")
                    print(f"   🕐 Last Activity: {data.get('last_activity', 'N/A')}")
                    print(f"   ❌ Error: {data.get('error', 'None')}")
                    working_urls.append(url)
                    
                except json.JSONDecodeError:
                    print(f"   ⚠️  Resposta não é JSON válido")
                    print(f"   📄 Content: {response.text[:100]}...")
                    
            elif response.status_code == 404:
                print(f"   ❌ Não encontrado (404)")
            elif response.status_code == 503:
                print(f"   ⏳ Serviço indisponível (503) - Pode estar fazendo deploy")
            else:
                print(f"   ⚠️  Status inesperado: {response.status_code}")
                
        except requests.exceptions.ConnectTimeout:
            print(f"   ⏰ Timeout de conexão")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Erro de conexão")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro na requisição: {e}")
        
        print()
    
    print("=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)
    
    if working_urls:
        print(f"✅ URLs funcionando: {len(working_urls)}")
        for url in working_urls:
            print(f"   🌐 {url}")
        print()
        print("🎉 DEPLOY REALIZADO COM SUCESSO!")
        print("🤖 Bot está rodando no Railway!")
        
    else:
        print("❌ Nenhuma URL funcionando")
        print()
        print("🔧 POSSÍVEIS PROBLEMAS:")
        print("   1. Deploy ainda em andamento (aguarde 2-3 minutos)")
        print("   2. URL incorreta (verifique no Dashboard do Railway)")
        print("   3. Erro no build (verifique logs no Railway)")
        print("   4. Variáveis de ambiente faltando")
        print()
        print("📋 PRÓXIMOS PASSOS:")
        print("   1. Acesse o Dashboard do Railway")
        print("   2. Verifique a aba 'Deployments'")
        print("   3. Confira os logs de build e runtime")
        print("   4. Confirme a URL pública correta")
        print("   5. Verifique as variáveis de ambiente")

if __name__ == "__main__":
    test_railway_urls()