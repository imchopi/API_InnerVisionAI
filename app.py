import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import cv2
import numpy as np
import requests
from dotenv import load_dotenv  # Cargar variables desde .env
import os
from ultralytics import YOLO
import eventlet

# Inicializar Flask
app = Flask(__name__)

# Configurar CORS para permitir solicitudes desde el frontend en producción
CORS(app, origins=["https://innervisionai.netlify.app/"])  # Permite solicitudes de solo este origen en específico (Frontend del Chatbot)

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
    """
    Procesa un frame recibido desde el frontend, aplica detección de objetos con YOLO y envía las detecciones de vuelta.
    """
    try:
        # Decodificar imagen desde base64
        image_bytes = np.frombuffer(data['image'], dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        if image is None:
            print("Error al decodificar la imagen")
            return

        # Detectar objetos con YOLO
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

        # Enviar detecciones al frontend
        socketio.emit('detections', detections)
    except Exception as e:
        print("Error procesando el frame:", str(e))

@app.route("/chat", methods=["POST"])
def chat():
    """
    Maneja las solicitudes del chatbot, enviando el mensaje del usuario a la API de OpenAI y devolviendo la respuesta.
    """
    try:
        data = request.json  # Obtener datos de la solicitud HTTP
        message = data.get("message")  # Extraer el mensaje enviado por el usuario

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": message}]
        }

        # Enviar solicitud a OpenAI
        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            return jsonify({"response": response.json()["choices"][0]["message"]["content"]})
        else:
            return jsonify({"error": "Error al obtener respuesta del chatbot"}), 500
    except Exception as e:
        print("Error al conectar con OpenAI:", str(e))
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    """
    Inicia el servidor Flask con WebSockets en un puerto dinámico (Render lo asigna automáticamente).
    """
    port = int(os.getenv("PORT", 5000))  # Usar el puerto asignado por Render o 5000 por defecto
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
