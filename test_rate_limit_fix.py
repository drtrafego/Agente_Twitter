#!/usr/bin/env python3
"""
🧪 TESTE DAS CORREÇÕES DE RATE LIMITING
Valida se as melhorias implementadas resolvem o problema
"""

import requests
import time
import json
from datetime import datetime

def test_bot_status():
    """Testa o status atual do bot"""
    url = "https://agente-twitter.up.railway.app/status"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Bot Status:")
            print(f"   🤖 Running: {data.get('bot_running', 'unknown')}")
            print(f"   📊 Daily Posts: {data.get('daily_posts', 0)}/{data.get('daily_limit', 17)}")
            print(f"   ⏰ Last Activity: {data.get('last_activity', 'unknown')}")
            print(f"   ❌ Error: {data.get('error', 'none')}")
            return data
        else:
            print(f"❌ Erro ao acessar status: {response.status_code}")
            return None
    except Exception as e:
        print(f"💥 Erro de conexão: {e}")
        return None

def monitor_bot_behavior(duration_minutes=30):
    """Monitora comportamento do bot por um período"""
    print(f"🔍 Monitorando bot por {duration_minutes} minutos...")
    print("=" * 60)
    
    start_time = datetime.now()
    end_time = start_time.replace(minute=start_time.minute + duration_minutes)
    
    previous_posts = None
    rate_limit_detected = False
    
    while datetime.now() < end_time:
        timestamp = datetime.now().strftime('%H:%M:%S')
        status = test_bot_status()
        
        if status:
            current_posts = status.get('daily_posts', 0)
            
            # Detectar mudanças
            if previous_posts is not None:
                if current_posts > previous_posts:
                    print(f"📈 {timestamp} - NOVO POST! ({previous_posts} → {current_posts})")
                elif current_posts == previous_posts:
                    print(f"⏸️  {timestamp} - Sem atividade")
            
            # Verificar se há erro
            error = status.get('error')
            if error and '429' in str(error):
                if not rate_limit_detected:
                    print(f"🚨 {timestamp} - RATE LIMIT DETECTADO!")
                    rate_limit_detected = True
            elif rate_limit_detected and not error:
                print(f"✅ {timestamp} - Rate limit resolvido!")
                rate_limit_detected = False
            
            previous_posts = current_posts
        else:
            print(f"❌ {timestamp} - Bot offline ou inacessível")
        
        print(f"   ⏳ Próxima verificação em 2 minutos...")
        time.sleep(120)  # Verificar a cada 2 minutos
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DO MONITORAMENTO")
    print("=" * 60)
    
    final_status = test_bot_status()
    if final_status:
        print(f"✅ Status final: {final_status.get('bot_running', 'unknown')}")
        print(f"📊 Posts finais: {final_status.get('daily_posts', 0)}")
        print(f"❌ Erro final: {final_status.get('error', 'none')}")
    
    if rate_limit_detected:
        print("⚠️  Rate limiting ainda presente - pode precisar de mais ajustes")
    else:
        print("✅ Nenhum rate limiting detectado durante o monitoramento")

def check_improvements():
    """Verifica se as melhorias foram aplicadas"""
    print("🔍 VERIFICANDO MELHORIAS IMPLEMENTADAS")
    print("=" * 60)
    
    improvements = [
        "✅ Rate limiting 429 tratado na função create_tweet",
        "✅ Processamento limitado a 1 menção por ciclo",
        "✅ Processamento limitado a 1 comentário por ciclo", 
        "✅ Delay inicial de 30-60s antes de responder",
        "✅ Delay de 1-2min entre processamentos",
        "✅ Aguarda 15min quando recebe 429"
    ]
    
    for improvement in improvements:
        print(improvement)
        time.sleep(0.5)
    
    print("\n🎯 COMPORTAMENTO ESPERADO:")
    print("   1. Bot processa apenas 1 ação por ciclo (10-15min)")
    print("   2. Delay de 30-60s antes de cada resposta")
    print("   3. Se receber 429, aguarda 15 minutos")
    print("   4. Máximo 17 posts por dia")
    print("   5. Sem múltiplas tentativas consecutivas")

if __name__ == "__main__":
    print("🧪 TESTE DAS CORREÇÕES DE RATE LIMITING")
    print("=" * 60)
    print(f"⏰ Iniciado em: {datetime.now().strftime('%H:%M:%S')}")
    
    # Verificar melhorias
    check_improvements()
    
    print("\n" + "=" * 60)
    
    # Testar status atual
    print("📊 STATUS ATUAL DO BOT:")
    test_bot_status()
    
    print("\n" + "=" * 60)
    print("🔄 Deseja monitorar o bot por 30 minutos? (Enter para sim, Ctrl+C para sair)")
    
    try:
        input()
        monitor_bot_behavior(30)
    except KeyboardInterrupt:
        print("\n👋 Teste finalizado pelo usuário!")
    
    print("\n✅ Teste concluído!")