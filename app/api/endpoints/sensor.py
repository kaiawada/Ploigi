from fastapi import APIRouter
import sqlite3

router = APIRouter()
DB_FILE = "sensor_data.db"

@router.get("/history")
async def get_history():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row  
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT timestamp, value1, value2 FROM data_logs WHERE type = 'sensor' ORDER BY id DESC LIMIT 50"
        )
        rows = cursor.fetchall()
        
        return [
            {"time": row["timestamp"], "temp": row["value1"], "humi": row["value2"]}
            for row in rows
        ]