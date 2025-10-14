#!/usr/bin/env python3
"""
📊 MONITOR DO BOT - Acompanhamento em Tempo Real
Encontra a URL correta e monitora o status do bot
"""

import requests
import time
import json
from datetime import datetime

def test_url_detailed(url):
    """Testa URL com detalhes e retorna dados se funcionar"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            try:
                data = response.json()
                return True, data
            except:
                return True, {"raw_response": response.text[:500]}
        return False, {"status": response.status_code, "error": response.text[:200]}
    except Exception as e:
        return False, {"error": str(e)}

def generate_possible_urls():
    """Gera todas as URLs possíveis baseadas em padrões Railway"""
    base_patterns = [
        "agente-twitter",
        "agente-twitter-production", 
        "drtrafego-agente-twitter",
        "bot-twitter",
        "twitter-bot",
        "agente-twitter-bot",
        "drtrafeg0-bot",
        "railway-bot",
        "python-bot"
    ]
    
    urls = []
    for pattern in base_patterns:
        # URLs principais
        urls.append(f"https://{pattern}.up.railway.app")
        urls.append(f"https://{pattern}.up.railway.app/status")
        urls.append(f"https://{pattern}.up.railway.app/")
        
        # Com sufixos comuns
        for suffix in ["-1", "-2", "-production", "-prod", "-main"]:
            urls.append(f"https://{pattern}{suffix}.up.railway.app")
            urls.append(f"https://{pattern}{suffix}.up.railway.app/status")
    
    return urls

def monitor_bot():
    """Monitora o bot em tempo real"""
    print("🚀 MONITOR DO BOT - BUSCA AVANÇADA")
    print("=" * 60)
    print(f"⏰ Iniciado em: {datetime.now().strftime('%H:%M:%S')}")
    
    urls = generate_possible_urls()
    print(f"🔍 Testando {len(urls)} URLs possíveis...")
    
    working_urls = []
    
    for i, url in enumerate(urls, 1):
        print(f"\r🔍 Testando {i}/{len(urls)}: {url[:50]}...", end="", flush=True)
        
        success, data = test_url_detailed(url)
        if success:
            working_urls.append((url, data))
            print(f"\n✅ ENCONTRADA: {url}")
            
            # Se encontrou /status, mostra dados detalhados
            if "/status" in url and isinstance(data, dict):
                print("📊 STATUS DO BOT:")
                for key, value in data.items():
                    print(f"   {key}: {value}")
        
        time.sleep(0.5)  # Evitar rate limit
    
    print(f"\n\n{'='*60}")
    print("📋 RESULTADOS DA BUSCA")
    print("=" * 60)
    
    if working_urls:
        print(f"✅ URLs funcionando: {len(working_urls)}")
        for url, data in working_urls:
            print(f"\n🟢 {url}")
            if isinstance(data, dict) and len(data) > 1:
                print("   📊 Dados:")
                for key, value in data.items():
                    if key != "raw_response":
                        print(f"      {key}: {value}")
    else:
        print("❌ NENHUMA URL ENCONTRADA")
        print("\n💡 DICAS:")
        print("   1. Verifique a URL exata no Railway Dashboard")
        print("   2. Confirme se o deploy foi bem-sucedido")
        print("   3. Verifique se o domínio foi configurado")
        print("   4. O bot pode estar rodando em porta diferente")
    
    return working_urls

def continuous_monitor(url, interval=30):
    """Monitora continuamente uma URL específica"""
    print(f"\n🔄 MONITORAMENTO CONTÍNUO: {url}")
    print(f"⏱️  Intervalo: {interval} segundos")
    print("=" * 60)
    
    while True:
        try:
            success, data = test_url_detailed(url)
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            if success and isinstance(data, dict):
                print(f"\n⏰ {timestamp} - ✅ BOT ATIVO")
                
                # Mostra dados importantes
                important_keys = ['running', 'daily_posts', 'last_activity', 'monitored_posts', 'replies_found']
                for key in important_keys:
                    if key in data:
                        print(f"   📊 {key}: {data[key]}")
                        
                # Detecta mudanças
                if 'daily_posts' in data:
                    posts = data['daily_posts']
                    if posts > 0:
                        print(f"   🎯 Bot já fez {posts} posts hoje!")
                        
            else:
                print(f"\n⏰ {timestamp} - ❌ BOT OFFLINE")
                if isinstance(data, dict) and 'error' in data:
                    print(f"   💥 Erro: {data['error']}")
            
            print(f"   ⏳ Próxima verificação em {interval}s...")
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print(f"\n\n🛑 Monitoramento interrompido pelo usuário")
            break
        except Exception as e:
            print(f"\n💥 Erro no monitoramento: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Primeiro, busca URLs funcionando
    working_urls = monitor_bot()
    
    # Se encontrou URLs, oferece monitoramento contínuo
    if working_urls:
        status_urls = [url for url, _ in working_urls if "/status" in url]
        if status_urls:
            print(f"\n🔄 Deseja monitorar continuamente? (Enter para sim, Ctrl+C para sair)")
            try:
                input()
                continuous_monitor(status_urls[0])
            except KeyboardInterrupt:
                print("\n👋 Monitoramento finalizado!")
    else:
        print("\n❌ Não foi possível encontrar URLs funcionando para monitorar.")
        print("📋 Verifique a URL correta no Railway Dashboard e teste manualmente.")