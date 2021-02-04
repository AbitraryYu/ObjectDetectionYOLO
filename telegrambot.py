import editfile
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# This is the muteFlag for YOLO
muteFlag = False

def mute(update: Update, context: CallbackContext) -> None:
    muteFlag = True
    update.message.reply_text(f'The state is now' + str(muteFlag))
    editfile.write('m')


def unmute(update: Update, context: CallbackContext) -> None:
    muteFlag = False
    update.message.reply_text(f'The state is now' + str(muteFlag))
    editfile.write('u')

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

updater = Updater('1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU')


updater.dispatcher.add_handler(CommandHandler('mute', mute))
updater.dispatcher.add_handler(CommandHandler('unmute', unmute))

# Must be added last
unknown_handler = MessageHandler(Filters.command, unknown)
updater.dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()