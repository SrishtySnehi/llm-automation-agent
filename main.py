from fastapi import FastAPI, HTTPException
from database import get_db_connection

app = FastAPI()

# API endpoint to get all users
@app.get("/users")
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return {"users": [dict(user) for user in users]}

# API endpoint to add a new user
@app.post("/users")
def create_user(name: str, email: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        user_id = cursor.lastrowid
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    
    conn.close()
    return {"id": user_id, "name": name, "email": email}