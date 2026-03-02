import threading
import sqlite3
from fastapi import FastAPI
from app.api.endpoints import pump, sensor
from app.core.config import settings
from app.core.mqtt_client import start_mqtt

app = FastAPI(title=settings.PROJECT_NAME)

def init_db():
    with sqlite3.connect("sensor_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                value1 REAL,
                value2 REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                device_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()


app.include_router(pump.router, prefix="/pump", tags=["Pump"])
app.include_router(sensor.router, prefix="/sensor", tags=["Sensor"])

@app.on_event("startup")
def startup_event():
    init_db()  
    threading.Thread(target=start_mqtt, daemon=True).start()

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}