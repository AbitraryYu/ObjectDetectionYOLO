# Install IP webcam app on smartphone
# IP Webcam: https://play.google.com/store/apps/details?id=com.pas.webcam

# Enable the server with no pw set
# In this example, it is HTTP and with PROTOCOL 8080, protocol must be included

# You can also visit the link and inspect the elements, I found it it is http://ip:port/video
# Clicking the 'Browser' on the Video Renderer to see the video in realtime.
# Right Click on the stream and select 'View Image Info' on Firefox
# You will see the highlighted address, the highlighted address is the address you want to copy to cv2.VideoCapture()

import cv2
import numpy as np

# cap = cv2.VideoCapture('http://192.168.2.33:8080/video')
cap = cv2.VideoCapture(0)

picID = 0

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite("samples/misc{}.jpeg".format(picID), frame)
        print('image written to samples/top{}.jpeg\a'.format(picID))
        picID += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
