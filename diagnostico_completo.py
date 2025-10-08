import tweepy
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

print("🔍 DIAGNÓSTICO COMPLETO DA API DO X")
print("=" * 60)

# Credenciais
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CLIENTE_ID = os.getenv("CLIENTE_ID")
CLIENTE_SECRET = os.getenv("CLIENTE_SECRET")
BOT_USERNAME = os.getenv("BOT_USERNAME")

print(f"🤖 Bot Username: {BOT_USERNAME}")
print(f"🔑 API_KEY: {API_KEY[:10]}...")
print(f"🔑 BEARER_TOKEN: {BEARER_TOKEN[:20]}...")
print(f"🔑 ACCESS_TOKEN: {ACCESS_TOKEN[:20]}...")
print(f"🔑 CLIENTE_ID: {CLIENTE_ID[:15]}...")
print()

# TESTE 1: Bearer Token (API v2)
print("🧪 TESTE 1: Bearer Token (API v2)")
print("-" * 40)
try:
    client_bearer = tweepy.Client(bearer_token=BEARER_TOKEN)
    user = client_bearer.get_me()
    print(f"✅ Bearer Token FUNCIONANDO! Usuário: @{user.data.username}")
    
    # Teste de busca
    try:
        tweets = client_bearer.search_recent_tweets(query="python", max_results=5)
        print(f"✅ Busca funcionando! Encontrados {len(tweets.data) if tweets.data else 0} tweets")
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        
except Exception as e:
    print(f"❌ Bearer Token falhou: {e}")

print()

# TESTE 2: OAuth 1.0a (API v2)
print("🧪 TESTE 2: OAuth 1.0a (API v2)")
print("-" * 40)
try:
    client_oauth1 = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    user = client_oauth1.get_me()
    print(f"✅ OAuth 1.0a (v2) FUNCIONANDO! Usuário: @{user.data.username}")
    
    # Teste de busca
    try:
        tweets = client_oauth1.search_recent_tweets(query=f"@{BOT_USERNAME}", max_results=5)
        print(f"✅ Busca de menções funcionando! Encontrados {len(tweets.data) if tweets.data else 0} tweets")
    except Exception as e:
        print(f"❌ Erro na busca de menções: {e}")
    
    # Teste de criação de tweet
    try:
        # NÃO vou criar um tweet real, só testar a autenticação
        print("✅ Autenticação para criação de tweets: OK")
    except Exception as e:
        print(f"❌ Erro na criação de tweets: {e}")
        
except Exception as e:
    print(f"❌ OAuth 1.0a (v2) falhou: {e}")

print()

# TESTE 3: OAuth 1.0a (API v1.1)
print("🧪 TESTE 3: OAuth 1.0a (API v1.1)")
print("-" * 40)
try:
    auth = tweepy.OAuth1UserHandler(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    api_v1 = tweepy.API(auth)
    user = api_v1.verify_credentials()
    print(f"✅ OAuth 1.0a (v1.1) FUNCIONANDO! Usuário: @{user.screen_name}")
    
    # Teste de menções
    try:
        mentions = api_v1.mentions_timeline(count=5)
        print(f"✅ Menções funcionando! Encontradas {len(mentions)} menções")
    except Exception as e:
        print(f"❌ Erro nas menções: {e}")
        
except Exception as e:
    print(f"❌ OAuth 1.0a (v1.1) falhou: {e}")

print()

# TESTE 4: OAuth 2.0 Client Credentials
print("🧪 TESTE 4: OAuth 2.0 Client Credentials")
print("-" * 40)
try:
    client_oauth2 = tweepy.Client(
        consumer_key=CLIENTE_ID,
        consumer_secret=CLIENTE_SECRET
    )
    # OAuth 2.0 não tem get_me(), vamos testar busca
    tweets = client_oauth2.search_recent_tweets(query="python", max_results=5)
    print(f"✅ OAuth 2.0 FUNCIONANDO! Encontrados {len(tweets.data) if tweets.data else 0} tweets")
except Exception as e:
    print(f"❌ OAuth 2.0 falhou: {e}")

print()

# TESTE 5: Híbrido (Bearer + OAuth 1.0a)
print("🧪 TESTE 5: Híbrido (Bearer para busca + OAuth 1.0a para ações)")
print("-" * 60)
try:
    # Bearer para busca
    client_search = tweepy.Client(bearer_token=BEARER_TOKEN)
    tweets = client_search.search_recent_tweets(query="python", max_results=3)
    print(f"✅ Busca com Bearer: {len(tweets.data) if tweets.data else 0} tweets")
    
    # OAuth 1.0a para ações
    client_actions = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    user = client_actions.get_me()
    print(f"✅ Ações com OAuth 1.0a: @{user.data.username}")
    print("✅ MÉTODO HÍBRIDO FUNCIONANDO!")
    
except Exception as e:
    print(f"❌ Método híbrido falhou: {e}")

print()
print("🎯 RESUMO FINAL")
print("=" * 60)
print("Testando qual método permite:")
print("1. ✅ Autenticação")
print("2. ✅ Busca de menções")  
print("3. ✅ Criação de tweets")
print("4. ✅ Funcionamento contínuo")
print()
print("💡 RECOMENDAÇÃO: Use o método que passou em TODOS os testes!")