import paho.mqtt.client as mqtt

# 1. 設定
MQTT_HOST = "localhost"
CLIENT_ID = "Mock_Pump_01"
TOPIC_CONTROL = "Kyberno/pump/cmd"
TOPIC_STATUS_ACT = "Kyberno/pump/status"
TOPIC_SYS_STATUS = "Kyberno/system/status"

# メッセージを受け取った時の処理
def on_message(client, userdata, msg):
    cmd = msg.payload.decode()
    print(f"[{CLIENT_ID}] 命令受信: {cmd}")
    
    if cmd == "ON":
        print(" -> ポンプ作動開始")
        client.publish(TOPIC_STATUS_ACT, "ON", retain=True)
    elif cmd == "OFF":
        print(" -> ポンプ停止")
        client.publish(TOPIC_STATUS_ACT, "OFF", retain=True)

# 2. Client作成 (ここが修正ポイント：CallbackAPIVersion.VERSION2 を追加)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)
client.on_message = on_message

# 3. 遺言設定
client.will_set(TOPIC_SYS_STATUS, payload="LWT_OFFLINE_PUMP", qos=1, retain=True)

# 4. 接続と購読
client.connect(MQTT_HOST, 1883)
client.subscribe(TOPIC_CONTROL)
client.publish(TOPIC_SYS_STATUS, "ONLINE_PUMP", retain=True)

print(f"[{CLIENT_ID}] 命令待ち受け中... (Topic: {TOPIC_CONTROL})")
client.loop_forever()