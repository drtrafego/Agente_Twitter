#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot X API v2 - Versão Railway Definitiva
Otimizado para deploy em produção no Railway
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

# Configurar logging APENAS para console (sem arquivo)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Inicializar Flask app
app = Flask(__name__)

# Variáveis globais
bot = None
bot_status = {
    'running': False,
    'daily_posts': 0,
    'last_activity': None,
    'error': None
}

class XAPIBot:
    def __init__(self):
        # Credenciais obrigatórias
        self.api_key = os.getenv('API_KEY')
        self.api_key_secret = os.getenv('API_KEY_SECRET')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.bot_username = os.getenv('BOT_USERNAME', 'drtrafeg0')
        
        # Validação crítica
        missing_vars = []
        if not self.api_key: missing_vars.append('API_KEY')
        if not self.api_key_secret: missing_vars.append('API_KEY_SECRET')
        if not self.access_token: missing_vars.append('ACCESS_TOKEN')
        if not self.access_token_secret: missing_vars.append('ACCESS_TOKEN_SECRET')
        if not self.bearer_token: missing_vars.append('BEARER_TOKEN')
        
        if missing_vars:
            error_msg = f"Variáveis faltando: {', '.join(missing_vars)}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        # Configurações
        self.base_url = "https://api.x.com/2"
        self.daily_limit = 17
        self.daily_posts = 0
        self.last_reset = datetime.now().date()
        self.is_running = False
        self.last_activity = datetime.now()
        
        logging.info(f"Bot inicializado para @{self.bot_username}")

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
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)),
            'oauth_version': '1.0'
        }
        
        # Combinar parâmetros
        all_params = oauth_params.copy()
        if params:
            all_params.update(params)
        
        # Criar string de parâmetros
        param_string = '&'.join([f"{k}={urllib.parse.quote(str(v), safe='')}" 
                                for k, v in sorted(all_params.items())])
        
        # Base string
        base_string = f"{method}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_string, safe='')}"
        
        # Chave de assinatura
        signing_key = f"{urllib.parse.quote(self.api_key_secret, safe='')}&{urllib.parse.quote(self.access_token_secret, safe='')}"
        
        # Gerar assinatura
        signature = base64.b64encode(
            hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
        ).decode()
        
        oauth_params['oauth_signature'] = signature
        
        # Header Authorization
        auth_header = 'OAuth ' + ', '.join([f'{k}="{urllib.parse.quote(str(v), safe="")}"' 
                                           for k, v in sorted(oauth_params.items())])
        
        return auth_header

    def authenticate(self):
        """Autentica com a API do X"""
        try:
            url = f"{self.base_url}/users/me"
            headers = {
                'Authorization': self.generate_oauth_header('GET', url),
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            logging.info(f"Auth status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                username = data.get('data', {}).get('username', 'unknown')
                logging.info(f"Autenticado como @{username}")
                return True
            else:
                logging.error(f"Erro auth: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Erro na autenticação: {e}")
            return False

    def search_mentions(self):
        """Busca menções recentes"""
        try:
            query = f"@{self.bot_username} -is:retweet"
            url = f"{self.base_url}/tweets/search/recent"
            params = {
                'query': query,
                'max_results': 10,
                'tweet.fields': 'created_at,author_id,conversation_id'
            }
            
            headers = {
                'Authorization': f"Bearer {self.bearer_token}",
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            logging.info(f"Search status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                tweets = data.get('data', [])
                logging.info(f"Encontradas {len(tweets)} menções")
                return tweets
            elif response.status_code == 429:
                logging.warning("Rate limit - aguardando...")
                return []
            else:
                logging.error(f"Erro search: {response.status_code}")
                return []
                
        except Exception as e:
            logging.error(f"Erro na busca: {e}")
            return []

    def create_tweet(self, text, reply_to=None):
        """Cria um tweet"""
        try:
            url = f"{self.base_url}/tweets"
            
            payload = {'text': text}
            if reply_to:
                payload['reply'] = {'in_reply_to_tweet_id': reply_to}
            
            headers = {
                'Authorization': self.generate_oauth_header('POST', url),
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            logging.info(f"Tweet status: {response.status_code}")
            
            if response.status_code == 201:
                self.daily_posts += 1
                self.last_activity = datetime.now()
                logging.info(f"Tweet criado! Posts hoje: {self.daily_posts}/{self.daily_limit}")
                return True
            else:
                logging.error(f"Erro tweet: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Erro ao criar tweet: {e}")
            return False

    def process_mentions(self):
        """Processa menções e responde"""
        mentions = self.search_mentions()
        
        for mention in mentions:
            if self.daily_posts >= self.daily_limit:
                logging.info("Limite diário atingido")
                break
                
            tweet_id = mention.get('id')
            text = mention.get('text', '')
            
            # Resposta simples
            response_text = "Olá! Obrigado por me mencionar. Como posso ajudar?"
            
            if self.create_tweet(response_text, reply_to=tweet_id):
                logging.info(f"Respondeu à menção: {tweet_id}")
                time.sleep(2)  # Evitar rate limit

    def run_bot_loop(self):
        """Loop principal do bot"""
        self.is_running = True
        
        while self.is_running:
            try:
                # Reset diário
                today = datetime.now().date()
                if today > self.last_reset:
                    self.daily_posts = 0
                    self.last_reset = today
                    logging.info("Contador diário resetado")
                
                # Processar menções
                if self.daily_posts < self.daily_limit:
                    self.process_mentions()
                
                # Atualizar status
                global bot_status
                bot_status.update({
                    'running': True,
                    'daily_posts': self.daily_posts,
                    'last_activity': self.last_activity.isoformat(),
                    'error': None
                })
                
                # Aguardar próximo ciclo
                time.sleep(300)  # 5 minutos
                
            except Exception as e:
                logging.error(f"Erro no loop: {e}")
                bot_status['error'] = str(e)
                time.sleep(60)  # Aguardar 1 minuto em caso de erro

# Endpoints Flask
@app.route('/', methods=['GET'])
def healthcheck():
    """Endpoint de healthcheck"""
    global bot_status
    
    return jsonify({
        'status': 'healthy',
        'bot_running': bot_status['running'],
        'daily_limit': 17,
        'daily_posts': bot_status['daily_posts'],
        'last_activity': bot_status['last_activity'],
        'timestamp': datetime.now().isoformat(),
        'error': bot_status['error']
    })

@app.route('/status', methods=['GET'])
def status():
    """Status detalhado"""
    return healthcheck()

def init_bot():
    """Inicializa o bot para Railway"""
    global bot, bot_status
    
    try:
        logging.info("Iniciando bot para Railway...")
        
        # Criar instância do bot
        bot = XAPIBot()
        
        # Autenticar
        if not bot.authenticate():
            raise Exception("Falha na autenticação")
        
        # Iniciar em thread separada
        bot_thread = Thread(target=bot.run_bot_loop, daemon=True)
        bot_thread.start()
        
        bot_status['running'] = True
        logging.info("Bot inicializado com sucesso!")
        
    except Exception as e:
        error_msg = f"Erro na inicialização: {e}"
        logging.error(error_msg)
        bot_status['error'] = error_msg
        bot_status['running'] = False

# Inicializar bot automaticamente
init_bot()

# Para execução local
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logging.info(f"Iniciando servidor na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)