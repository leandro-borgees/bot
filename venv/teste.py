import telebot

# Substitua pelo token do seu bot
TOKEN_BOT = '7516053180:AAF1SodlNPxn5x8185Q3_wc78vbWX1y7ZFE'
bot = telebot.TeleBot(TOKEN_BOT)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Envia o ID do grupo onde a mensagem foi recebida
    group_id = message.chat.id
    bot.send_message(message.chat.id, f'O ID deste grupo é: {group_id}')

# Este comando deve ser enviado no grupo onde o bot foi adicionado
bot.polling()
