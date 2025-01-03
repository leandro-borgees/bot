from config import PLANS, user_plans, user_payment_methods, gateway_pagamento,welcome_image,PLANS_RENEW
from mercado_pago_api import create_payment_preference, create_pix_payment, get_payment_status as get_mp_payment_status
from efi_api import create_efi_pix_payment, get_efi_payment_status
from pushinpay_api import create_pushinpay_pix_payment, check_pushinpay_payment_status
from payment_verification import enqueue_payment_verification
from group_utils import send_group_link
import threading
from telebot import types
import logging
import time
from remove_users import update_user_plan
import threading
import json
from datetime import datetime, timedelta
from telebot import TeleBot
from time import sleep

# Configuração do bot
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")



def send_welcome(bot, message):
    chat_id = message.chat.id


    
    # Envia uma imagem como mensagem de boas-vindas
    with open("welcome_image.jpg", "rb") as photo:
        bot.send_photo(
            chat_id,
            photo,
            caption=(
                "🔥 Seja Bem-Vindo ao Maior Grupo VIP do Telegram! 🔥\n\n"
                "🔞 MAIOR GRUPO VIP DE PUTARI@ 🔞\n\n"
                "O que você vai encontrar aqui:\n"
                "🔹 Onlyfans\n"
                "🔹 CloseFriends\n"
                "🔹 Privacy\n"
                "🔹 Incesto Real\n"
                "🔹 Grupo de Live\n"
                "🔹 XVideosRed\n"
                "🔹 DarkWEB\n"
                "🔹 Vazadas\n"
                "🔹 Tufos\n"
                "🔹 E muito mais...\n\n"
                "Nossos planos são os melhores do mercado!\n"
                "⚡ Acesso Total e Vantagens Exclusivas \n"
                "📞 Link do Suporte: @Suporte_OnlyFuns"
            )
        )
    
     # Aguardar 2 segundos antes de continuar
    time.sleep(1.5)

    # Exibe as opções de plano
    show_plan_options(bot, chat_id)



