import logging
import psutil
import threading
import time
from telebot import TeleBot
from config import TOKEN_BOT, GROUP_ID
from handlers import send_welcome, callback_query_handler   
from remove_users import start_daily_task
import json
import threading
import time
from datetime import datetime, timedelta
from telebot import TeleBot
from config import TOKEN_BOT




# Configura o logging para o bot
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)

# Inicializa o bot
bot = TeleBot(TOKEN_BOT)

@bot.message_handler(commands=['start', 'reiniciar'])
def welcome_message(message):
   send_welcome(bot, message)


# Configura o manipulador de callback
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    callback_query_handler(bot, call)

@bot.message_handler(func=lambda message: True)
def handle_unknown_message(message):
    """
    Responde a mensagens que não são reconhecidas pelo bot.
    """
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "⚠️ Não entendi sua mensagem.\n"
        "Use o comando /start para iniciar a conversa e ver as opções disponíveis.",
        parse_mode="Markdown"
    )




# Função para monitorar o status do bot
def monitor_bot_status():
    while True:
        try:
            memory_usage = psutil.Process().memory_info().rss / 1024 ** 2  # Em MB
            cpu_usage = psutil.Process().cpu_percent(interval=1)  # Percentual
            logging.info(f"Uso de memória: {memory_usage:.2f} MB")
            logging.info(f"Uso de CPU: {cpu_usage:.2f}%")
            time.sleep(10)
        except Exception as e:
            logging.error(f"Erro no monitoramento de status: {e}")

# Função para reiniciar o bot em caso de falha
def start_bot_polling():
    while True:
        try:
            logging.info("Iniciando o polling do bot...")
            bot.polling()
        except Exception as e:
            logging.error(f"Erro no polling do bot: {e}. Reiniciando em 3 segundos...")
            time.sleep(3)


# Thread para monitorar o status do bot
status_thread = threading.Thread(target=monitor_bot_status, daemon=True)
status_thread.start()

# Inicia tarefas diárias em uma thread separada
daily_task_thread = threading.Thread(target=start_daily_task, args=(bot, GROUP_ID), daemon=True)
daily_task_thread.start()


# Inicia o bot                           
if __name__ == "__main__":
    start_bot_polling()