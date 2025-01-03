import threading
import time
from datetime import datetime
import json
import logging
from datetime import datetime, timedelta
from config import  PLANS, PLANS_RENEW
from telebot import types
from payment_verification import enqueue_payment_verification






def notify_users_about_expiration(bot):
    try:
        # Carrega os dados do arquivo JSON
        with open('users.json', 'r') as file:
            users = json.load(file)

        today = datetime.now().date()
        warning_dates = [today + timedelta(days=5), today + timedelta(days=1)]

        for user in users:
            expiry_date = datetime.strptime(user['expiry_date'], "%Y-%m-%d").date()
            if expiry_date in warning_dates:
                send_renewal_notification(bot, user)
    except Exception as e:
        logging.error(f"Erro ao verificar planos prestes a expirar: {e}")


def send_renewal_notification(bot, user):
    chat_id = user['chat_id']
    plan = user['plan']
    discount = PLANS_RENEW.get(plan, 0)
    
    markup = types.InlineKeyboardMarkup()
    renew_button = types.InlineKeyboardButton(
        f"Renovar Agora com Desconto",
        callback_data=f"renew_{chat_id}"
    )
    markup.add(renew_button)
    
    bot.send_message(
        chat_id,
        f"⚠️ Seu plano '{plan}' está prestes a expirar!\n"
        f"Renove agora com desconto e continue aproveitando os benefícios exclusivos.",
        parse_mode="Markdown",
        reply_markup=markup
    )


# Atualizar registro no JSON após a renovação
from datetime import datetime, timedelta
import json

def update_user_plan(chat_id, plan, periodicity):
    """
    Renova o plano e a data de expiração de um usuário no arquivo 'users.json'.
    
    Args:
        chat_id (int): O ID do chat do usuário no Telegram.
        plan (str): O plano escolhido pelo usuário (ex.: "VIP BRONZE", "VIP PRATA").
        periodicity (int): O número de dias que o plano será válido.
    """
    try:
        # Carrega os dados existentes do arquivo JSON
        file_path = 'users.json'
        try:
            with open(file_path, 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        # Flag para indicar se o usuário foi encontrado
        user_found = False

        # Procura o usuário pelo chat_id e atualiza os dados
        for user in users:
            if user['chat_id'] == chat_id:
                # Atualiza o plano e calcula a nova data de expiração
                expiry_date = datetime.now() + timedelta(days=periodicity)
                user['plan'] = plan
                user['expiry_date'] = expiry_date.strftime("%Y-%m-%d")
                user_found = True
                break

        if not user_found:
            # Caso o usuário não exista no arquivo, cria um novo registro
            expiry_date = datetime.now() + timedelta(days=periodicity)
            new_user = {
                "chat_id": chat_id,
                "plan": plan,
                "expiry_date": expiry_date.strftime("%Y-%m-%d")
            }
            users.append(new_user)

        # Salva os dados atualizados no arquivo JSON
        with open(file_path, "w") as file:
            json.dump(users, file, indent=4)

        print(f"Plano do usuário {chat_id} atualizado/renovado para {plan}. Expira em {expiry_date.strftime('%Y-%m-%d')}.")
    except Exception as e:
        print(f"Erro ao renovar o plano do usuário: {e}")






def remove_expired_users(bot, group_id):
    """Remove usuários do grupo VIP cujo plano expirou."""
    try:
        # Carrega os dados do arquivo JSON
        with open('users.json', 'r') as file:
            users = json.load(file)

        # Data atual no formato esperado
        today = datetime.now().strftime("%Y-%m-%d")

        # Filtrar usuários com planos vencidos
        expired_users = [user for user in users if user['expiry_date'].startswith(today)]

        if expired_users:
            for user in expired_users:
                try:
                    # Remove o usuário do grupo
                    bot.kick_chat_member(group_id, user['chat_id'])
                    print(f"Usuário {user['chat_id']} removido do grupo.")
                except Exception as e:
                    print(f"Erro ao remover o usuário {user['chat_id']}: {e}")

            # Atualiza o arquivo JSON removendo os usuários expirados
            users = [user for user in users if not user['expiry_date'].startswith(today)]
            with open('users.json', 'w') as file:
                json.dump(users, file, indent=4)
        else:
            print("Nenhum usuário com plano vencido para remover hoje.")

    except Exception as e:
        print(f"Erro ao processar a remoção de usuários: {e}")

def daily_task_scheduler(bot, group_id):
    while True:
        now = datetime.now()
        if now.hour == 20 and now.minute == 46:
            notify_users_about_expiration(bot)
            remove_expired_users(bot, group_id)
            time.sleep(60)
        else:
            time.sleep(10)


def start_daily_task(bot, group_id):
    """Inicia a tarefa de agendamento em um thread separado."""
    task_thread = threading.Thread(target=daily_task_scheduler, args=(bot, group_id))
    task_thread.daemon = True  # Torna o thread um thread daemons para encerrar automaticamente
    task_thread.start()