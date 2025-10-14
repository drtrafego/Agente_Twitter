#!/usr/bin/env python3
"""
🔍 VERIFICAR ATIVIDADE DO BOT NO TWITTER
Verifica se o bot @drtrafeg0 está ativo e funcionando
"""

import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class TwitterChecker:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.api_key_secret = os.getenv('API_KEY_SECRET')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        self.base_url = "https://api.x.com/2"
        
    def generate_oauth_header(self, method, url, params=None):
        """Gera header OAuth 1.0a"""
        import urllib.parse
        import hmac
        import hashlib
        import base64
        import secrets
        import string
        
        # Parâmetros OAuth
        oauth_params = {
            'oauth_consumer_key': self.api_key,
            'oauth_token': self.access_token,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(datetime.now().timestamp())),
            'oauth_nonce': ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)),
            'oauth_version': '1.0'
        }
        
        # Combina parâmetros
        all_params = {**oauth_params}
        if params:
            all_params.update(params)
        
        # Ordena parâmetros
        sorted_params = sorted(all_params.items())
        param_string = '&'.join([f"{k}={urllib.parse.quote(str(v), safe='')}" 
                                for k, v in sorted_params])
        
        # Base string
        base_string = f"{method}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_string, safe='')}"
        
        # Signing key
        signing_key = f"{urllib.parse.quote(self.api_key_secret, safe='')}&{urllib.parse.quote(self.access_token_secret, safe='')}"
        
        # Signature
        signature = base64.b64encode(
            hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
        ).decode()
        
        oauth_params['oauth_signature'] = signature
        
        # Header
        auth_header = 'OAuth ' + ', '.join([f'{k}="{urllib.parse.quote(str(v), safe="")}"' 
                                           for k, v in oauth_params.items()])
        return auth_header

    def get_my_info(self):
        """Obtém informações do usuário autenticado"""
        url = f"{self.base_url}/users/me"
        headers = {
            'Authorization': self.generate_oauth_header('GET', url),
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"Erro {response.status_code}: {response.text}"
        except Exception as e:
            return False, f"Erro de conexão: {e}"

    def get_recent_tweets(self, user_id, max_results=10):
        """Obtém tweets recentes do usuário"""
        url = f"{self.base_url}/users/{user_id}/tweets"
        params = {
            'max_results': max_results,
            'tweet.fields': 'created_at,public_metrics,in_reply_to_user_id'
        }
        
        headers = {
            'Authorization': self.generate_oauth_header('GET', url, params),
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"Erro {response.status_code}: {response.text}"
        except Exception as e:
            return False, f"Erro de conexão: {e}"

def check_bot_activity():
    """Verifica a atividade do bot"""
    print("🔍 VERIFICAÇÃO DE ATIVIDADE DO BOT")
    print("=" * 50)
    print(f"⏰ Verificação em: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    checker = TwitterChecker()
    
    # 1. Verifica autenticação
    print("🔐 Verificando autenticação...")
    success, result = checker.get_my_info()
    
    if not success:
        print(f"   ❌ Erro na autenticação: {result}")
        return
    
    user_data = result.get('data', {})
    username = user_data.get('username', 'N/A')
    user_id = user_data.get('id', 'N/A')
    
    print(f"   ✅ Autenticado como: @{username}")
    print(f"   📋 User ID: {user_id}")
    print()
    
    # 2. Verifica tweets recentes
    print("📝 Verificando tweets recentes...")
    success, result = checker.get_recent_tweets(user_id, 20)
    
    if not success:
        print(f"   ❌ Erro ao buscar tweets: {result}")
        return
    
    tweets = result.get('data', [])
    print(f"   📊 Tweets encontrados: {len(tweets)}")
    
    if not tweets:
        print("   ⚠️  Nenhum tweet encontrado")
        return
    
    # 3. Analisa atividade recente
    print("\n📈 ANÁLISE DE ATIVIDADE:")
    
    now = datetime.now()
    recent_tweets = []
    replies = []
    
    for tweet in tweets:
        created_at = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
        age_hours = (now - created_at.replace(tzinfo=None)).total_seconds() / 3600
        
        tweet_info = {
            'id': tweet['id'],
            'text': tweet['text'][:100] + '...' if len(tweet['text']) > 100 else tweet['text'],
            'created_at': created_at.strftime('%H:%M:%S'),
            'age_hours': age_hours,
            'is_reply': tweet.get('in_reply_to_user_id') is not None
        }
        
        if age_hours <= 24:  # Últimas 24 horas
            recent_tweets.append(tweet_info)
            
        if tweet_info['is_reply']:
            replies.append(tweet_info)
    
    print(f"   🕐 Tweets nas últimas 24h: {len(recent_tweets)}")
    print(f"   💬 Respostas (menções): {len(replies)}")
    
    # 4. Mostra atividade recente
    if recent_tweets:
        print(f"\n📋 ATIVIDADE RECENTE (últimas 24h):")
        for tweet in recent_tweets[:5]:  # Mostra os 5 mais recentes
            status = "💬 RESPOSTA" if tweet['is_reply'] else "📝 TWEET"
            print(f"   {status} | {tweet['created_at']} | {tweet['text']}")
    
    # 5. Status do bot
    print(f"\n🤖 STATUS DO BOT:")
    
    if recent_tweets:
        last_activity = min(tweet['age_hours'] for tweet in recent_tweets)
        if last_activity < 1:
            print("   🟢 ATIVO - Atividade na última hora")
        elif last_activity < 6:
            print("   🟡 MODERADO - Atividade nas últimas 6 horas")
        elif last_activity < 24:
            print("   🟠 BAIXO - Atividade nas últimas 24 horas")
        else:
            print("   🔴 INATIVO - Sem atividade recente")
            
        print(f"   ⏰ Última atividade: {last_activity:.1f}h atrás")
        
        if replies:
            print(f"   💬 Respondendo menções: SIM ({len(replies)} respostas)")
        else:
            print("   💬 Respondendo menções: NÃO")
    else:
        print("   🔴 SEM ATIVIDADE DETECTADA")
    
    print(f"\n{'='*50}")
    print("✅ VERIFICAÇÃO CONCLUÍDA")

if __name__ == "__main__":
    check_bot_activity()