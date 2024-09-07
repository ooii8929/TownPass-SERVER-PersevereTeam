from flask import jsonify, request 
from ..db import db_connection
import uuid

def get_all_conversations(task_id):
  data = request.get_json()
  res_data = {
  	"task_id": task_id,
  	"user_uid": data['user_uid'],
  	"score": '20',
  	"conversations": [{
  	  "user_uid": "xxx",
  	  "last_uid": "init",
  	  "reply": '',
  	  "answer": ''
    }, {
  	  "category": 'system',
  	  "uid": '498801e1-2f50-4265-8ae1-8216972729d7',
	    "ts": "時間戳記",
	    "type": 'option',
  	  "content": '', # 任務簡介、景點簡介、問題回覆
	    "question": '',	  # 問題題目
	    "options": [{"label": 'A', "option": '選項 A'}, {"label": 'B', "option": '選項 B'}, {"label": 'C', "option": '選項 C'}] # 選擇題選項
	}, {
	  "category": 'user',
	  "uid": '498801e1-2f50-4265-8ae1-8216972729d7',
	  "last_uid": '86cf517c-8b66-45ab-a54e-1366bb6dc6a3', # 如果是這個任務的第一次互動就送 init，如果是回覆就送上一則訊息的 uuid
	  "reply": '', # 使用的回覆 (如果上一則是開放問題 或是使用者提問，總之是一段文字)
	  "answer": 'A' # 使用者選擇的答案 (如果上一題是選擇題)
	}, {
	  "category": 'system',
	  "uid": '498801e1-2f50-4265-8ae1-8216972729d7',
	  "ts": "時間戳記",
	  "type": 'open',
  	"content": '你剛剛回答得很好，OOXXOOXX...', # 任務簡介、景點簡介、問題回覆
	  "question": '你有沒有什麼想問的呢', 
	  "options": [],
	}, {
	  "category": 'user',
	  "uid": '498801e1-2f50-4265-8ae1-8216972729d7',
	  "last_uid": 'uuid asdferwer er',
	  "reply": '我沒有問題了', # 使用的回覆 (如果上一則是開放問題 或是使用者提問，總之是一段文字)
	  "answer": '' 
	}, {
	  "category": 'system',
	  "uid": '498801e1-2f50-4265-8ae1-8216972729d7',
	  "ts": "時間戳記",
	  "type": 'next',
  	"content": '', # 任務簡介、景點簡介、問題回覆
	  "question": '恭喜你完成了這個任務，接下來想去哪個任務呢？',	  
	  "options": [{"task_id": 4, "task_name": 'XXXX'}, {"task_id": 8, "task_name": 'YYYY'}, {"task_id": 8, "task_name": 'ZZZ'}]
	}]
  }
  return jsonify(res_data)


def create_conversation(task_id):
  data = request.get_json()
  uid = str(uuid.uuid4())
  res_data = {}
  if data['last_uid'] == 'init':
    res_data = {
      "task_id": task_id,
      "user_uid": data['user_uid'],
      "score": 10,
      "conversation": {
        "content": '歡迎來到大稻埕，這是簡介', # 任務簡介、景點簡介、問題回覆
        "question": '以下問題，哪一個答案正確呢',	  # 選擇題題目
        "options": [{"label": 'A', "option": '選項 A'}, {"label": 'B', "option": '選項 B'}, {"label": 'C', "option": '選項 C'}], # 選擇題選項
        "type": "option",	
        "uid": uid,
        "ts": "時間戳記"
      }
    }
  else:
    res_data = {
      "task_id": task_id,
      "user_uid": data['user_uid'],
      "score": 12,
      "conversation": {
        "content": '哇，你剛剛的答案答錯了唷，我們是 OOXX', # 任務簡介、景點簡介、問題回覆
        "question": "你還有什麼問題想要問呢",	  # 選擇題題目
        "options": [], # 選擇題選項
        "type": "open",	
        "uid": uid,
        "ts": "時間戳記"
      }
    } 
  return jsonify(res_data)