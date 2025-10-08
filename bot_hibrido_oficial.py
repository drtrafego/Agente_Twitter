#!/usr/bin/env python3
"""
Bot Híbrido X API v2 - Solução Definitiva
Baseado na documentação oficial do X API v2
Usa OAuth 1.0a para User Context e Bearer Token para App-Only quando apropriado
Otimizado para Free Tier: 17 posts/24h, 500 posts lidos/mês
"""

import os
import time
import logging
import json
import hashlib
import hmac
import base64
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import requests
from dotenv import load_dotenv

# Configuração de logging sem emojis para compatibilidade
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_hibrido.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class XAPIHybridBot:
    """
    Bot híbrido para X API v2 seguindo documentação oficial
    Usa OAuth 1.0a para User Context e Bearer Token para App-Only
    """
    
    def __init__(self):
        load_dotenv()
        
        # Credenciais OAuth 1.0a (para User Context)
        self.api_key = os.getenv('API_KEY')
        self.api_key_secret = os.getenv('API_KEY_SECRET')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        
        # Bearer Token (para App-Only quando possível)
        self.bearer_token = os.getenv('BEARER_TOKEN')
        
        self.bot_username = os.getenv('BOT_USERNAME', 'drtrafeg0')
        
        # URLs da API v2 oficial
        self.base_url = "https://api.x.com/2"
        
        # Rate limiting para Free Tier
        self.daily_post_limit = 17  # Limite oficial do Free Tier
        self.posts_today = 0
        self.last_reset = datetime.now().date()
        
        # Cache para evitar duplicatas
        self.processed_mentions = set()
        
        # Palavras-chave para resposta
        self.keywords = {
            'oi': 'Ola! Como posso ajudar voce hoje?',
            'hello': 'Hello! How can I help you today?',
            'ajuda': 'Estou aqui para ajudar! O que voce precisa?',
            'help': 'I am here to help! What do you need?',
            'bot': 'Sim, sou um bot inteligente! Como posso ser util?',
            'como': 'Posso explicar sobre diversos topicos. Seja mais especifico!',
            'what': 'I can help with various topics. Please be more specific!'
        }
        
        logger.info(f"Bot X API v2 inicializado para @{self.bot_username}")
        logger.info(f"Limite diario: {self.daily_post_limit} posts")
    
    def reset_daily_counter(self):
        """Reset contador diário se necessário"""
        today = datetime.now().date()
        if today > self.last_reset:
            self.posts_today = 0
            self.last_reset = today
            logger.info("Contador diario resetado")
    
    def can_post(self) -> bool:
        """Verifica se pode postar (respeitando limite do Free Tier)"""
        self.reset_daily_counter()
        return self.posts_today < self.daily_post_limit
    
    def generate_oauth1_signature(self, method: str, url: str, params: Dict) -> str:
        """
        Gera assinatura OAuth 1.0a conforme especificação oficial
        """
        # Parâmetros OAuth 1.0a
        oauth_params = {
            'oauth_consumer_key': self.api_key,
            'oauth_token': self.access_token,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': str(int(time.time() * 1000)),
            'oauth_version': '1.0'
        }
        
        # Combina parâmetros OAuth com parâmetros da requisição
        all_params = {**oauth_params, **params}
        
        # Ordena parâmetros
        sorted_params = sorted(all_params.items())
        
        # Cria string de parâmetros
        param_string = '&'.join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted_params])
        
        # Cria string base para assinatura
        base_string = f"{method.upper()}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_string, safe='')}"
        
        # Cria chave de assinatura
        signing_key = f"{urllib.parse.quote(self.api_key_secret, safe='')}&{urllib.parse.quote(self.access_token_secret, safe='')}"
        
        # Gera assinatura HMAC-SHA1
        signature = base64.b64encode(
            hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
        ).decode()
        
        oauth_params['oauth_signature'] = signature
        
        return oauth_params
    
    def make_oauth1_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Faz requisição OAuth 1.0a para endpoints que exigem User Context
        """
        url = f"{self.base_url}/{endpoint}"
        params = data if method.upper() == 'GET' and data else {}
        
        # Gera assinatura OAuth 1.0a
        oauth_params = self.generate_oauth1_signature(method, url, params)
        
        # Cria header Authorization
        auth_header = 'OAuth ' + ', '.join([f'{k}="{urllib.parse.quote(str(v), safe="")}"' for k, v in oauth_params.items()])
        
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json',
            'User-Agent': f'XAPIBot/1.0 (@{self.bot_username})'
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                logger.error(f"Metodo HTTP nao suportado: {method}")
                return None
            
            logger.info(f"{method} {endpoint} - Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 401:
                logger.error("401 Unauthorized - Verificar credenciais OAuth 1.0a")
                return None
            elif response.status_code == 429:
                logger.warning("Rate limit atingido - Aguardando...")
                time.sleep(900)  # 15 minutos
                return None
            else:
                logger.error(f"Erro na API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na requisicao OAuth 1.0a: {str(e)}")
            return None
    
    def make_bearer_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Faz requisição com Bearer Token para endpoints App-Only
        """
        url = f"{self.base_url}/{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "User-Agent": f"XAPIBot/1.0 (@{self.bot_username})"
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                logger.error(f"Metodo HTTP nao suportado: {method}")
                return None
            
            logger.info(f"{method} {endpoint} - Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 401:
                logger.error("401 Unauthorized - Verificar Bearer Token")
                return None
            elif response.status_code == 429:
                logger.warning("Rate limit atingido - Aguardando...")
                time.sleep(900)  # 15 minutos
                return None
            else:
                logger.error(f"Erro na API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na requisicao Bearer: {str(e)}")
            return None
    
    def get_user_info(self) -> Optional[Dict]:
        """
        Obtém informações do usuário autenticado
        Usa OAuth 1.0a (User Context obrigatório)
        """
        return self.make_oauth1_request('GET', 'users/me')
    
    def create_tweet(self, text: str, reply_to: Optional[str] = None) -> Optional[Dict]:
        """
        Cria um tweet usando OAuth 1.0a (User Context obrigatório)
        """
        if not self.can_post():
            logger.warning(f"Limite diario atingido ({self.posts_today}/{self.daily_post_limit})")
            return None
        
        data = {"text": text}
        if reply_to:
            data["reply"] = {"in_reply_to_tweet_id": reply_to}
        
        result = self.make_oauth1_request('POST', 'tweets', data)
        if result:
            self.posts_today += 1
            logger.info(f"Tweet criado! Posts hoje: {self.posts_today}/{self.daily_post_limit}")
        
        return result
    
    def search_mentions(self, max_results: int = 10) -> Optional[List[Dict]]:
        """
        Busca menções usando Bearer Token (App-Only permitido)
        """
        query = f"@{self.bot_username} -is:retweet"
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "id,text,author_id,created_at,in_reply_to_user_id",
            "expansions": "author_id",
            "user.fields": "username"
        }
        
        result = self.make_bearer_request('GET', 'tweets/search/recent', params)
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
            f"@{author_username} Obrigado por me mencionar! Como posso ajudar?",
            f"@{author_username} Oi! Estou aqui e pronto para conversar!",
            f"@{author_username} Ola! Que bom te ver por aqui! Como vai?",
            f"@{author_username} Hey! Obrigado pela mencao! Em que posso ser util?"
        ]
        
        import random
        return random.choice(responses)
    
    def process_mentions(self):
        """
        Processa menções e responde automaticamente
        """
        logger.info("Buscando novas mencoes...")
        
        mentions = self.search_mentions()
        if not mentions:
            logger.info("Nenhuma mencao encontrada")
            return
        
        new_mentions = 0
        for mention in mentions:
            mention_id = mention['id']
            
            # Evita processar a mesma menção duas vezes
            if mention_id in self.processed_mentions:
                continue
            
            # Processa a menção
            mention_text = mention['text']
            author_username = "user"  # Fallback
            
            logger.info(f"Nova mencao: {mention_text[:50]}...")
            
            # Gera e envia resposta
            response_text = self.generate_response(mention_text, author_username)
            
            if self.create_tweet(response_text, mention_id):
                logger.info(f"Respondido para @{author_username}")
                new_mentions += 1
            else:
                logger.warning(f"Falha ao responder para @{author_username}")
            
            # Adiciona ao cache
            self.processed_mentions.add(mention_id)
            
            # Pausa entre respostas para evitar spam
            time.sleep(5)
        
        if new_mentions > 0:
            logger.info(f"Processadas {new_mentions} novas mencoes")
    
    def run(self):
        """
        Loop principal do bot
        """
        logger.info("Iniciando bot X API v2 hibrido...")
        
        # Verifica autenticação OAuth 1.0a
        user_info = self.get_user_info()
        if not user_info:
            logger.error("Falha na autenticacao OAuth 1.0a")
            return
        
        username = user_info.get('data', {}).get('username', 'unknown')
        logger.info(f"Autenticado como @{username}")
        
        # Loop principal
        while True:
            try:
                self.process_mentions()
                
                # Heartbeat
                logger.info(f"Bot ativo - Posts hoje: {self.posts_today}/{self.daily_post_limit}")
                
                # Aguarda 5 minutos antes da próxima verificação
                time.sleep(300)
                
            except KeyboardInterrupt:
                logger.info("Bot interrompido pelo usuario")
                break
            except Exception as e:
                logger.error(f"Erro no loop principal: {str(e)}")
                time.sleep(60)  # Aguarda 1 minuto antes de tentar novamente

def main():
    """Função principal"""
    bot = XAPIHybridBot()
    bot.run()

if __name__ == "__main__":
    main()