import time
import logging
import threading
import queue
from config import user_plans, user_payment_methods, gateway_pagamento, processed_payments
from mercado_pago_api import get_payment_status as get_mp_payment_status
from efi_api import get_efi_payment_status
from pushinpay_api import check_pushinpay_payment_status
from group_utils import send_group_link

# Configura o logging para depuração
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Fila para manter os pagamentos que precisam ser verificados
payment_queue = queue.Queue()

# Função que coloca o pagamento na fila para ser verificado
def enqueue_payment_verification(bot, chat_id, payment_id, payment_method):
    payment_queue.put((bot, chat_id, payment_id, payment_method))
    logging.debug(f"Pagamento enfileirado para verificação: {payment_id}")

# Função para processar a fila de pagamentos em uma thread separada
def process_payment_queue():
    while True:
        bot, chat_id, payment_id, payment_method = payment_queue.get()
        try:
            handle_payment_verification(bot, chat_id, payment_id, payment_method)
        except Exception as e:
            logging.error(f"Erro ao verificar pagamento: {e}")
        finally:
            payment_queue.task_done()  # Marca a tarefa como concluída

# Função que verifica o status do pagamento periodicamente
def handle_payment_verification(bot, chat_id, payment_id, payment_method):
    """
    Verifica o status do pagamento periodicamente para determinar se foi aprovado.
    """
    start_time = time.time()
    while time.time() - start_time < 15 * 60:  # Verifica durante 15 minutos

        # Se o pagamento já foi processado, interrompe a verificação
        if payment_id in processed_payments:
            logging.debug(f"Pagamento {payment_id} já processado. Ignorando.")
            return

        # Verificação para o Mercado Pago
        if payment_method == 'credit_card' or gateway_pagamento == "mercado_pago":
            status = get_mp_payment_status(payment_id)
            logging.debug("Status Mercado Pago: %s", status)
            if status and status.get('status') == 'approved':
                #bot.send_message(chat_id, "✅ Pagamento aprovado! Clique no link abaixo para entrar no grupo VIP:")
                #send_group_link(bot, chat_id)
                processed_payments.add(payment_id)  # Marca o pagamento como processado
                return

        # Verificação para o gateway Efí
        elif gateway_pagamento == "efi":
            status = get_efi_payment_status(payment_id)
            logging.debug("Status Efí: %s", status)
            if status == 'approved':
                #bot.send_message(chat_id, "✅ Pagamento aprovado! Clique no link abaixo para entrar no grupo VIP:")
                #send_group_link(bot, chat_id)
                processed_payments.add(payment_id)  # Marca o pagamento como processado
                return
            elif status == 'expired':
                bot.send_message(chat_id, "⚠️ A cobrança expirou. Vamos gerar um novo código para você.")
                break
            elif status == 'pending':
                logging.debug("Pagamento pendente. Reavaliando...")

        # Verificação para o Pushin Pay
        elif gateway_pagamento == "pushin_pay":
            status_info = check_pushinpay_payment_status(payment_id)
            logging.debug("Status Pushin Pay: %s", status_info)
            if status_info.get('status') == 'paid':
                #bot.send_message(chat_id, "✅ Pagamento aprovado! Clique no link abaixo para entrar no grupo VIP:")
                #send_group_link(bot, chat_id)
                processed_payments.add(payment_id)  # Marca o pagamento como processado
                return
            elif status_info.get('status') == 'PENDING':
                logging.debug("Pagamento pendente para ID %s. Reavaliando.", payment_id)
            elif status_info.get('status') == 'FAILED':
                bot.send_message(chat_id, "⚠️ O pagamento falhou. Tente novamente.")
                break

        # Espera 1 minuto antes de verificar novamente
        time.sleep(60)

    # Caso o pagamento não seja confirmado no tempo limite
    bot.send_message(chat_id, "⏳ O pagamento não foi confirmado a tempo. Vamos gerar um novo código para você.")
    plan = user_plans.get(chat_id)
    if plan:
        payment_method = user_payment_methods.get(chat_id)
        if payment_method == 'credit_card':
            from handlers import send_payment_link  # Importação local para evitar ciclo
            send_payment_link(bot, chat_id, plan)
        elif payment_method == 'pix':
            from handlers import send_pix_code  # Importação local para evitar ciclo
            send_pix_code(bot, chat_id, plan)

# Inicia uma thread para processar a fila de pagamentos
payment_thread = threading.Thread(target=process_payment_queue, daemon=True)
payment_thread.start()