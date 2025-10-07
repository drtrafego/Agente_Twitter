import tweepy
import time
import random
import threading
import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da API do Twitter
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

# URL de conexão do banco de dados Neon
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def setup_database():
    """Cria a tabela da fila de tweets se ela não existir."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tweet_queue (
            id SERIAL PRIMARY KEY,
            tweet_id BIGINT NOT NULL,
            author_id BIGINT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            process_after TIMESTAMP WITH TIME ZONE NOT NULL,
            processed BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Banco de dados configurado com sucesso.")

def response_worker():
    """Processa a fila de tweets do banco de dados."""
    print("Worker de resposta iniciado.")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Seleciona tweets que estão prontos para serem processados
            cur.execute("SELECT id, tweet_id FROM tweet_queue WHERE process_after <= CURRENT_TIMESTAMP AND processed = FALSE ORDER BY created_at LIMIT 1;")
            tweet_to_process = cur.fetchone()

            if tweet_to_process:
                db_id, tweet_id = tweet_to_process
                print(f"Processando tweet ID: {tweet_id}")

                try:
                    # Lógica para responder ao tweet
                    with open("respostas.txt", "r", encoding="utf-8") as f:
                        respostas = [linha.strip() for linha in f if linha.strip()]
                    
                    if respostas:
                        resposta = random.choice(respostas)
                        client_v2.create_tweet(in_reply_to_tweet_id=tweet_id, text=resposta)
                        print(f"Tweet {tweet_id} respondido com: '{resposta}'")

                        # Marca o tweet como processado
                        cur.execute("UPDATE tweet_queue SET processed = TRUE WHERE id = %s;", (db_id,))
                        conn.commit()
                    else:
                        print("Arquivo de respostas está vazio.")

                except tweepy.errors.TweepyException as e:
                    print(f"Erro ao responder ao tweet {tweet_id}: {e}")
                    # Opcional: Adicionar lógica para tentar novamente mais tarde

            cur.close()
        except psycopg2.Error as e:
            print(f"Erro de banco de dados no worker: {e}")
        finally:
            if conn:
                conn.close()
        
        # Espera antes de verificar a fila novamente
        time.sleep(10)

class MentionStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"Menção recebida de @{tweet.author_id}: {tweet.text}")
        
        # Calcula o tempo para processamento (delay de 2 a 4 minutos)
        delay = random.randint(120, 240)
        process_after = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() + delay))

        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tweet_queue (tweet_id, author_id, process_after) VALUES (%s, %s, %s);",
                (tweet.id, tweet.author_id, process_after)
            )
            conn.commit()
            cur.close()
            print(f"Tweet {tweet.id} adicionado à fila para processar em {delay} segundos.")
        except psycopg2.Error as e:
            print(f"Erro ao inserir tweet na fila: {e}")
        finally:
            if conn:
                conn.close()

    def on_connection_error(self):
        print("Erro de conexão com a stream. Tentando reconectar...")
        time.sleep(15)

if __name__ == "__main__":
    # Garante que a tabela do banco de dados exista
    setup_database()

    # Autenticação com a API v2 para responder
    client_v2 = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    # Inicia o worker de resposta em uma thread separada
    worker_thread = threading.Thread(target=response_worker, daemon=True)
    worker_thread.start()

    # Inicia a escuta de menções
    stream = MentionStream(BEARER_TOKEN)
    
    # Limpa regras antigas
    rules = stream.get_rules().data
    if rules:
        stream.delete_rules([rule.id for rule in rules])
        print("Regras de stream antigas foram limpas.")

    # Adiciona nova regra para ouvir menções
    rule = f"to:{BOT_USERNAME}"
    stream.add_rules(tweepy.StreamRule(rule))
    print(f"Regra de stream adicionada: '{rule}'")

    print("Iniciando a escuta por menções...")
    stream.filter(threaded=True)