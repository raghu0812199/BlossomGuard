import io
from PIL import Image
from ultralytics import YOLO
from flask import Flask, request
import nest_asyncio
from pyngrok import ngrok
from collections import Counter

app = Flask(__name__)
model = YOLO('D:/PyCharmProjects/flowerDetection2.0/runs/detect/train2/weights/best.pt')

@app.route("/detect", methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        results = model(img)

        classnames = model.names
        flowername = list()
        for r in results:
            for cn in r.boxes.cls:
                flowername.append(classnames[int(cn)])

        flowerdic = Counter(flowername)
        results_json = {"boxes": results[0].boxes.xyxy.tolist(),
                        "flowers": flowerdic}
        return {"result": results_json}



ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
app.run(host="0.0.0.0", port=8000)