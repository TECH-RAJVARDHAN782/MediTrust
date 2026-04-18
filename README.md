# 🛡️ MediTrust: Decentralized Medicine Authentication

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC.svg)
![Groq](https://img.shields.io/badge/AI-Groq_Llama_3.3-f43f5e.svg)

**MedVerify** is an AI-powered, blockchain-simulated supply chain ledger designed to eliminate counterfeit medicines and bring absolute transparency to healthcare. 

It provides an end-to-end cryptographic trace from the manufacturing facility directly to the patient's hands, verifiable instantly via a simple QR scan.

---

## ✨ Key Features

* 🏭 **Manufacturer Portal (Admin):** Mint new medicine batches onto the immutable ledger, automatically generating secure QR codes for packaging.
* 🚚 **Transit Tracking:** Append geographic transit nodes to a medicine's blockchain trace as it moves through the supply chain.
* 📱 **Consumer Web App:** Patients can scan a medicine's QR code to instantly verify its authenticity, molecular composition, expiration date, and full transit history.
* 🤖 **MedBot Clinical AI:** An integrated AI assistant powered by **Llama 3.3 (via Groq)** that answers patient questions regarding medicine uses, compositions, and safety.
* 🔗 **Cryptographic Verification:** Every movement is hashed using `SHA-256`, linking blocks cryptographically to ensure the ledger cannot be tampered with.

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Database:** SQLite (Relational structure acting as the genesis ledger)
* **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS
* **Scanning & QR:** HTML5-QRCode, QRCode.js
* **Artificial Intelligence:** Groq API (Llama-3.3-70b-versatile)

---

## 📂 Project Structure

```text
medchain-project/
├── main.py              # The FastAPI backend, Blockchain logic, and AI endpoints
├── index.html           # The "Crystal Liquid Pro" Consumer App UI
├── admin.html           # The "PharmaPortal" Manufacturer UI
├── medchain.db          # Auto-generated SQLite database
├── .env                 # Environment variables (API Keys)
└── .gitignore           # Ignored files (venv, .env, .db)
