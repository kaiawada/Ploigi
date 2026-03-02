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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if topic == "Kyberno/sensor/data":
        try:
            data = json.loads(payload)
            temp = data["temp"]
            humi = data["humi"]
            
            with db_lock:
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO data_logs (timestamp, type, value1, value2) VALUES (?, ?, ?, ?)",
                        (timestamp, "sensor", temp, humi)
                    )
                    conn.commit()
            print(f"【DB記録/データ】{timestamp} -> 温度:{temp}℃ 湿度:{humi}%")
        except Exception as e:
            print(f"【エラー】センサーデータ保存失敗: {e}")

    elif topic == "Kyberno/system/status":
        try:
            with db_lock:
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO system_events (timestamp, device_id, event_type, status) VALUES (?, ?, ?, ?)",
                        (timestamp, "NodeMCU_01", "STATUS_CHANGE", payload)
                    )
                    conn.commit()
            print(f"【DB記録/イベント】{timestamp} -> デバイス状態: {payload}")
        except Exception as e:
            print(f"【エラー】システムイベント保存失敗: {e}")

def start_mqtt():

    client = mqtt.Client()
    client.on_message = on_message
    
    def on_connect(c, u, f, rc):
        if rc == 0:
            print("MQTT Connected successfully.")

            c.subscribe("Kyberno/sensor/data")
            c.subscribe("Kyberno/system/status")
        else:
            print(f"Connection failed with code {rc}")
    
    client.on_connect = on_connect
    client.connect("localhost", 1883, 60)
    client.loop_forever()