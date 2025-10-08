#!/usr/bin/env python3
"""
Bot Oficial X API v2 - Baseado na Documentação Oficial
Desenvolvido seguindo as melhores práticas da documentação oficial do X API v2
Otimizado para Free Tier: 17 posts/24h, 500 posts lidos/mês
"""

import os
import time
import logging
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import requests
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_oficial.log')
    ]
)
logger = logging.getLogger(__name__)

class XAPIBot:
    """
    Bot oficial para X API v2 seguindo documentação oficial
    Usa OAuth 2.0 Bearer Token conforme recomendado
    """
    
    def __init__(self):
        load_dotenv()
        
        # Credenciais OAuth 2.0 (recomendado pela documentação)
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.bot_username = os.getenv('BOT_USERNAME', 'drtrafeg0')
        
        # URLs da API v2 oficial
        self.base_url = "https://api.x.com/2"
        
        # Headers padrão conforme documentação
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "User-Agent": f"XAPIBot/1.0 (@{self.bot_username})"
        }
        
        # Rate limiting para Free Tier
        self.daily_post_limit = 17  # Limite oficial do Free Tier
        self.posts_today = 0
        self.last_reset = datetime.now().date()
        
        # Cache para evitar duplicatas
        self.processed_mentions = set()
        
        # Palavras-chave para resposta
        self.keywords = {
            'oi': 'Olá! Como posso ajudar você hoje? 😊',
            'hello': 'Hello! How can I help you today? 😊',
            'ajuda': 'Estou aqui para ajudar! O que você precisa? 🤝',
            'help': 'I\'m here to help! What do you need? 🤝',
            'bot': 'Sim, sou um bot inteligente! Como posso ser útil? 🤖',
            'como': 'Posso explicar sobre diversos tópicos. Seja mais específico! 💡',
            'what': 'I can help with various topics. Please be more specific! 💡'
        }
        
        logger.info(f"🚀 Bot X API v2 inicializado para @{self.bot_username}")
        logger.info(f"📊 Limite diário: {self.daily_post_limit} posts")
    
    def reset_daily_counter(self):
        """Reset contador diário se necessário"""
        today = datetime.now().date()
        if today > self.last_reset:
            self.posts_today = 0
            self.last_reset = today
            logger.info("🔄 Contador diário resetado")
    
    def can_post(self) -> bool:
        """Verifica se pode postar (respeitando limite do Free Tier)"""
        self.reset_daily_counter()
        return self.posts_today < self.daily_post_limit
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Faz requisição para API v2 com tratamento de erros
        Baseado na documentação oficial
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            else:
                logger.error(f"❌ Método HTTP não suportado: {method}")
                return None
            
            # Log da requisição
            logger.info(f"📡 {method} {endpoint} - Status: {response.status_code}")
            
            if response.status_code == 200 or response.status_code == 201:
                return response.json()
            elif response.status_code == 401:
                logger.error("❌ 401 Unauthorized - Verificar credenciais")
                return None
            elif response.status_code == 429:
                logger.warning("⚠️ Rate limit atingido - Aguardando...")
                time.sleep(900)  # 15 minutos
                return None
            else:
                logger.error(f"❌ Erro na API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na requisição: {str(e)}")
            return None
    
    def get_user_info(self) -> Optional[Dict]:
        """
        Obtém informações do usuário autenticado
        Endpoint: GET /2/users/me
        """
        return self.make_request('GET', 'users/me')
    
    def create_tweet(self, text: str, reply_to: Optional[str] = None) -> Optional[Dict]:
        """
        Cria um tweet usando API v2
        Endpoint: POST /2/tweets
        """
        if not self.can_post():
            logger.warning(f"⚠️ Limite diário atingido ({self.posts_today}/{self.daily_post_limit})")
            return None
        
        data = {"text": text}
        if reply_to:
            data["reply"] = {"in_reply_to_tweet_id": reply_to}
        
        result = self.make_request('POST', 'tweets', data)
        if result:
            self.posts_today += 1
            logger.info(f"✅ Tweet criado! Posts hoje: {self.posts_today}/{self.daily_post_limit}")
        
        return result
    
    def search_mentions(self, max_results: int = 10) -> Optional[List[Dict]]:
        """
        Busca menções usando API v2
        Endpoint: GET /2/tweets/search/recent
        """
        query = f"@{self.bot_username} -is:retweet"
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "id,text,author_id,created_at,in_reply_to_user_id",
            "expansions": "author_id",
            "user.fields": "username"
        }
        
        result = self.make_request('GET', 'tweets/search/recent', params)
        if result and 'data' in result:
            return result['data']
        return []
    
    def generate_response(self, mention_text: str, author_username: str) -> str:
        """
        Gera resposta personalizada baseada no texto da menção
        """
        mention_lower = mention_text.lower()
        
        # Busca por palavras-chave
        for keyword, response in self.keywords.items():
            if keyword in mention_lower:
                return f"@{author_username} {response}"
        
        # Resposta padrão personalizada
        responses = [
            f"@{author_username} Obrigado por me mencionar! Como posso ajudar? 😊",
            f"@{author_username} Oi! Estou aqui e pronto para conversar! 👋",
            f"@{author_username} Olá! Que bom te ver por aqui! Como vai? 🌟",
            f"@{author_username} Hey! Obrigado pela menção! Em que posso ser útil? 🤝"
        ]
        
        import random
        return random.choice(responses)
    
    def process_mentions(self):
        """
        Processa menções e responde automaticamente
        """
        logger.info("🔍 Buscando novas menções...")
        
        mentions = self.search_mentions()
        if not mentions:
            logger.info("📭 Nenhuma menção encontrada")
            return
        
        new_mentions = 0
        for mention in mentions:
            mention_id = mention['id']
            
            # Evita processar a mesma menção duas vezes
            if mention_id in self.processed_mentions:
                continue
            
            # Evita responder a si mesmo
            if mention.get('author_id') == self.get_user_info().get('data', {}).get('id'):
                continue
            
            # Processa a menção
            mention_text = mention['text']
            author_username = "user"  # Fallback se não conseguir obter username
            
            logger.info(f"📨 Nova menção de @{author_username}: {mention_text[:50]}...")
            
            # Gera e envia resposta
            response_text = self.generate_response(mention_text, author_username)
            
            if self.create_tweet(response_text, mention_id):
                logger.info(f"✅ Respondido para @{author_username}")
                new_mentions += 1
            else:
                logger.warning(f"⚠️ Falha ao responder para @{author_username}")
            
            # Adiciona ao cache
            self.processed_mentions.add(mention_id)
            
            # Pausa entre respostas para evitar spam
            time.sleep(5)
        
        if new_mentions > 0:
            logger.info(f"🎉 Processadas {new_mentions} novas menções")
    
    def run(self):
        """
        Loop principal do bot
        """
        logger.info("🚀 Iniciando bot X API v2...")
        
        # Verifica autenticação
        user_info = self.get_user_info()
        if not user_info:
            logger.error("❌ Falha na autenticação - Verificar BEARER_TOKEN")
            return
        
        username = user_info.get('data', {}).get('username', 'unknown')
        logger.info(f"✅ Autenticado como @{username}")
        
        # Loop principal
        while True:
            try:
                self.process_mentions()
                
                # Heartbeat
                logger.info(f"💓 Bot ativo - Posts hoje: {self.posts_today}/{self.daily_post_limit}")
                
                # Aguarda 5 minutos antes da próxima verificação
                time.sleep(300)
                
            except KeyboardInterrupt:
                logger.info("🛑 Bot interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop principal: {str(e)}")
                time.sleep(60)  # Aguarda 1 minuto antes de tentar novamente

def main():
    """Função principal"""
    bot = XAPIBot()
    bot.run()

if __name__ == "__main__":
    main()