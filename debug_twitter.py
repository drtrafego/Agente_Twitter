#!/usr/bin/env python3
"""
Script de debug para testar credenciais do Twitter API
"""
import os
import tweepy
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

def test_bearer_token():
    """Testa autenticação com Bearer Token"""
    print("🔍 Testando Bearer Token...")
    bearer_token = os.getenv('BEARER_TOKEN')
    
    if not bearer_token:
        print("❌ BEARER_TOKEN não encontrado!")
        return False
    
    print(f"✅ BEARER_TOKEN encontrado: {bearer_token[:20]}...")
    
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        # Teste simples: buscar um tweet público
        tweets = client.search_recent_tweets(query="hello", max_results=10)
        print(f"✅ Bearer Token válido! Encontrados {len(tweets.data) if tweets.data else 0} tweets")
        return True
    except Exception as e:
        print(f"❌ Erro com Bearer Token: {e}")
        if "Consumer key must be string" in str(e):
            print("   💡 Dica: Este erro indica problema na configuração do tweepy")
        return False

def test_oauth_credentials():
    """Testa autenticação OAuth 1.0a"""
    print("\n🔍 Testando OAuth 1.0a...")
    
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_KEY_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_secret = os.getenv('ACCESS_TOKEN_SECRET')
    
    missing = []
    if not api_key: missing.append('API_KEY')
    if not api_secret: missing.append('API_KEY_SECRET')
    if not access_token: missing.append('ACCESS_TOKEN')
    if not access_secret: missing.append('ACCESS_TOKEN_SECRET')
    
    if missing:
        print(f"❌ Credenciais OAuth faltando: {', '.join(missing)}")
        return False
    
    print("✅ Todas as credenciais OAuth encontradas")
    print(f"   API_KEY: {api_key[:10]}...")
    print(f"   API_KEY_SECRET: {api_secret[:10]}...")
    print(f"   ACCESS_TOKEN: {access_token[:20]}...")
    print(f"   ACCESS_TOKEN_SECRET: {access_secret[:10]}...")
    
    try:
        auth = tweepy.OAuth1UserHandler(
            api_key, api_secret,
            access_token, access_secret
        )
        api = tweepy.API(auth)
        
        # Teste: verificar credenciais
        user = api.verify_credentials()
        print(f"✅ OAuth válido! Usuário: @{user.screen_name}")
        return True
    except Exception as e:
        print(f"❌ Erro com OAuth: {e}")
        return False

def test_streaming():
    """Testa se consegue acessar streaming API"""
    print("\n🔍 Testando Streaming API...")
    
    bearer_token = os.getenv('BEARER_TOKEN')
    if not bearer_token:
        print("❌ BEARER_TOKEN necessário para streaming")
        return False
    
    # Verificar se o Bearer Token não é um placeholder
    if bearer_token.startswith('AAAAAAAAAA') and 'XXXXXXX' in bearer_token:
        print("❌ BEARER_TOKEN ainda é um placeholder! Substitua pelo token real.")
        return False
    
    try:
        # Usar StreamingClient para testar streaming
        stream = tweepy.StreamingClient(bearer_token=bearer_token)
        # Tentar obter regras atuais (isso que está falhando no bot)
        rules = stream.get_rules()
        print("✅ Streaming API acessível!")
        if rules.data:
            print(f"   Regras existentes: {len(rules.data)}")
        else:
            print("   Nenhuma regra configurada")
        return True
    except Exception as e:
        print(f"❌ Erro no Streaming API: {e}")
        if "Consumer key must be string" in str(e):
            print("   💡 Dica: Verifique se o BEARER_TOKEN está correto no arquivo .env")
        elif "403 Forbidden" in str(e):
            print("   💡 Dica: Erro 403 - credenciais não associadas a um Projeto no Twitter Developer Portal")
        return False

def main():
    print("🚀 INICIANDO DEBUG DAS CREDENCIAIS TWITTER")
    print("=" * 50)
    
    # Verificar arquivo .env
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        return
    
    print("✅ Arquivo .env encontrado")
    
    # Testar cada tipo de autenticação
    bearer_ok = test_bearer_token()
    oauth_ok = test_oauth_credentials()
    streaming_ok = test_streaming()
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    print(f"   Bearer Token: {'✅' if bearer_ok else '❌'}")
    print(f"   OAuth 1.0a: {'✅' if oauth_ok else '❌'}")
    print(f"   Streaming API: {'✅' if streaming_ok else '❌'}")
    
    if all([bearer_ok, oauth_ok, streaming_ok]):
        print("\n🎉 TODAS AS CREDENCIAIS ESTÃO FUNCIONANDO!")
    else:
        print("\n⚠️  PROBLEMAS DETECTADOS - verifique as credenciais")

if __name__ == "__main__":
    main()