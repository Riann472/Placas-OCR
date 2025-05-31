# Imports
import cv2 as cv
import numpy as np
import requests
import torch
from flask import Flask, jsonify, request
from flask_cors import CORS
from ultralytics import YOLO

# Carrega os modelos YOLO para detecção das placas
model_placa = YOLO("./yoloModels/placa.pt")
model_texto = YOLO("./yoloModels/textoplaca.pt")

app = Flask(__name__)
CORS(app)


# Função para encodar a imagem para enviar para o servidor node
def encode_image(img):
    _, img_encoded = cv.imencode(".jpg", img)
    return img_encoded.tobytes()


# Função pra mandar a requisição para o ocr
def enviar_para_ocr(image_bytes):
    res = requests.post(
        "http://localhost:3001/upload",
        files={"file": ("placa.jpg", image_bytes, "image/jpeg")},
    )
    if res.status_code != 200:
        return None, {"error": "Erro ao se comunicar com o servidor OCR"}
    return res.json(), None


# Endpoint upload
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Você precisa enviar um arquivo."}), 400

    # Caso tenha um arquivo, joga ele em uma variavel
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nome de arquivo vazio!"}), 400

    # transforma essa imagem em uint8 para o openCV processar a imagem e armazenar em uma variavel
    imgBuffer = np.frombuffer(file.read(), np.uint8)
    image = cv.imdecode(imgBuffer, cv.IMREAD_COLOR)

    # Desativa o calculo de gradientes do torch e detecta a posição da primeira placa encontrada
    with torch.no_grad():
        result_placa = model_placa(image)
    boxes = result_placa[0].boxes

    # Se nao detectar placa nenhuma, assume que o usuario ja enviou a placa cortada e segue para detecção do texto
    if not boxes or len(boxes) != 1:
        with torch.no_grad():
            result_texto = model_texto(image)
        boxes_texto = result_texto[0].boxes

        # Se não detectar textos, assume que o usuario ja cortou o texto ou que não há placas na imagem, assim enviando a imagem original para o OCR
        if not boxes_texto:
            ocr_result, error = enviar_para_ocr(encode_image(image))
            if error:
                return jsonify(error), 500
            return jsonify({"message": ocr_result}), 200

        # Caso detecte textos de placa, corta a imagem para esse texto e envia para o ocr
        x1, y1, x2, y2 = map(int, boxes_texto[0].xyxy[0].tolist())
        cropped = image[y1:y2, x1:x2]
        ocr_result, error = enviar_para_ocr(encode_image(cropped))
        if error:
            return jsonify(error), 500
        return jsonify({"message": ocr_result}), 200

    # Caso detecte placa, corta o texto a partir da placa cortada e envia pro ocr
    x1, y1, x2, y2 = map(int, boxes[0].xyxy[0].tolist())
    cropped_placa = image[y1:y2, x1:x2]

    with torch.no_grad():
        result_texto_na_placa = model_texto(cropped_placa)
    boxes_texto = result_texto_na_placa[0].boxes

    # Se detectar texto na placa, corta e envia pro ocr
    if boxes_texto:
        x1t, y1t, x2t, y2t = map(int, boxes_texto[0].xyxy[0].tolist())
        cropped_placa = cropped_placa[y1t:y2t, x1t:x2t]

    ocr_result, error = enviar_para_ocr(encode_image(cropped_placa))
    if error:
        return jsonify(error), 500
    return jsonify({"message": ocr_result}), 200


if __name__ == "__main__":
    app.run(debug=True)
