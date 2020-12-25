import cv2

rotateOption = [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180,

# Flipping the image by a random degree with a factor of 90
dst = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
