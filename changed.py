import os
import requests
import time
from pathlib import Path

cwd = os.getcwd()
# A timer
startTime = 0
# Send messages to the telegram bot EIE4430
token = "1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU"
# Your chat_id
chat_id = "380473789"
# Should I call to telegram?
prompt = True
class Listen(object):
    def __init__(self):
        self._cached_stamp = 0
        self.filename = 'D:\hey.txt'
        if not os.path.exists('D:\hey.txt'):
            Path('D:\hey.txt').touch()

    def ook(self):
        global prompt
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            file = open(self.filename, "r")
            f = file.read()
            if f == 'u':
                print('blahblahblah')
                prompt = True
            elif f == 'm':
                print('shutting up')
                prompt = False
            else:
                print('m8, sth wrong')
            file.close()
    
def send_msg(text):
    # Use telegram api
    url_req = "https://api.telegram.org/bot" + token +"/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    requests.get(url_req)


m1 = Listen()
while(1):
    if (prompt and (time.time() - startTime) > 10):
        print(prompt)
        print((time.time() -startTime) > 10)
        send_msg('hey listen')
        startTime = time.time()
    m1.ook()