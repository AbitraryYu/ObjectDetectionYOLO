import editfile
import requests
import telegram
import time

# Create telegram Bot
bot = telegram.Bot(token="1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU")
# Send messages to the telegram bot EIE4430
token = "1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU"
# Your chat_id
chat_id = "380473789"
# StartTime
startTime = 0


def send_msg(text):
    # Use telegram api
    url_req = (
        "https://api.telegram.org/bot"
        + token
        + "/sendMessage"
        + "?chat_id="
        + chat_id
        + "&text="
        + text
    )
    requests.get(url_req)


while 1:

    if time.time() - startTime > 10:
        text = editfile.read()
        if text == "g":
            send_msg(
                "Detected stuff that may harm the baby. Please remove it as soon as possible."
            )
            editfile.write("u")
            startTime = time.time()
