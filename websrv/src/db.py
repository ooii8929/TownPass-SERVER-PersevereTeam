import sqlite3

def db_connection():
  conn = None
  try:
    conn = sqlite3.connect('game.sqlite')
    conn.row_factory = sqlite3.Row
  except sqlite3.Error as e:
    print("Error while connecting to SQLite database:", e)
  return conn

# lang TEXT DEFAULT 'tw',
def create_tables():
    sql_statements = [ 
        """CREATE TABLE IF NOT EXISTS users (
                uid TEXT NOT NULL PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER DEFAULT 18,
                style TEXT NULL,
                lang TEXT DEFAULT 'tw'
        );""",
        """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, 
                task_id INTEGER NOT NULL,
                user_uid INTEGER NOT NULL,
                interactions Integer NOT NULL DEFAULT 0,
                status char(1) NOT NULL, 
                score INTEGER DEFAULT 0,
                begin_date TEXT NULL, 
                end_date TEXT NULL, 
                FOREIGN KEY (user_uid) REFERENCES users (uid)
        );""", """CREATE TABLE IF NOT EXISTS conversations (
                uid TEXT NOT NULL PRIMARY KEY, 
                task_id INTEGER NOT NULL,
                user_uid INTEGER NOT NULL,
                type TEXT NOT NULL DEFAULT 'open',
                category TEXT DEFAULT 'system',
                content TEXT NULL,
                question TEXT NULL,
                options TEXT NULL,
                last_uid TEXT NULL,
                reply TEXT NULL,
                answer TEXT NULL,
                option TEXT NULL,
                ts TEXT NOT NULL,
                FOREIGN KEY (user_uid) REFERENCES users (uid),
                FOREIGN KEY (task_id) REFERENCES tasks (id)
        );"""]

    # create a database connection
    try:
        with sqlite3.connect('game.sqlite') as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            
            conn.commit()
    except sqlite3.Error as e:
        print(e)
