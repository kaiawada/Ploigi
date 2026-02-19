from fastapi import FastAPI
import json
import threading
import paho.mqtt.client as mqtt
from datetime import datetime
from app.api.endpoints import pump
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

sensor_logs = []

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    if topic == "Kyberno/sensor/data":
        try:
            data = json.loads(payload)
            temp = data["temp"]
            humi = data["humi"]
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = {"time": timestamp, "temp": temp, "humi": humi}
            sensor_logs.append(log_entry)
            
            print(f"【成功】{timestamp} 測定完了 -> 温度:{temp}℃ 湿度:{humi}%")

        except Exception as e:
            print(f"【エラー】データの解析に失敗しました: {e} / 受信内容: {payload}")

def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = lambda c, u, f, rc: c.subscribe("Kyberno/sensor/data")
    client.connect("localhost", 1883, 60)
    client.loop_forever()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=start_mqtt, daemon=True).start()

app.include_router(pump.router, prefix="/pump", tags=["Pump"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

@app.get("/sensor/check")
async def check_sensor():
    return {"current_logs": sensor_logs}