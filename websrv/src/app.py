from flask import Flask 
from flask_cors import CORS
from .services.user_service import show_user, get_all_users, create_user
from .services.conversation_service import get_all_conversations, create_conversation

from .db import create_tables

create_tables()

app = Flask(__name__) 
CORS(app)


@app.route('/')
def hello_geek():
    return '<h1>Hello, Flask in Docker</h2>'
    
app.add_url_rule('/api/v1/user/<username>', 'show_user', show_user) 
app.add_url_rule('/api/v1/user', 'get_all_users', get_all_users)
app.add_url_rule('/api/v1/user', 'create_user', create_user, methods=['POST'])

app.add_url_rule('/api/v1/tasks/<task_id>/conversation', 'create_conversation', create_conversation, methods=['POST'])
app.add_url_rule('/api/v1/tasks/<task_id>/conversations', 'get_all_conversations', get_all_conversations, methods=['POST'])

if __name__ == "__main__": 
    app.run(debug=True)