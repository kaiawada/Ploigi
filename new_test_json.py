import json
from datetime import datetime

payload = '{"temp": 25.5, "humi": 60.2}'

data = json.loads(payload)

temperature = data["temp"]
humidity = data["humi"]


now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"[{now}] 受信成功！")
print(f"温度: {temperature}度 / 湿度: {humidity}%")