import requests
from config import PUSHINPAY_TOKEN, PUSHINPAY_BASE_URL

# Função para obter o token de autenticação (no caso, é fixo)
def gen_pushinpay_token():
    try:
        return {"accessToken": PUSHINPAY_TOKEN}
    except Exception as ex:
        return {'error': f'Erro ao obter token: {str(ex)}'}

# Função para criar um pagamento PIX com Pushin Pay
def create_pushinpay_pix_payment(value, webhook_url=None, repasses=None):
    try:
        # Obtem o token de acesso
        get_token = gen_pushinpay_token()
        if "error" in get_token:
            return get_token  # Retorna o erro se o token não foi obtido

        access_token = get_token["accessToken"]

        # Define o endpoint e os cabeçalhos para a requisição
        url = f'{PUSHINPAY_BASE_URL}/pix/cashIn'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        # Converte o valor para centavos (caso ainda não esteja convertido)
        value_in_cents = int(round(value * 100))

        # Define o corpo da requisição com o valor do pagamento
        payment_data = {"value": value_in_cents}
        
        # Adiciona a URL de webhook se fornecida
        if webhook_url:
            payment_data["webhook_url"] = webhook_url
        
        # Adiciona regras de divisão (split) se fornecidas
        if repasses:
            payment_data["split_rules"] = repasses

        # Realiza a requisição para criar o pagamento PIX
        response = requests.post(url, headers=headers, json=payment_data)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            payment_info = response.json()
            return {
                "id": payment_info["id"],
                "status": payment_info["status"],
                "qr_code": payment_info["qr_code_base64"],
                "qr_code_text": payment_info["qr_code"]
            }
        else:
            return {'error': f'{response.status_code} : {response.text}'}
    except Exception as ex:
        return {'error': f'Erro ao criar pagamento: {str(ex)}'}

# Função para verificar o status de um pagamento PIX no Pushin Pay
def check_pushinpay_payment_status(transaction_id):
    try:
        # Obtem o token de acesso
        get_token = gen_pushinpay_token()
        if "error" in get_token:
            return get_token  # Retorna o erro se o token não foi obtido

        access_token = get_token["accessToken"]

        # Define o endpoint e os cabeçalhos para a requisição
        url = f'{PUSHINPAY_BASE_URL}/transactions/{transaction_id}'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        # Realiza a requisição para verificar o status do pagamento
        response = requests.get(url, headers=headers)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            payment_info = response.json()
            return {
                "status": payment_info["status"],
                "value": payment_info["value"]
            }
        else:
            return {'error': f'{response.status_code} : {response.text}'}
    except Exception as ex:
        return {'status': 'error', 'error': f'Erro ao verificar pagamento: {str(ex)}'}