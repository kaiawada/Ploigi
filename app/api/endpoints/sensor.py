from fastapi import APIRouter
import sqlite3

router = APIRouter()
DB_FILE = "sensor_data.db"

@router.get("/history")
async def get_history():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row  # ラベル貼りの工場設定
        cursor = conn.cursor()
        
        # 最新50件を取得（読み出し SELECT）
        cursor.execute(
            "SELECT timestamp, value1, value2 FROM data_logs WHERE type = 'sensor' ORDER BY id DESC LIMIT 50"
        )
        rows = cursor.fetchall()
        
        # 内部の棚の名前(value1等)を、ブラウザ向けの名前(temp等)にマッピング
        return [
            {"time": row["timestamp"], "temp": row["value1"], "humi": row["value2"]}
            for row in rows
        ]