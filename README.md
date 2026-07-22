# 🤖 Detector Inteligente de EPIs con IA (Versión Básica)

Bienvenido a esta guía práctica de **coreIndustrial**. Aquí aprenderás a conectar una cámara estándar (como una webcam o una cámara IP barata) a un modelo de Inteligencia Artificial para detectar si tus operarios llevan el casco puesto.

## 🎯 ¿Qué vamos a conseguir?
1. Leer el vídeo en tiempo real de tu cámara.
2. Analizar las imágenes usando **YOLOv8** y un modelo de Inteligencia Artificial que **ya viene incluido** en esta descarga.
3. Detectar **Cascos y Chalecos** de forma automática.
4. Si un operario permanece en zona de riesgo sin EPIs más de 5 segundos, **enviaremos una alerta a tu móvil a través de Telegram**.

---

## 🛠️ Requisitos Previos

1. **Python instalado** en tu ordenador (versión 3.8 o superior).
2. **Una cámara** conectada (Webcam USB) o la dirección IP de tu cámara de seguridad (RTSP).
3. **Telegram** instalado en tu móvil para recibir las alertas.

---

## 🚀 Instalación Paso a Paso

### 1. Instalar las librerías necesarias
Abre tu terminal o símbolo del sistema (CMD) y ejecuta el siguiente comando:

```bash
pip install opencv-python ultralytics requests flask
```

### 2. El Modelo de IA
Para que la IA sepa qué es un "casco" y qué es un "chaleco", necesita un modelo entrenado. 
**¡Buena noticia!** Ya hemos incluido en esta descarga un modelo de alta calidad (`best.pt`) entrenado específicamente para detectar Cascos y Chalecos de seguridad. No tienes que descargar nada más, funcionará nada más arrancar.

### 3. ¡Ejecutar el Detector!
Abre tu terminal en la carpeta del proyecto y ejecuta el siguiente comando para lanzar la interfaz web:

```bash
python app.py
```

Se abrirá un servidor local y podrás acceder a la interfaz web con diseño corporativo desde tu navegador en **http://127.0.0.1:5000**.
Desde allí podrás:
- Pegar tu Token de Telegram en el panel lateral.
- Ver la cámara en tiempo real haciendo clic en "Iniciar Monitorización".

---

## 🏭 ¿Quieres llevar esto a toda tu planta?
Este script es una prueba de concepto. Un entorno real industrial necesita cámaras IP, servidores robustos, conexión con sistemas PLC/SCADA y bases de datos para analizar métricas.

En **CoreIndustrial** somos expertos en digitalización y visión artificial para fábricas. Si quieres implantar sistemas de seguridad automatizados y fiables sin dolores de cabeza, **hablemos**.

🌐 [coreindustrial.es](https://coreindustrial.es)
