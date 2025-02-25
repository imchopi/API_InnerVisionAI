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

# Configurar CORS (Permite conexiones desde el frontend)
CORS(app, resources={r"/*": {"origins": "https://innervisionai.netlify.app"}})

# Configurar WebSockets
socketio = SocketIO(app, cors_allowed_origins="https://innervisionai.netlify.app", async_mode='eventlet')

# Cargar variables de entorno
load_dotenv()

# Claves de API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Cargar modelo YOLO solo cuando sea necesario
def load_yolo_model():
    return YOLO("yolov8n.pt")

# Manejar conexiones WebSocket
@socketio.on('connect')
def handle_connect():
    print("Cliente conectado:", request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado:", request.sid)

@socketio.on('frame')
def handle_frame(data):
    """Procesa un frame y detecta objetos con YOLO."""
    try:
        model = load_yolo_model()  # Cargar el modelo solo cuando se necesite
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
    return "API de InnerVisionAI funcionando �"

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
    print(f"Iniciando servidor en el puerto {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=True)