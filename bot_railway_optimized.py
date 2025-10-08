#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot X API v2 Otimizado para Railway
Versão com healthcheck endpoint e timeout handling
"""

import os
import time
import json
import logging
import requests
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask, jsonify
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging sem emojis para compatibilidade
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_railway.log', encoding='utf-8')
    ]
)

class XAPIBot:
    def __init__(self):
        # Credenciais
        self.api_key = os.getenv('API_KEY')
        self.api_key_secret = os.getenv('API_KEY_SECRET')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.bot_username = os.getenv('BOT_USERNAME', 'drtrafeg0')
        
        # Verificar se todas as credenciais estão presentes
        if not all([self.api_key, self.api_key_secret, self.access_token, 
                   self.access_token_secret, self.bearer_token]):
            raise ValueError("Credenciais incompletas! Verifique as variáveis de ambiente.")
        
        # Configurações
        self.base_url = "https://api.x.com/2"
        self.daily_limit = 17  # Free Tier limit
        self.daily_posts = 0
        self.last_reset = datetime.now().date()
        
        # Cache para evitar duplicatas
        self.processed_mentions = set()
        
        # Status do bot
        self.is_running = True
        self.last_activity = datetime.now()
        
        logging.info(f"Bot X API v2 inicializado para @{self.bot_username}")
        logging.info(f"Limite diario: {self.daily_limit} posts")

    def get_oauth1_headers(self, method, url, params=None):
        """Gerar headers OAuth 1.0a para User Context"""
        import hmac
        import hashlib
        import base64
        import urllib.parse
        from secrets import token_urlsafe
        
        # Parâmetros OAuth
        oauth_params = {
            'oauth_consumer_key': self.api_key,
            'oauth_token': self.access_token,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': token_urlsafe(32),
            'oauth_version': '1.0'
        }
        
        # Combinar parâmetros
        all_params = {**oauth_params}
        if params:
            all_params.update(params)
        
        # Criar string de parâmetros
        param_string = '&'.join([f"{k}={urllib.parse.quote(str(v), safe='')}" 
                                for k, v in sorted(all_params.items())])
        
        # Criar base string
        base_string = f"{method}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_string, safe='')}"
        
        # Criar chave de assinatura
        signing_key = f"{urllib.parse.quote(self.api_key_secret, safe='')}&{urllib.parse.quote(self.access_token_secret, safe='')}"
        
        # Gerar assinatura
        signature = base64.b64encode(
            hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
        ).decode()
        
        oauth_params['oauth_signature'] = signature
        
        # Criar header Authorization
        auth_header = 'OAuth ' + ', '.join([f'{k}="{urllib.parse.quote(str(v), safe="")}"' 
                                           for k, v in sorted(oauth_params.items())])
        
        return {'Authorization': auth_header, 'Content-Type': 'application/json'}

    def authenticate(self):
        """Verificar autenticação"""
        try:
            url = f"{self.base_url}/users/me"
            headers = self.get_oauth1_headers('GET', url)
            
            response = requests.get(url, headers=headers, timeout=30)
            logging.info(f"GET users/me - Status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get('data', {}).get('username', 'unknown')
                logging.info(f"Autenticado como @{username}")
                return True
            else:
                logging.error(f"Erro de autenticacao: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Erro na autenticacao: {e}")
            return False

    def search_mentions(self):
        """Buscar menções usando Bearer Token"""
        try:
            # Reset contador diário se necessário
            if datetime.now().date() > self.last_reset:
                self.daily_posts = 0
                self.last_reset = datetime.now().date()
                logging.info("Contador diario resetado")
            
            # Verificar limite diário
            if self.daily_posts >= self.daily_limit:
                logging.warning(f"Limite diario atingido: {self.daily_posts}/{self.daily_limit}")
                return []
            
            # Buscar menções
            query = f"@{self.bot_username} -is:retweet"
            url = f"{self.base_url}/tweets/search/recent"
            headers = {
                'Authorization': f'Bearer {self.bearer_token}',
                'Content-Type': 'application/json'
            }
            params = {
                'query': query,
                'max_results': 10,
                'tweet.fields': 'author_id,created_at,text'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            logging.info(f"GET tweets/search/recent - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                mentions = data.get('data', [])
                new_mentions = [m for m in mentions if m['id'] not in self.processed_mentions]
                
                logging.info(f"Encontradas {len(new_mentions)} novas mencoes")
                return new_mentions
                
            elif response.status_code == 429:
                logging.warning("Rate limit atingido - Aguardando...")
                time.sleep(900)  # 15 minutos
                return []
            else:
                logging.error(f"Erro ao buscar mencoes: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logging.error(f"Erro na busca de mencoes: {e}")
            return []

    def generate_response(self, mention_text):
        """Gerar resposta baseada no texto da menção"""
        text = mention_text.lower()
        
        if any(word in text for word in ['oi', 'hello', 'ola']):
            return "Oi! Como posso ajudar voce hoje?"
        elif any(word in text for word in ['ajuda', 'help']):
            return "Estou aqui para ajudar! Me mencione com suas duvidas."
        elif 'bot' in text:
            return "Sim, sou um bot automatizado! Como posso ser util?"
        elif any(word in text for word in ['obrigado', 'thanks', 'valeu']):
            return "De nada! Fico feliz em ajudar!"
        else:
            return "Obrigado por me mencionar! Como posso ajudar?"

    def create_tweet(self, text):
        """Criar tweet usando OAuth 1.0a"""
        try:
            if self.daily_posts >= self.daily_limit:
                logging.warning(f"Limite diario atingido: {self.daily_posts}/{self.daily_limit}")
                return False
            
            url = f"{self.base_url}/tweets"
            headers = self.get_oauth1_headers('POST', url)
            data = json.dumps({'text': text})
            
            response = requests.post(url, headers=headers, data=data, timeout=30)
            logging.info(f"POST tweets - Status: {response.status_code}")
            
            if response.status_code == 201:
                self.daily_posts += 1
                logging.info(f"Tweet criado! Posts hoje: {self.daily_posts}/{self.daily_limit}")
                return True
            else:
                logging.error(f"Erro ao criar tweet: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Erro na criacao de tweet: {e}")
            return False

    def process_mentions(self):
        """Processar menções e responder"""
        try:
            mentions = self.search_mentions()
            
            for mention in mentions:
                if mention['id'] in self.processed_mentions:
                    continue
                
                # Marcar como processada
                self.processed_mentions.add(mention['id'])
                
                # Gerar resposta
                response_text = self.generate_response(mention['text'])
                
                # Criar tweet de resposta
                if self.create_tweet(response_text):
                    logging.info(f"Respondeu a mencao: {mention['id']}")
                    self.last_activity = datetime.now()
                    time.sleep(2)  # Evitar rate limit
                else:
                    break  # Parar se não conseguir criar tweet
                    
        except Exception as e:
            logging.error(f"Erro ao processar mencoes: {e}")

    def run_bot_loop(self):
        """Loop principal do bot"""
        logging.info("Iniciando loop do bot...")
        
        while self.is_running:
            try:
                # Processar menções
                self.process_mentions()
                
                # Heartbeat
                logging.info(f"Bot ativo - Posts hoje: {self.daily_posts}/{self.daily_limit}")
                self.last_activity = datetime.now()
                
                # Aguardar antes da próxima verificação
                time.sleep(300)  # 5 minutos
                
            except Exception as e:
                logging.error(f"Erro no loop principal: {e}")
                time.sleep(60)  # Aguardar 1 minuto em caso de erro

# Flask app para healthcheck
app = Flask(__name__)
bot = None

@app.route('/')
def health_check():
    """Endpoint de healthcheck para Railway"""
    global bot
    
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'bot_running': bot.is_running if bot else False,
        'daily_posts': bot.daily_posts if bot else 0,
        'daily_limit': bot.daily_limit if bot else 17,
        'last_activity': bot.last_activity.isoformat() if bot and bot.last_activity else None
    }
    
    return jsonify(status)

@app.route('/status')
def bot_status():
    """Status detalhado do bot"""
    global bot
    
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    status = {
        'bot_username': bot.bot_username,
        'is_running': bot.is_running,
        'daily_posts': bot.daily_posts,
        'daily_limit': bot.daily_limit,
        'last_reset': bot.last_reset.isoformat(),
        'last_activity': bot.last_activity.isoformat() if bot.last_activity else None,
        'processed_mentions_count': len(bot.processed_mentions)
    }
    
    return jsonify(status)

def main():
    """Função principal"""
    global bot
    
    try:
        # Inicializar bot
        bot = XAPIBot()
        
        # Verificar autenticação
        if not bot.authenticate():
            logging.error("Falha na autenticacao - Encerrando")
            return
        
        # Iniciar bot em thread separada
        bot_thread = Thread(target=bot.run_bot_loop, daemon=True)
        bot_thread.start()
        
        # Iniciar Flask app
        port = int(os.environ.get('PORT', 5000))
        logging.info(f"Iniciando servidor Flask na porta {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        logging.error(f"Erro na funcao principal: {e}")
    finally:
        if bot:
            bot.is_running = False
        logging.info("Bot encerrado")

if __name__ == "__main__":
    main()