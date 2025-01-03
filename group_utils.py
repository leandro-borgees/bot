import time
from datetime import datetime, timedelta
import logging
from config import GROUP_ID, user_plans, PLANS,NOTIFICATION_IDS
import json

def send_group_link(bot, chat_id):
    """
    Envia um link dinâmico do grupo VIP para o usuário.
    Gera o link no momento do pagamento aprovado.
    """
    # ID do grupo VIP (substitua pelo ID correto do seu grupo)
    group_id = GROUP_ID  # Exemplo: substitua pelo ID real do grupo

 # Tente criar o link de convite dinâmico
    try:
        invite_link = bot.create_chat_invite_link(
            chat_id=group_id,
            expire_date=None,  # Não define uma expiração em tempo, pois queremos que expire após o clique
            member_limit=1  # Limita o link para um único uso (1 clique)
        )

        # Envia o link para o cliente
        bot.send_message(chat_id, f"✅ Pagamento aprovado! Clique no link abaixo para entrar no grupo VIP:\n{invite_link.invite_link}")
         # Notifica os administradores sobre a venda
        # Obter informações do plano do usuário
        selected_plan = user_plans.get(chat_id, "Desconhecido")
        plan_info = PLANS.get(selected_plan, (0, "Plano Desconhecido", 0))
        price = plan_info[0]

        # Notifica os administradores sobre a venda
        for admin_id in NOTIFICATION_IDS:
            try:
                bot.send_message(
                    admin_id,
                    f"🚨 *Nova venda realizada!*\n\n"
                    f"👤 Usuário: [ID {chat_id}](tg://user?id={chat_id})\n"
                    f"📦 Plano: {selected_plan}\n"
                    f"💰 Valor: R${price:.2f}",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Erro ao notificar administrador {admin_id}: {e}")


    except Exception as e:
        bot.send_message(chat_id, "⚠️ Ocorreu um erro ao gerar o link de acesso. Por favor, tente novamente mais tarde.")
        print(f"Erro ao criar o link de convite: {e}")
        return
    
   



    # Obter o plano selecionado pelo usuário
    selected_plan = user_plans.get(chat_id)
    if not selected_plan:
        bot.send_message(chat_id, "⚠️ Não foi possível identificar o plano selecionado. Entre em contato com o suporte.")
        return

    # Obter a duração do plano a partir do dicionário PLANS
    plan_info = PLANS.get(selected_plan)
    if not plan_info:
        bot.send_message(chat_id, "⚠️ Não foi possível identificar as informações do plano. Entre em contato com o suporte.")
        return

    # Calcula a data de expiração
    plan_duration = plan_info[2]  # Terceiro elemento do dicionário PLANS deve ser a duração em dias
    expiry_date = datetime.now() + timedelta(days=plan_duration)

    # Armazena as informações no arquivo JSON
    user_data = {
        "chat_id": chat_id,
        "plan": selected_plan,
        "expiry_date": expiry_date.strftime("%Y-%m-%d")
    }

    file_path = 'users.json'
    #user_data = {"id": user_id, "plan": selected_plan}
    
    try:
        # Tenta abrir o arquivo JSON para leitura
        with open(file_path, "r") as file:
            data = json.load(file)  # Lê os dados existentes
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio/corrompido, cria uma lista vazia
        data = []

    # Adiciona o novo usuário à lista
    data.append(user_data)

    # Salva os dados atualizados no arquivo JSON
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    #print(f"Dados salvos para o usuário {user_id} no plano {selected_plan}")