from flask import jsonify, request 
from ..db import db_connection
import uuid

def get_all_users():
    conn = db_connection()
    cursor = conn.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    # 將每個 row 轉換為字典，鍵為 column_names
    users = [dict(zip(column_names, row)) for row in rows]
    conn.close()
    return jsonify(users)

def create_user():
    data = request.get_json()
    uid = str(uuid.uuid4())
    print(uid)
    conn = db_connection()
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO users (uid, name, age, style) VALUES (?, ?, ?, ?)", (uid, data['name'], data['age'], data['style']))
    conn.commit()  
    return jsonify({"uid": uid, "name": data['name']})

def show_user(username): 
    # Greet the user 
    return jsonify( {"user": f'Hello {username} !'})
