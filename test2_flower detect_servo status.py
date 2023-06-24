import json
import cv2
import base64
import numpy as np
import requests
import time

with open('roboflow_config.json') as f:
    config = json.load(f)

    ROBOFLOW_API_KEY = config["ROBOFLOW_API_KEY"]
    ROBOFLOW_MODEL = config["ROBOFLOW_MODEL"]
    ROBOFLOW_SIZE = config["ROBOFLOW_SIZE"]

    FRAMERATE = config["FRAMERATE"]
    BUFFER = config["BUFFER"]
    IP_ADDRESS ="10.150.0.69"
    PORT="80"

upload_url = "".join([
    "https://detect.roboflow.com/",
    ROBOFLOW_MODEL,
    "?api_key=",
    ROBOFLOW_API_KEY,
    "&format=JSON",
    "&stroke=5"
])

video = cv2.VideoCapture('http://10.150.1.67:8080/video')

def send_servo_request(state):
    url = f'http://{IP_ADDRESS}:{PORT}/?servo={state}'
    response = requests.get(url)
    print('Response:', response.text)

def infer():
    ret, img = video.read()

    height, width, channels = img.shape
    scale = ROBOFLOW_SIZE / max(height, width)
    img = cv2.resize(img, (round(scale * width), round(scale * height)))

    retval, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)

    resp = requests.post(upload_url, data=img_str, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }, stream=True).raw

    result = json.loads(resp.read().decode('utf-8'))

    print(result)

    if result["predictions"]:
        print(1)
        send_servo_request("on")
        try:
            image = np.asarray(bytearray(base64.b64decode(result["predictions"][0]["image"])), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            for prediction in result["predictions"]:
                tl = (int(prediction["x_min"]), int(prediction["y_min"]))
                br = (int(prediction["x_max"]), int(prediction["y_max"]))
                label = prediction["class"]
                confidence = prediction["confidence"]
                color = (0, 255, 0)
                cv2.rectangle(image, tl, br, color, 2)
                cv2.putText(image, f"{label}: {confidence:.2f}", tl, cv2.FONT_HERSHEY_TRIPLEX, 0.5, color, 1)
        except KeyError:
            image = img
    else:
        send_servo_request("off")
        image = img

    return image

while True:
    if(cv2.waitKey(1) == ord('q')):
        break

    start = time.time()

    image = infer()

    cv2.imshow('image', image)

    print((1/(time.time()-start)), " fps")

video.release()
cv2.destroyAllWindows()