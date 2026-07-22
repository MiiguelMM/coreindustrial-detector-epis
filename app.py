import cv2
import time
import requests
from flask import Flask, render_template, Response, request, jsonify
from ultralytics import YOLO

app = Flask(__name__)

# Configuración global simulada (en un entorno real iría a base de datos)
class Config:
    TELEGRAM_TOKEN = ""
    TELEGRAM_CHAT_ID = ""
    ALERT_TIME = 5
    IS_RUNNING = False

current_detections = {
    "helmet": False,
    "vest": False
}

# Cargamos el modelo real
try:
    model = YOLO("best.pt")
except Exception:
    model = None

def enviar_alerta_telegram(mensaje):
    if not Config.TELEGRAM_TOKEN or not Config.TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": Config.TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        requests.post(url, json=payload)
        return True
    except:
        return False

import os

def generate_frames():
    # Intenta usar un vídeo de prueba si existe, si no usa la webcam
    if os.path.exists('demo.mp4'):
        cap = cv2.VideoCapture('demo.mp4')
    else:
        cap = cv2.VideoCapture(0)
        
    tiempo_inicio_sin_casco = 0
    alerta_enviada = False

    while Config.IS_RUNNING:
        success, frame = cap.read()
        
        # Si el vídeo termina, reiniciarlo en bucle
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = cap.read()
            if not success:
                break
        
        if model:
            results = model(frame, verbose=False, conf=0.5)
            persona_detectada = False
            casco_detectado = False
            
            # Reset current frame detections
            current_detections['helmet'] = False
            current_detections['vest'] = False

            # Para que no vaya a cámara rápida (limitamos a ~30 fps aprox si el modelo va muy rápido)
            time.sleep(0.03)

            for box in results[0].boxes:
                class_name = model.names[int(box.cls[0])].lower()
                
                # Mapeo real de clases
                if class_name in ['person', 'persona']: persona_detectada = True
                
                is_target_class = False
                display_name = ""

                if class_name in ['helmet', 'casco', 'hard-hat', 'hardhat', 'head', 'hard hat']: 
                    casco_detectado = True
                    current_detections['helmet'] = True
                    is_target_class = True
                    display_name = "CASCO"
                if class_name in ['safety vest', 'vest', 'chaleco', 'reflective']:
                    current_detections['vest'] = True
                    is_target_class = True
                    display_name = "CHALECO"
                
                # Dibujar SOLAMENTE casco y chaleco en el vídeo real
                if is_target_class:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    conf = float(box.conf[0])
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"{display_name} {conf:.2f}"
                    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    cv2.rectangle(frame, (x1, y1 - 20), (x1 + tw, y1), (0, 255, 0), -1)
                    cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            if persona_detectada and not casco_detectado:
                if tiempo_inicio_sin_casco == 0:
                    tiempo_inicio_sin_casco = time.time()
                    alerta_enviada = False
                
                tiempo_transcurrido = time.time() - tiempo_inicio_sin_casco
                
                if tiempo_transcurrido >= Config.ALERT_TIME and not alerta_enviada:
                    enviar_alerta_telegram("🚨 ALERTA PRL: Operario sin casco detectado.")
                    alerta_enviada = True
            else:
                tiempo_inicio_sin_casco = 0
                alerta_enviada = False

            # Ya no usamos el plot automático para que no salgan chalecos ni personas
            # frame = results[0].plot()
            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
    # Si se apaga, mandamos un frame en negro
    black_frame = cv2.imencode('.jpg', cv2.resize(cv2.imread('templates/blank.jpg') if False else frame, (640,480)))[1].tobytes()
    yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + black_frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    if Config.IS_RUNNING:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return "Camera is off", 204

@app.route('/api/toggle', methods=['POST'])
def toggle_camera():
    data = request.json
    Config.IS_RUNNING = data.get('status', False)
    if not Config.IS_RUNNING:
        current_detections['helmet'] = False
        current_detections['vest'] = False
    return jsonify({"status": "ok"})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(current_detections)

@app.route('/api/config', methods=['POST'])
def update_config():
    data = request.json
    Config.TELEGRAM_TOKEN = data.get('token', '')
    Config.TELEGRAM_CHAT_ID = data.get('chat_id', '')
    Config.ALERT_TIME = int(data.get('alert_time', 5))
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 COREINDUSTRIAL - MONITOR IA INICIADO")
    print("Abre tu navegador web en: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=False, port=5000)
