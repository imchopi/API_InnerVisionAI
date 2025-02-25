from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import cv2
import numpy as np
import requests
from dotenv import load_dotenv
import os
from ultralytics import YOLO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://innervisionai.netlify.app"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Cargar variables desde .env
load_dotenv()

# Cargar modelo YOLO más ligero (YOLOv5n)
model = YOLO("yolov5nu.pt")

# Claves de API de OpenAI obtenidas de las variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Limitar el número de conexiones simultáneas
MAX_CONNECTIONS = 10  # Ajusta según sea necesario

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "https://innervisionai.netlify.app"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# Función para redimensionar la imagen
def resize_image(image, target_width=640):
    height, width = image.shape[:2]
    scale_factor = target_width / width
    new_height = int(height * scale_factor)
    resized_image = cv2.resize(image, (target_width, new_height))
    return resized_image

@socketio.on('connect')
def handle_connect():
    # Limitar el número de conexiones simultáneas
    if len(socketio.server.manager.rooms) > MAX_CONNECTIONS:
        raise ConnectionRefusedError('Demasiadas conexiones activas')

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

        # Redimensionar la imagen para reducir el uso de RAM
        image = resize_image(image, target_width=640)

        # Detectar objetos con YOLO
        results = model(image)

        # Liberar memoria de la imagen
        del image

        # Limitar el número de detecciones
        max_detections = 10  # Ajusta según sea necesario
        detections = []
        for result in results:
            for box in result.boxes[:max_detections]:  # Limitar detecciones
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

        # Enviar solicitud a OpenAI para obtener la respuesta del chatbot
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
    port = int(os.environ.get('PORT', 4000))  # Usa el puerto de Render o 5000 por defecto
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
