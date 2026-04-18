from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import hashlib
import json
import time
import os
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()
AI_KEY = os.getenv("PRIMARY_AI_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FIXED: Pointing strictly to one database
DB_PATH = os.path.join(BASE_DIR, "medchain.db")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
ADMIN_FILE = os.path.join(BASE_DIR, "admin.html")

app = FastAPI(title="MedVerify Blockchain API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. BLOCKCHAIN CRYPTOGRAPHY
# ==========================================
class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash="0" * 64, data="Genesis Block")

    def create_block(self, previous_hash, data):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(time.time()),
            "data": data,
            "previous_hash": previous_hash
        }
        encoded_block = json.dumps(block, sort_keys=True).encode()
        block["hash"] = hashlib.sha256(encoded_block).hexdigest()
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

# ==========================================
# 2. DATABASE SEEDING
# ==========================================
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            barcode TEXT PRIMARY KEY,
            name TEXT,
            composition TEXT,
            manufacturer TEXT,
            med_use TEXT,
            expiry TEXT,
            isVerified TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supply_history (
            med_id TEXT,
            action TEXT,
            location TEXT,
            date TEXT
        )
    """)

    live_data = [
        ("8901000000001","Dolo 650","Paracetamol 650mg","Micro Labs","Fever and pain relief","2026-12-01","true"),
        ("8901000000002","Crocin","Paracetamol 500mg","GSK","Fever and mild pain","2026-10-01","true"),
        ("8901000000003","Calpol","Paracetamol 500mg","GSK","Fever and headache","2027-01-01","true"),
        ("8901000000004","Combiflam","Ibuprofen + Paracetamol","Sanofi","Pain relief and inflammation","2026-09-01","true"),
        ("8901000000005","Augmentin 625","Amoxicillin + Clavulanic Acid","GSK","Bacterial infections","2026-11-01","true"),
        ("8901000000006","Azithromycin","Azithromycin 500mg","Cipla","Bacterial infections","2026-08-01","true"),
        ("8901000000007","Amoxicillin","Amoxicillin 500mg","Sun Pharma","Bacterial infections","2027-02-01","true"),
        ("8901000000008","Cetirizine","Cetirizine 10mg","Dr. Reddy's","Allergy relief","2026-07-01","true"),
        ("8901000000009","Levocetirizine","Levocetirizine 5mg","Cipla","Allergic rhinitis","2026-06-01","true"),
        ("8901000000010","Benadryl","Diphenhydramine","Johnson & Johnson","Cough and allergy","2026-05-01","true"),
        ("8901000000011","Pantoprazole","Pantoprazole 40mg","Sun Pharma","Acidity and GERD","2027-03-01","true"),
        ("8901000000012","Digene","Magnesium Hydroxide + Aluminium Hydroxide","Abbott","Acidity relief","2026-09-01","true"),
        ("8901000000013","Rantac","Ranitidine","JB Chemicals","Acidity and ulcers","2026-04-01","true"),
        ("8901000000014","ORS","Oral Rehydration Salts","Dabur","Dehydration treatment","2027-01-01","true"),
        ("8901000000015","Vitamin D3","Cholecalciferol","Uprise","Bone health","2027-05-01","true"),
        ("8901000000016","Zinc Tablets","Zinc Sulphate","Himalaya","Immunity support","2026-08-01","true"),
        ("8901000000017","Metformin","Metformin 500mg","Sun Pharma","Diabetes management","2027-06-01","true"),
        ("8901000000018","Amlodipine","Amlodipine 5mg","Cipla","Blood pressure control","2027-02-01","true"),
        ("8901000000019","Atorvastatin","Atorvastatin 10mg","Dr. Reddy's","Cholesterol control","2027-04-01","true"),
        ("8901000000020","Insulin","Human Insulin","Novo Nordisk","Diabetes treatment","2026-12-01","true"),
        ("8901000000021","Paracetamol Syrup","Paracetamol 250mg/5ml","Cipla","Fever in children","2026-10-01","true"),
        ("8901000000022","Ibuprofen","Ibuprofen 400mg","Abbott","Pain and inflammation","2026-11-01","true"),
        ("8901000000023","Omeprazole","Omeprazole 20mg","Dr. Reddy's","Acidity and ulcers","2027-03-01","true"),
        ("8901000000024","Cough Syrup","Dextromethorphan","Benadryl","Dry cough relief","2026-06-01","true")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO medicines
        (barcode, name, composition, manufacturer, med_use, expiry, isVerified)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, live_data)

    today = date.today().strftime("%Y-%m-%d")
    for med in live_data:
        # FORCED STRING CONVERSION: This guarantees it can never be a tuple!
        safe_barcode = str(med) 
        
        cursor.execute("SELECT count(*) FROM supply_history WHERE med_id = ?", (safe_barcode,))
        if cursor.fetchone() == 0:
            cursor.execute("""
                INSERT INTO supply_history (med_id, action, location, date)
                VALUES (?, ?, ?, ?)
            """, (safe_barcode, "Minted & Packaged", "Factory Import", today))

    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. FASTAPI ROUTES
# ==========================================
@app.get("/")
def serve_frontend():
    return FileResponse(INDEX_FILE)

@app.get("/admin")
def serve_admin():
    return FileResponse(ADMIN_FILE)

@app.get("/api/scan/{med_id}")
def scan_medicine(med_id: str):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medicines WHERE barcode = ?", (med_id,))
    med_row = cursor.fetchone()

    if not med_row:
        conn.close()
        return {"success": False, "message": f"Product ID [{med_id}] not found in ledger. Counterfeit risk."}

    med_data = dict(med_row)

    cursor.execute("""
        SELECT action, location, date
        FROM supply_history
        WHERE med_id = ?
        ORDER BY rowid ASC
    """, (med_id,))
    history_data = cursor.fetchall()
    conn.close()

    # FIXED: Instantiating a fresh blockchain per scan to prevent infinite memory growth
    local_chain = SimpleBlockchain()
    trace = []
    
    for step in history_data:
        last_block = local_chain.get_last_block()
        data_string = f"{med_id}-{step['action']}-{step['location']}-{step['date']}"
        new_block = local_chain.create_block(previous_hash=last_block["hash"], data=data_string)

        trace.append({
            "action": step["action"],
            "location": step["location"],
            "date": step["date"],
            "hash": new_block["hash"],
            "prev_hash": new_block["previous_hash"]
        })

    return {"success": True, "medicine": med_data, "trace": trace}

class MintData(BaseModel):
    barcode: str
    name: str
    composition: str
    manufacturer: str
    med_use: str
    expiry: str
    location: str

@app.post("/api/mint")
def mint_medicine(data: MintData):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO medicines
            (barcode, name, composition, manufacturer, med_use, expiry, isVerified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data.barcode, data.name, data.composition, data.manufacturer, data.med_use, data.expiry, "true"))

        today = date.today().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO supply_history (med_id, action, location, date)
            VALUES (?, ?, ?, ?)
        """, (data.barcode, "Minted & Packaged", data.location, today))

        conn.commit()
        return {"success": True, "message": f"Successfully registered {data.name} to ledger!"}
    except sqlite3.IntegrityError:
        return {"success": False, "message": f"Error: Barcode '{data.barcode}' already exists."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()

class TransitData(BaseModel):
    barcode: str
    action: str
    location: str

@app.post("/api/transit")
def update_transit(data: TransitData):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM medicines WHERE barcode = ?", (data.barcode,))
        med = cursor.fetchone()
        
        if not med:
            return {"success": False, "message": f"Blockchain Error: Barcode '{data.barcode}' not found in Genesis Ledger."}

        today = date.today().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO supply_history (med_id, action, location, date)
            VALUES (?, ?, ?, ?)
        """, (data.barcode, data.action, data.location, today))

        conn.commit()
        return {"success": True, "message": f"Block appended! {med['name']} updated to: {data.location}"}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()

@app.get("/api/medicines")
def get_all_medicines():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT barcode, name, manufacturer, expiry FROM medicines ORDER BY rowid DESC")
        rows = cursor.fetchall()
        medicines = [dict(r) for r in rows]
        return {"success": True, "medicines": medicines}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()

# ==========================================
# 4. CHATBOT ROUTE
# ==========================================
class ChatMessage(BaseModel):
    message: str

@app.post("/api/chat")
def handle_chat(chat: ChatMessage):
    user_message = chat.message

    if not AI_KEY:
        return {"success": False, "reply": "❌ Error: Python cannot find the API key. Check your .env file."}

    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AI_KEY.strip()}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are MedBot, a helpful assistant. Keep answers short."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        data = response.json()

        if isinstance(data, dict) and "error" in data:
            err = data["error"]
            err_msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
            return {"success": False, "reply": f"⚠️ Groq Error: {err_msg}"}

        if isinstance(data, dict) and "choices" in data and isinstance(data["choices"], list) and data["choices"]:
            bot_reply = data["choices"][0]["message"]["content"]
            return {"success": True, "reply": bot_reply}

        return {"success": False, "reply": "⚠️ Received unexpected data format from Groq."}

    except Exception as e:
        return {"success": False, "reply": f"💻 Python crashed! Terminal says: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
