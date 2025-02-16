# 🎟️ Reservation API

This is a **FastAPI-based Reservation API** for a movie theater/event seat booking system.  
It supports listing events, checking seat availability, reserving seats, and canceling reservations while ensuring **concurrency control**.

---

## 🚀 Features
✅ List available events and seats  
✅ Reserve a seat with **concurrency handling**  
✅ Cancel reservations  
✅ Prevents double booking  
✅ SQLite database  

---

## 🛠️ Setup Instructions

### **1️⃣ Install Dependencies**
First, create a virtual environment (recommended):
```sh
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
Then, install the required dependencies:
```sh
pip install fastapi uvicorn sqlalchemy sqlite3 pydantic
```

### **2️⃣ Initialize the Database**
Run the following to create tables and insert dummy data:
```sh
python init_db.py
```

### **3️⃣ Run the API**
Start the FastAPI server:
```sh
uvicorn main:app --reload
```
The API will be available at:  
📌 **Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

---

## 🔗 API Endpoints

### **1️⃣ List All Events**
**GET** `/events`  
📌 Returns a list of events with available seating.  
✅ Example Response:
```json
[
  {
    "id": 1,
    "name": "Avengers Movie",
    "total_seats": 10,
    "available_seats": 5
  }
]
```

---

### **2️⃣ Get Seats for an Event**
**GET** `/events/{event_id}/seats`  
📌 Lists all seats and their reservation status.  
✅ Example Response:
```json
[
  {
    "id": 1,
    "seat_number": "A1",
    "is_reserved": false
  }
]
```

❌ **Error Responses:**
```json
{ "detail": "Event not found" }
```

---

### **3️⃣ Reserve a Seat**
**POST** `/events/{event_id}/reservations?seat_number=A1&user_name=John`  
📌 Reserves a seat for a user.  
✅ **Successful Response:**
```json
{
  "message": "Seat reserved successfully!",
  "reservation_id": 5
}
```
❌ **Error Responses:**
```json
{ "detail": "Event not found" }
{ "detail": "Seat not found" }
{ "detail": "Seat already reserved" }
```

---

### **4️⃣ Cancel a Reservation**
**DELETE** `/reservations/{reservation_id}`  
📌 Cancels a reservation.  
✅ Example Response:
```json
{
  "message": "Reservation canceled successfully!"
}
```
❌ **Error Responses:**
```json
{ "detail": "Reservation not found" }
```

---

---

## 🔬 Running Concurrency Test
To test multiple users booking the same seat:
```sh
python test_concurrency.py
```
Expected Output:
```json
{"message": "Seat reserved successfully!", "reservation_id": 4}
{"detail": "Seat already reserved"}
{"detail": "Seat already reserved"}
```
✅ Ensures that **only one** seat can be reserved!

---

## 📂 Project Structure
```
reservation_api/
│── main.py           # FastAPI application
│── database.py       # Database models & setup
│── init_db.py        # Creates dummy data
│── test_concurrency.py # Simulates multiple users booking a seat
│── README.md         # Documentation
│── venv/             # (Optional) Virtual environment
│── reservations.db   # SQLite database (auto-created)
```