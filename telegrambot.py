import editfile
import telegram
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# This is the muteFlag for YOLO
muteFlag = False

# Create telegram Bot
bot = telegram.Bot(token='1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU')
# Send messages to the telegram bot EIE4430
token = "1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU"
# Your chat_id
chat_id = "380473789"

def mute(update: Update, context: CallbackContext) -> None:
    muteFlag = True
    update.message.reply_text(f'The state is now' + str(muteFlag))
    editfile.write('m')


def unmute(update: Update, context: CallbackContext) -> None:
    muteFlag = False
    update.message.reply_text(f'The state is now' + str(muteFlag))
    editfile.write('u')

def send_photo():
    bot.send_photo(chat_id=chat_id, photo=open('current.jpeg', 'rb'))

def image(update: Update, context: CallbackContext) -> None:
    text = editfile.read()
    editfile.write('i')
    time.sleep(3)
    send_photo()
    editfile.write(text)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

updater = Updater('1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU')


updater.dispatcher.add_handler(CommandHandler('mute', mute))
updater.dispatcher.add_handler(CommandHandler('unmute', unmute))
updater.dispatcher.add_handler(CommandHandler('image', image))

# Must be added last
unknown_handler = MessageHandler(Filters.command, unknown)
updater.dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
