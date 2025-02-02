import numpy as np
import argparse
import cv2
import os
import time
import requests
import telegram

startTime = 0
# Create telegram Bot
bot = telegram.Bot(token="1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU")
# Send messages to the telegram bot EIE4430
token = "1408532525:AAEpFAGIzqcUUC3S3khTCWHyWUYm196I8WU"
# Your chat_id
chat_id = "380473789"
# Should I call telegram?
prompt = True


def extract_boxes_confidences_classids(outputs, confidence, width, height):
    boxes = []
    confidences = []
    classIDs = []

    for output in outputs:
        for detection in output:
            # Extract the scores, classid, and the confidence of the prediction
            scores = detection[5:]
            classID = np.argmax(scores)
            conf = scores[classID]

            # Consider only the predictions that are above the confidence threshold
            if conf > confidence:
                # Scale the bounding box back to the size of the image
                box = detection[0:4] * np.array([width, height, width, height])
                centerX, centerY, w, h = box.astype("int")

                # Use the center coordinates, width and height to get the coordinates of the top left corner
                x = int(centerX - (w / 2))
                y = int(centerY - (h / 2))

                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(conf))
                classIDs.append(classID)

    return boxes, confidences, classIDs


def draw_bounding_boxes(image, boxes, confidences, classIDs, idxs, colors):
    if len(idxs) > 0:
        for i in idxs.flatten():
            # extract bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]

            # draw the bounding box and label on the image
            color = [int(c) for c in colors[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
            cv2.putText(
                image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

    return image


def make_prediction(net, layer_names, labels, image, confidence, threshold):
    height, width = image.shape[:2]

    # Create a blob and pass it through the model
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (320, 320), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(layer_names)

    # Extract bounding boxes, confidences and classIDs
    boxes, confidences, classIDs = extract_boxes_confidences_classids(
        outputs, confidence, width, height
    )

    # Apply Non-Max Suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

    return boxes, confidences, classIDs, idxs


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


# def get_updates():
#    # Use telegram api
#    url_req = "https://api.telegram.org/bot" + token +"/getUpdates" + "?timeout=10"
#    results = requests.get(url_req)
#    json = results.json()
#    if(json['result'][-1]['message'].get('text')):
#        msg = json['result'][-1]['message']['text']
#        if (msg == "/mute"):
#            return False
#        elif (msg == "/unmute"):
#            return True
#        else: return True
#    else: return True


def send_photo():
    bot.send_photo(chat_id=chat_id, photo=open("photo/screenshot.jpg", "rb"))


class Listen(object):
    def __init__(self):
        self._cached_stamp = 0
        self.filename = "state.txt"
        if not os.path.exists("state.txt"):
            Path("state.txt").touch()

    def checkfile(self):
        global prompt
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            file = open(self.filename, "r")
            f = file.read()
            if f == "u":
                print("blahblahblah")
                prompt = True
            elif f == "m":
                print("shutting up")
                prompt = False
            else:
                print("m8, sth wrong")
            file.close()


listener = Listen()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--weights",
        type=str,
        default="model/yolov3.weights",
        help="Path to model weights",
    )
    parser.add_argument(
        "-cfg",
        "--config",
        type=str,
        default="model/yolov3.cfg",
        help="Path to configuration file",
    )
    parser.add_argument(
        "-l",
        "--labels",
        type=str,
        default="model/coco.names",
        help="Path to label file",
    )
    parser.add_argument(
        "-c",
        "--confidence",
        type=float,
        default=0.5,
        help="Minimum confidence for a box to be detected.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.3,
        help="Threshold for Non-Max Suppression",
    )
    parser.add_argument(
        "-u",
        "--use_gpu",
        default=False,
        action="store_true",
        help="Use GPU (OpenCV must be compiled for GPU). For more info checkout: https://www.pyimagesearch.com/2020/02/03/how-to-use-opencvs-dnn-module-with-nvidia-gpus-cuda-and-cudnn/",
    )
    parser.add_argument(
        "-s",
        "--save",
        default=False,
        action="store_true",
        help="Whether or not the output should be saved",
    )
    parser.add_argument(
        "-sh", "--show", default=True, action="store_false", help="Show output"
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "-i", "--image_path", type=str, default="", help="Path to the image file."
    )
    input_group.add_argument(
        "-v", "--video_path", type=str, default="", help="Path to the video file."
    )

    args = parser.parse_args()

    # Get the labels
    labels = open(args.labels).read().strip().split("\n")

    # Create a list of colors for the labels
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

    # Load weights using OpenCV
    net = cv2.dnn.readNetFromDarknet(args.config, args.weights)

    if args.use_gpu:
        print("Using GPU")
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    if args.save:
        print("Creating output directory if it doesn't already exist")
        os.makedirs("output", exist_ok=True)

    # Get the output layer names
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    if args.image_path != "":
        image = cv2.imread(args.image_path)

        boxes, confidences, classIDs, idxs = make_prediction(
            net, layer_names, labels, image, args.confidence, args.threshold
        )

        image = draw_bounding_boxes(image, boxes, confidences, classIDs, idxs, colors)

        # show the output image
        if args.show:
            cv2.imshow("YOLO Object Detection", image)
            cv2.waitKey(0)

        if args.save:
            cv2.imwrite(f'output/{args.image_path.split("/")[-1]}', image)
    else:
        if args.video_path != "":
            cap = cv2.VideoCapture(args.video_path)
        else:
            # cap = cv2.VideoCapture(0)
            # cap = cv2.VideoCapture('http://192.168.2.33:8080/video')
            cap = cv2.VideoCapture("http://192.168.2.7:8080/video")

        if args.save:
            width = int(cap.get(3))
            height = int(cap.get(4))
            fps = cap.get(cv2.CAP_PROP_FPS)
            name = args.video_path.split("/")[-1] if args.video_path else "camera.avi"
            out = cv2.VideoWriter(
                f"output/{name}",
                cv2.VideoWriter_fourcc("M", "J", "P", "G"),
                fps,
                (width, height),
            )

        while cap.isOpened():
            ret, image = cap.read()

            if not ret:
                print("Video file finished.")
                break

            boxes, confidences, classIDs, idxs = make_prediction(
                net, layer_names, labels, image, args.confidence, args.threshold
            )

            image = draw_bounding_boxes(
                image, boxes, confidences, classIDs, idxs, colors
            )

            # print(classIDs)
            # if (len(classIDs) > 0 and (time.time() - startTime > 10) and get_updates()):
            # if (len(classIDs) > 0 and (time.time() - startTime > 10)):
            listener.checkfile()
            if len(classIDs) > 0 and (time.time() - startTime > 10) and prompt:
                send_msg(
                    "Detected stuff that may harm the baby. Please remove it as soon as possible."
                )
                startTime = time.time()

            text = open("state.txt", "r").read()
            if text == "i":
                cv2.imwrite("current.jpeg", image)

            if args.show:
                cv2.imshow("YOLO Object Detection", image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            if args.save:
                out.write(image)

        cap.release()
        if args.save:
            out.release()
    cv2.destroyAllWindows()