def show_plan_options(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    for key, (price, description, periodicity) in PLANS.items():
        button_text = f"{description} - R${price:.2f}"
        markup.add(types.InlineKeyboardButton(button_text, callback_data=f"plan_{key}"))

    message_text = (
        "🔥 **Nossos Planos!!!** 🔥\n\n"
        "🔸 **🥉 VIP BRONZE**\n"
        "➡️ Acesso TOTAL por **7 dias**\n\n"
        "🔸 **🥈 VIP PRATA**\n"
        "➡️ Acesso TOTAL por **30 dias** + **Categorias Especiais**\n\n"
        "🔸 **🥇 VIP OURO**\n"
        "➡️ **O campeão de vendas**\n"
        "➡️ Acesso **VITALÍCIO** + **todas as categorias especiais** + **novos conteúdos**\n\n"
        "🔸 **💎 VIP PRO**\n"
        "➡️ **O mais desejado**\n"
        "➡️ Acesso **VITALÍCIO**\n"
        "➡️ Tudo do VIP OURO + **10 GRUPOS EXCLUSIVOS**\n\n"
        "⚡️ **Benefícios dos planos OURO e PRO**\n"
        "🔒 Pagamento único, acesso **permanente**.\n"
        "📞 **Suporte**: @Suporte\_OnlyFuns\n"
        "🛡️ **Pagamento 100% garantido** via Mercado Pago (PIX/CARTÃO)"
    )

    bot.send_message(chat_id, message_text, reply_markup=markup, parse_mode="Markdown")


def show_plan_option_discounts(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    for key, (price, description, periodicity) in PLANS_RENEW.items():
        button_text = f"{description} - R${price:.2f}"
        markup.add(types.InlineKeyboardButton(button_text, callback_data=f"discounts_{key}"))

    message_text = (
        "🔥 **Nossos Planos!!!** 🔥\n\n"
        "🔸 **🥉 VIP BRONZE**\n"
        "➡️ Acesso TOTAL por **7 dias**\n\n"
        "🔸 **🥈 VIP PRATA**\n"
        "➡️ Acesso TOTAL por **30 dias** + **Categorias Especiais**\n\n"
        "🔸 **🥇 VIP OURO**\n"
        "➡️ **O campeão de vendas**\n"
        "➡️ Acesso **VITALÍCIO** + **todas as categorias especiais** + **novos conteúdos**\n\n"
        "🔸 **💎 VIP PRO**\n"
        "➡️ **O mais desejado**\n"
        "➡️ Acesso **VITALÍCIO**\n"
        "➡️ Tudo do VIP OURO + **10 GRUPOS EXCLUSIVOS**\n\n"
        "⚡️ **Benefícios dos planos OURO e PRO**\n"
        "🔒 Pagamento único, acesso **permanente**.\n\n"
        "📞 **Suporte**: @Suporte\_OnlyFuns\n"
        "🛡️ **Pagamento 100% garantido** via Mercado Pago (PIX/CARTÃO)"
    )

    bot.send_message(chat_id, message_text, reply_markup=markup, parse_mode="Markdown")




def show_payment_method_options(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 Cartão de Crédito", callback_data="payment_credit_card"))
    markup.add(types.InlineKeyboardButton("🔗 Pix", callback_data="payment_pix_code"))
    #markup.add(types.InlineKeyboardButton("📷 Pix - QR Code", callback_data="payment_pix_qr"))
    bot.send_message(chat_id, "  o método de pagamento:", reply_markup=markup)

def show_payment_method_options_discounts(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 Cartão de Crédito", callback_data="payment_credit_card_discounts"))
    markup.add(types.InlineKeyboardButton("🔗 Pix", callback_data="payment_pix_code_discounts"))
    #markup.add(types.InlineKeyboardButton("📷 Pix - QR Code", callback_data="payment_pix_qr"))
    bot.send_message(chat_id, "Escolha o método de pagamento:", reply_markup=markup)

def callback_query_handler(bot, call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id  # Obtém o ID da mensagem com os botões

    if call.data.startswith("renew_"):
        # Exibe as opções de planos para renovação
        show_plan_option_discounts(bot, chat_id)
    
    elif call.data.startswith("discounts_"):
        plan = call.data.split("_")[1]
        user_plans[chat_id] = plan
        bot.send_message(chat_id, f"🔄 Você escolheu renovar o plano {PLANS_RENEW[plan][1]} com o valor de R${PLANS_RENEW[plan][0]:.2f}.")
        show_payment_method_options_discounts(bot, chat_id)

    
    if call.data.startswith("plan_"):
        plan = call.data.split("_")[1]
        user_plans[chat_id] = plan
        bot.send_message(chat_id, f"🔹 Você escolheu o {PLANS[plan][1]} no valor de R${PLANS[plan][0]:.2f}.")
        show_payment_method_options(bot, chat_id)

    elif call.data == "payment_credit_card":
        plan = user_plans.get(chat_id)
        if plan:
            user_payment_methods[chat_id] = 'credit_card'
            send_payment_link(bot, chat_id, plan)


    elif call.data == "payment_pix_code":
        plan = user_plans.get(chat_id)
        if plan:
            user_payment_methods[chat_id] = 'pix'
            send_pix_code(bot, chat_id, plan, send_qr=False)

    elif call.data == "payment_credit_card_discounts":
        plan = user_plans.get(chat_id)
        if plan:
            user_payment_methods[chat_id] = 'credit_card'
            send_payment_link_discounts(bot, chat_id, plan)


    elif call.data == "payment_pix_code_discounts":
        plan = user_plans.get(chat_id)
        if plan:
            user_payment_methods[chat_id] = 'pix'
            send_pix_code_discounts(bot, chat_id, plan, send_qr=False)


    elif call.data == "payment_pix_qr":
        plan = user_plans.get(chat_id)
        if plan:
            user_payment_methods[chat_id] = 'pix'
            send_pix_code(bot, chat_id, plan, send_qr=True)

    elif call.data.startswith("verify_payment:"):
        payment_id = call.data.split(":")[1]
        if gateway_pagamento == "mercado_pago":
            status = get_mp_payment_status(payment_id)
            status_check = status.get('status') == 'approved'
        elif gateway_pagamento == "efi":
            status = get_efi_payment_status(payment_id)
            status_check = status == 'approved'
        elif gateway_pagamento == "pushin_pay":
            status_info = check_pushinpay_payment_status(payment_id)
            status_check = status_info.get('status') == 'paid'

        else:
            status_check = False

        if status_check:
            # Remove os botões após a confirmação do pagamento
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)

            # Envia o link do grupo VIP
            send_group_link(bot, chat_id)
        else:
            # Exibe a mensagem informando que o pagamento ainda não foi identificado
            bot.answer_callback_query(
                call.id, 
                "⚠️ Pagamento ainda não identificado. Aguarde um momento."
            )

    else:
        bot.answer_callback_query(call.id, "⚠️ O pagamento ainda não foi confirmado.")

    if call.data.startswith("verify_payment_discounts:"):
        payment_id = call.data.split(":")[1]
        if gateway_pagamento == "mercado_pago":
            status = get_mp_payment_status(payment_id)
            status_check = status.get('status') == 'approved'
        elif gateway_pagamento == "efi":
            status = get_efi_payment_status(payment_id)
            status_check = status == 'approved'
        elif gateway_pagamento == "pushin_pay":
            status_info = check_pushinpay_payment_status(payment_id)
            status_check = status_info.get('status') == 'paid'

        if status_check:
        # Remove os botões após a confirmação do pagamento
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)

        # Atualiza o registro do usuário
        plan = user_plans.get(chat_id)
        if plan:
            amount, description, periodicity = PLANS_RENEW[plan]
            update_user_plan(chat_id, plan, periodicity)

        # Envia a confirmação de renovação
        bot.send_message(chat_id, "✅ Seu plano foi renovado com sucesso! Aproveite mais dias de acesso VIP.", parse_mode="Markdown")
      
    else:
        bot.answer_callback_query(call.id, "⚠️ O pagamento ainda não foi confirmado.")




def send_payment_link(bot, chat_id, plan):
    amount, description,periodicity = PLANS[plan]
    preference = create_payment_preference(amount, description)
    if not preference:
        bot.send_message(chat_id, "⚠️ Ocorreu um erro ao gerar o pagamento. Tente novamente mais tarde.")
        return

    payment_url = preference['init_point']
    payment_id = preference['id']

    bot.send_message(chat_id, "💳 Clique no link abaixo para realizar o pagamento com cartão de crédito:")
    bot.send_message(chat_id, payment_url)

    markup = types.InlineKeyboardMarkup()
    pay_btn = types.InlineKeyboardButton("Verificar Pagamento", callback_data=f"verify_payment:{payment_id}")
    markup.add(pay_btn)

    bot.send_message(chat_id, "✅ Após efetuar o pagamento, clique no botão abaixo:", reply_markup=markup)
    enqueue_payment_verification(bot, chat_id, payment_id, 'credit_card')

def send_payment_link_discounts(bot, chat_id, plan):
    amount, description,periodicity = PLANS_RENEW[plan]
    preference = create_payment_preference(amount, description)
    if not preference:
        bot.send_message(chat_id, "⚠️ Ocorreu um erro ao gerar o pagamento. Tente novamente mais tarde.")
        return

    payment_url = preference['init_point']
    payment_id = preference['id']

    bot.send_message(chat_id, "💳 Clique no link abaixo para realizar o pagamento com cartão de crédito:")
    bot.send_message(chat_id, payment_url)

    markup = types.InlineKeyboardMarkup()
    pay_btn = types.InlineKeyboardButton("Verificar Pagamento", callback_data=f"verify_payment_discounts:{payment_id}")
    markup.add(pay_btn)

    bot.send_message(chat_id, "✅ Após efetuar o pagamento, clique no botão abaixo:", reply_markup=markup)
    enqueue_payment_verification(bot, chat_id, payment_id, 'credit_card')

def escape_markdown(text):
    escape_chars = r'_*\[\]()~>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

def send_pix_code(bot, chat_id, plan, send_qr=True):
    amount, description,periodicity = PLANS[plan]

    if gateway_pagamento == "mercado_pago":
        payment = create_pix_payment(amount, description)
        if not payment:
            bot.send_message(chat_id, "⚠️ Ocorreu um erro ao gerar o pagamento. Tente novamente mais tarde.")
            return
        pix_code = payment['point_of_interaction']['transaction_data']['qr_code']
        payment_id = payment['id']

    elif gateway_pagamento == "efi":
        payment = create_efi_pix_payment(amount, description,periodicity)
        if not payment:
            bot.send_message(chat_id, "⚠️ Ocorreu um erro ao gerar o pagamento. Tente novamente mais tarde.")
            return
        pix_code = payment['pixCopiaECola']
        payment_id = payment['txid']

    elif gateway_pagamento == "pushin_pay":
        payment = create_pushinpay_pix_payment(amount)
        if not payment or "error" in payment:
            bot.send_message(chat_id, f"⚠️ Ocorreu um erro ao gerar o pagamento: {payment.get('error', 'Erro desconhecido')}")
            return
        pix_code = payment['qr_code_text']
        payment_id = payment['id']
    
    else:
        bot.send_message(chat_id, "⚠️ Gateway de pagamento inválido.")
        return

    qr_code_url = f"https://quickchart.io/qr?text={pix_code}"  # URL do QR Code

    markup = types.InlineKeyboardMarkup()
    pay_btn = types.InlineKeyboardButton("Verificar Pagamento", callback_data=f"verify_payment:{payment_id}")
    markup.add(pay_btn)

    if send_qr:
        bot.send_message(chat_id, "🔗 Aqui está seu QR Code. Escaneie e pague no seu banco:")
        bot.send_photo(chat_id, qr_code_url, reply_markup=markup)
        pix_code_box = f"<pre>{pix_code}</pre>"
        bot.send_message(chat_id, "🔗 Aqui está seu código Pix. Copie e pague no seu banco:", parse_mode="HTML")
        bot.send_message(chat_id, pix_code_box, parse_mode="HTML", reply_markup=markup)
    else:
        pix_code_box = f"<pre>{pix_code}</pre>"
        bot.send_message(chat_id, "🔗 Aqui está seu código Pix. Copie e pague no seu banco:", parse_mode="HTML")
        bot.send_message(chat_id, pix_code_box, parse_mode="HTML", reply_markup=markup)

    enqueue_payment_verification(bot, chat_id, payment_id, 'pix')

def send_pix_code_discounts(bot, chat_id, plan, send_qr=True):
    amount, description,periodicity = PLANS_RENEW[plan]

    if gateway_pagamento == "mercado_pago":
        payment = create_pix_payment(amount, description)
        if not payment:
            bot.send_message(chat_id, "⚠️ Ocorreu um erro ao gerar o pagamento. Tente novamente mais tarde.")
            return
        pix_code = payment['point_of_interaction']['transaction_data']['qr_code']
        payment_id = payment['id']

    elif gateway_pagamento == "efi":
        payment = create_efi_pix_payment(amount, description,periodicity)
        if not payment:
            bot.send_message(chat_id, "⚠️ Ocorreu um erro ao gerar o pagamento. Tente novamente mais tarde.")
            return
        pix_code = payment['pixCopiaECola']
        payment_id = payment['txid']

    elif gateway_pagamento == "pushin_pay":
        payment = create_pushinpay_pix_payment(amount)
        if not payment or "error" in payment:
            bot.send_message(chat_id, f"⚠️ Ocorreu um erro ao gerar o pagamento: {payment.get('error', 'Erro desconhecido')}")
            return
        pix_code = payment['qr_code_text']
        payment_id = payment['id']
    
    else:
        bot.send_message(chat_id, "⚠️ Gateway de pagamento inválido.")
        return

    qr_code_url = f"https://quickchart.io/qr?text={pix_code}"  # URL do QR Code

    markup = types.InlineKeyboardMarkup()
    pay_btn = types.InlineKeyboardButton("Verificar Pagamento", callback_data=f"verify_payment_discounts:{payment_id}")
    markup.add(pay_btn)

    if send_qr:
        bot.send_message(chat_id, "🔗 Aqui está seu QR Code. Escaneie e pague no seu banco:")
        bot.send_photo(chat_id, qr_code_url, reply_markup=markup)
        pix_code_box = f"<pre>{pix_code}</pre>"
        bot.send_message(chat_id, "🔗 Aqui está seu código Pix. Copie e pague no seu banco:", parse_mode="HTML")
        bot.send_message(chat_id, pix_code_box, parse_mode="HTML", reply_markup=markup)
    else:
        pix_code_box = f"<pre>{pix_code}</pre>"
        bot.send_message(chat_id, "🔗 Aqui está seu código Pix. Copie e pague no seu banco:", parse_mode="HTML")
        bot.send_message(chat_id, pix_code_box, parse_mode="HTML", reply_markup=markup)

    enqueue_payment_verification(bot, chat_id, payment_id, 'pix')

def clear_user_data(chat_id):
    user_plans.pop(chat_id, None)
    user_payment_methods.pop(chat_id, None)
    logging.debug(f"Dados temporários removidos para o chat_id: {chat_id}")