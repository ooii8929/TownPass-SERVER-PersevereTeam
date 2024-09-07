from flask import jsonify, request 
from ..db import db_connection
import uuid
import time
import json
from ..models.bot_model import Bot
from ..models.defined_enum import Language, Style, SectionStage, QestionType

def get_all_conversations(task_id):
  data = request.get_json()
  conn = db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM conversations WHERE task_id=? AND user_uid=? ", (task_id, data['user_uid'],)) 
  rows = cursor.fetchall()
  column_names = [description[0] for description in cursor.description]
  conversations = [dict(zip(column_names, row)) for row in rows]
  res = {
  	"task_id": task_id,
  	"user_uid": data['user_uid'],
  	"score": '20',
  	"conversations": conversations
  }
  return jsonify(res)

def create_conversation(task_id):
  data = request.get_json()
  uid = str(uuid.uuid4())
  system_uid = str(uuid.uuid4())
  ts = time.time()
  user_uid = data['user_uid']

  res_data = {}
  conn = db_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM users WHERE uid=?", (data['user_uid'],))
  user = cursor.fetchone()

  my_bot = Bot(
      language=Language[user['lang'].upper()],
      age=user['age'],
      style=Style[user['style'].upper()],
      user_location='永樂市場',
      all_locations = ["大稻埕碼頭", "龍山寺", "中正紀念堂", "九份老街","十分瀑布", "松山文創園區", "北投溫泉", "淡水老街"],
      visited_locations = ["大稻埕碼頭", "龍山寺", "淡水老街"]
    )

  if data['last_uid'] == 'init':
    cursor.execute("INSERT INTO tasks (task_id, user_uid, interactions, status) VALUES (?, ?, ?, ?)", (task_id, user_uid, 1, 'A'))
    cursor.execute("INSERT INTO conversations (uid, task_id, user_uid, type, category, ts) VALUES (?, ?, ?, ?, ?, ?)", (uid, task_id, user_uid, 'init', 'user', ts))
    # call model to get next conversation
    ai_res = my_bot.interact(SectionStage.BEGINNING, "")
    options = ai_res["options"]
    # insert system conversation to db
    type = ai_res["type"].name.lower()
    cursor.execute("INSERT INTO conversations (uid, task_id, user_uid, type, category, content, question, options, ts) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (system_uid, task_id, user_uid, type, 'system', ai_res["content"], ai_res["question"], json.dumps(options, separators=(',', ':')), ts)) 
    res_data = {
      "task_id": task_id,
      "user_uid": data['user_uid'],
      "score": 0,
      "conversation": {
        "content": ai_res['content'], # 任務簡介、景點簡介、問題回覆
        "question": ai_res['question'],	  # 選擇題題目
        "options": ai_res['options'],
        "type": type,	
        "uid": uid,
        "ts": ts
      }
    }
  else:
    cursor.execute("SELECT * FROM conversations WHERE uid=?", (data['last_uid'],))
    last_conversation = cursor.fetchone()
    # get option
    cursor.execute("INSERT INTO conversations (uid, task_id, user_uid, type, category, reply, answer, option, ts) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (uid, task_id, user_uid, 'user', 'user', data['reply'], data['answer'], "option", ts)) 
    # call model to get next conversation
    ai_res = my_bot.interact(SectionStage.PROGRESS, f"這是提問: {last_conversation['question']}, 這是答案: {data['reply']}")
    print("********", ai_res)
    # insert system conversation to db
    options = [] if ai_res['type'] == QestionType.OPEN else ai_res["options"]
    # insert system conversation to db 
    type = ai_res["type"].name.lower()
    cursor.execute("INSERT INTO conversations (uid, task_id, user_uid, type, category, content, question, options, ts) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (system_uid, task_id, user_uid, type, 'system', ai_res['content'], ai_res["question"], json.dumps(options, separators=(',', ':')), ts))  
    res_data = {
      "task_id": task_id,
      "user_uid": data['user_uid'],
      "score": 12,
      "conversation": {
        "content": ai_res['content'], # 任務簡介、景點簡介、問題回覆
        "question": ai_res['question'],	  # 選擇題題目
        "options": options, # 選擇題選項
        "type": type,	
        "uid": uid,
        "ts": ts
      }
    } 
  
  conn.commit()
  conn.close()
  return jsonify(res_data)