# Configurações do bot e API
TOKEN_BOT = '7516053180:AAF1SodlNPxn5x8185Q3_wc78vbWX1y7ZFE'
TOKEN_MERCADOPAGO = 'APP_USR-2179435799020724-091320-904084a56a6f1be88dc5073f27d65a08-270581412'
CLIENTE_ID = 'Client_Id_fb6ae71e1705caf64079ae8e085ff132ba10f4b3'
CLIENT_SECRET = 'Client_Secret_53e430bcbc2a5d329543d40778d9205bf5df9296'
CERTIFICADO_EFI = 'venv\producao-611378-deu certo_cert.pem'
GROUP_LINK = 'https://t.me/+tp36DLxdBq05ZjUx'
ID_DONO = 'SyncAdmin_bot'
GROUP_ID = -1002492656387
PUSHINPAY_TOKEN = '4102|MQl3KR5zWV8UJLDdnGL8AmNzdqWa6hc56CUzMph3ca85b864'
PUSHINPAY_BASE_URL = 'https://api.pushinpay.com.br/api'

NOTIFICATION_IDS = [1199857681] 


welcome_image = 'welcome_image.jpg'

PLANS = {
    "VIP BRONZE": (7.50, "🔥 VIP BRONZE - 7 dias de acesso ", 7),
    "VIP PRATA": (14.90, "✨ VIP PRATA - 30 dias de acesso ", 30),
    "VIP OURO": (47.90, "🏆 VIP OURO - 1 ano de acesso ", 365),
    "VIP PRO": (77.90, "💎 VIP PRO - VITALÍCIO + 10 Grupos ", 9999999),
}


DISCOUNTS = {
    "VIP BRONZE": 10,  # 10% de desconto
    "VIP PRATA": 20,  # 20% de desconto
    "VIP OURO": 15,  # 15% de desconto
    "VIP PRO": 25,  # 25% de desconto
}


# Atualizando o dicionário de planos para renovação considerando o desconto
PLANS_RENEW = {
    f"{plan}": (
        round(price * (1 - discount / 100), 2),  # Calcula o preço com desconto
        f"{description.strip()}",    # Adiciona 'Renovação' ao texto
        duration,
    )
    for plan, (price, description, duration) in PLANS.items()
    for discount in [DISCOUNTS.get(plan, 0)]  # Obtém o desconto correspondente
}


# Escolha do Gateway de pagamento
gateway_pagamento = "mercado_pago"  # Opções: "efi", "mercado_pago" e "pushin_pay"

# Armazenamento temporário de planos e métodos de pagamento escolhidos
user_plans = {}
user_payment_methods = {}



# Dicionário para rastrear pagamentos já processados
processed_payments = set()  # Armazena os IDs dos usuários processados