import json
import sqlite3
import threading
import paho.mqtt.client as mqtt
from datetime import datetime

DB_FILE = "sensor_data.db"
db_lock = threading.Lock()

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    if topic == "Kyberno/sensor/data":
        try:
            data = json.loads(payload)
            temp = data["temp"]
            humi = data["humi"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # DBへの書き込み（INSERT）
            with db_lock:
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO data_logs (timestamp, type, value1, value2) VALUES (?, ?, ?, ?)",
                        (timestamp, "sensor", temp, humi)
                    )
                    conn.commit()
            print(f"【DB記録】{timestamp} -> 温度:{temp}℃ 湿度:{humi}%")
        except Exception as e:
            print(f"【エラー】DB保存失敗: {e}")

def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = lambda c, u, f, rc: c.subscribe("Kyberno/sensor/data")
    client.connect("localhost", 1883, 60)
    client.loop_forever()