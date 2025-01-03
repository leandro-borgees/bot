from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Função para responder com o ID do usuário
def get_id(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    update.message.reply_text(f"Seu ID é: {user_id}")

def main():
    # Insira o token do seu bot aqui
    TOKEN = "SEU_TOKEN_AQUI"

    # Configuração do bot
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # Adiciona o comando /meuid para obter o ID
    dispatcher.add_handler(CommandHandler("meuid", get_id))

    # Inicia o bot
    updater.start_polling()
    print("Bot está rodando... Pressione Ctrl+C para interromper.")
    updater.idle()

if __name__ == "__main__":
    main()

