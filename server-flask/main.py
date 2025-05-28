import cv2 as cv
import requests
import numpy as np
from ultralytics import YOLO
from flask import Flask, jsonify, request
from flask_cors import CORS

model_placa = YOLO("./yoloModels/placa.pt")
model_texto = YOLO("./yoloModels/textoplaca.pt")
app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Você precisa enviar um arquivo."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nome de arquivo vazio!"}), 400

    file_bytes = file.read()
    imgBuffer = np.frombuffer(file_bytes, np.uint8)
    image = cv.imdecode(imgBuffer, cv.IMREAD_COLOR)

    # Detecta a placa com o modelo YOLO de placas
    result_placa = model_placa(image)
    boxes = result_placa[0].boxes

    if boxes is None or len(boxes) != 1:
        # Se não achou uma placa, tenta detectar o texto da placa com outro modelo
        result_texto = model_texto(image)
        boxes_texto = result_texto[0].boxes

        if boxes_texto is None or len(boxes_texto) == 0:
            res = requests.post(
                "http://localhost:3001/upload",
                files={"file": ("placa.jpg", file_bytes, "image/jpeg")},
            )

            if res.status_code != 200:
                return (
                    jsonify({"error": "Erro ao se comunicar com o servidor OCR"}),
                    500,
                )
            return jsonify({"message": res.json()}), 200

        # Usa a primeira box de texto detectada
        box_text = boxes_texto[0]
        x1, y1, x2, y2 = map(int, box_text.xyxy[0].tolist())
        cropped = image[y1:y2, x1:x2]

        _, img_encoded = cv.imencode(".jpg", cropped)

        res = requests.post(
            "http://localhost:3001/upload",
            files={"file": ("placa.jpg", img_encoded.tobytes(), "image/jpeg")},
        )

        if res.status_code != 200:
            return jsonify({"error": "Erro ao se comunicar com o servidor OCR"}), 500
        return jsonify({"message": res.json()}), 200

    # Uma placa detectada → recorta e envia
    box = boxes[0]

    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
    cropped_placa = image[y1:y2, x1:x2]

    # Usa o modelo de texto para refinar a área do texto na placa recortada
    result_texto_na_placa = model_texto(cropped_placa)
    boxes_texto = result_texto_na_placa[0].boxes

    if boxes_texto is None or len(boxes_texto) == 0:
        # Se não detectou texto na placa recortada, envia a placa recortada mesmo assim
        _, img_encoded = cv.imencode(".jpg", cropped_placa)
    else:
        # Se detectou texto, recorta a região do texto dentro da placa recortada
        box_texto = boxes_texto[0]
        x1t, y1t, x2t, y2t = map(int, box_texto.xyxy[0].tolist())
        cropped_texto = cropped_placa[y1t:y2t, x1t:x2t]
        _, img_encoded = cv.imencode(".jpg", cropped_texto)

    # Envia o recorte final (texto refinado ou placa inteira) para o servidor OCR
    res = requests.post(
        "http://localhost:3001/upload",
        files={"file": ("placa.jpg", img_encoded.tobytes(), "image/jpeg")},
    )

    if res.status_code != 200:
        return jsonify({"error": "Erro ao se comunicar com o servidor OCR"}), 500
    return jsonify({"message": res.json()}), 200


if __name__ == "__main__":
    app.run(debug=True)
