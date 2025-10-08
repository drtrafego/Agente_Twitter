#!/usr/bin/env python3
"""
Teste específico para OAuth 2.0 (Client Credentials)
"""
import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def test_oauth2_client_credentials():
    """Testa OAuth 2.0 Client Credentials"""
    print("🔍 Testando OAuth 2.0 Client Credentials...")
    
    client_id = os.getenv('CLIENTE_ID')
    client_secret = os.getenv('CLIENTE_SECRET')
    
    if not client_id or not client_secret:
        print("❌ CLIENTE_ID ou CLIENTE_SECRET não encontrados!")
        return False
    
    print(f"✅ Client ID: {client_id[:10]}...")
    print(f"✅ Client Secret: {client_secret[:10]}...")
    
    try:
        # Tentar autenticação OAuth 2.0
        client = tweepy.Client(
            consumer_key=client_id,
            consumer_secret=client_secret
        )
        
        # Teste básico
        tweets = client.search_recent_tweets(query="hello", max_results=10)
        print(f"✅ OAuth 2.0 funcionando! Encontrados {len(tweets.data) if tweets.data else 0} tweets")
        return True
        
    except Exception as e:
        print(f"❌ Erro OAuth 2.0: {e}")
        return False

def test_oauth2_streaming():
    """Testa streaming com OAuth 2.0"""
    print("\n🔍 Testando Streaming com OAuth 2.0...")
    
    client_id = os.getenv('CLIENTE_ID')
    client_secret = os.getenv('CLIENTE_SECRET')
    
    try:
        # Tentar streaming com OAuth 2.0
        stream = tweepy.StreamingClient(
            consumer_key=client_id,
            consumer_secret=client_secret
        )
        
        rules = stream.get_rules()
        print("✅ Streaming OAuth 2.0 funcionando!")
        if rules.data:
            print(f"   Regras existentes: {len(rules.data)}")
        else:
            print("   Nenhuma regra configurada")
        return True
        
    except Exception as e:
        print(f"❌ Erro Streaming OAuth 2.0: {e}")
        if "403 Forbidden" in str(e):
            print("   💡 Ainda precisa de Projeto no Developer Portal")
        return False

def main():
    print("🚀 TESTANDO OAUTH 2.0 CREDENTIALS")
    print("=" * 40)
    
    oauth2_ok = test_oauth2_client_credentials()
    streaming_ok = test_oauth2_streaming()
    
    print("\n" + "=" * 40)
    print("📊 RESUMO OAuth 2.0:")
    print(f"   Client Credentials: {'✅' if oauth2_ok else '❌'}")
    print(f"   Streaming: {'✅' if streaming_ok else '❌'}")

if __name__ == "__main__":
    main()