import paho.mqtt.client as mqtt
import json
import time
import random

# 1. まず設定（変数）を定義する
MQTT_HOST = "localhost" 
CLIENT_ID = "Mock_Sensor_01"
TOPIC_DATA = "Kyberno/sensor/data"
TOPIC_STATUS = "Kyberno/system/status"

# 2. Clientを作成する（ここを1行にまとめます）
# CallbackAPIVersion.VERSION2 を指定し、その後に CLIENT_ID を渡す
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)

# 3. 遺言設定
client.will_set(TOPIC_STATUS, payload="LWT_OFFLINE_SENSOR", qos=1, retain=True)

# 4. 接続
client.connect(MQTT_HOST, 1883)
client.publish(TOPIC_STATUS, "ONLINE_SENSOR", retain=True)

print(f"[{CLIENT_ID}] 起動中... Ctrl+C で停止")

try:
    while True:
        temp = round(random.uniform(24.0, 26.0), 1)
        humi = round(random.uniform(50.0, 60.0), 1)
        
        payload = {"temp": temp, "humi": humi}
        client.publish(TOPIC_DATA, json.dumps(payload))
        
        print(f"送信データ: {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    client.publish(TOPIC_STATUS, "OFFLINE_SENSOR", retain=True)
    client.disconnect()