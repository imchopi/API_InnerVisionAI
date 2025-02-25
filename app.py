import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import cv2
import numpy as np
import requests
from dotenv import load_dotenv
import os
from ultralytics import YOLO

# Inicializar Flask
app = Flask(__name__)

# Configurar CORS (Evita bloqueos con Netlify)
CORS(app, resources={r"/*": {"origins": "https://innervisionai.netlify.app"}})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://innervisionai.netlify.app"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Configurar WebSockets
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Cargar variables de entorno
load_dotenv()

# Cargar modelo YOLO
model = YOLO("yolov8n.pt")

# Claves de API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

@socketio.on('frame')
def handle_frame(data):
    """Procesa un frame y detecta objetos con YOLO."""
    try:
        image_bytes = np.frombuffer(data['image'], dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        if image is None:
            print("Error al decodificar la imagen")
            return

        results = model(image)

        detections = []
        for result in results:
            for box in result.boxes:
                xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
                confidence = round(box.conf.item(), 2)
                class_id = int(box.cls.item())
                class_name = model.names.get(class_id, "Desconocido")

                detections.append({
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": [xmin, ymin, xmax, ymax]
                })

        socketio.emit('detections', detections)
    except Exception as e:
        print("Error procesando el frame:", str(e))

@app.route("/")
def home():
    return "API de InnerVisionAI funcionando 🚀"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    """Maneja las solicitudes del chatbot y conecta con OpenAI."""
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight OK"}), 200

    try:
        data = request.json
        message = data.get("message")

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": message}]
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)

        if response.status_code == 200:
            return jsonify({"response": response.json()["choices"][0]["message"]["content"]})
        else:
            return jsonify({"error": "Error al obtener respuesta del chatbot"}), 500
    except Exception as e:
        print("Error al conectar con OpenAI:", str(e))
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    """Inicia el servidor Flask con WebSockets en Render."""
    port = int(os.getenv("PORT", 5000))  
    socketio.run(app, host='0.0.0.0', port=port)
