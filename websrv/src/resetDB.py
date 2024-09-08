from db import db_connection

conn = db_connection()
cursor = conn.cursor()
cursor.execute("DELETE FROM conversations")
conn.commit()
conn.close()
