import sqlite3
import os

def inspect_chroma_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 獲取所有表格名稱
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='embedding_fulltext_search';")
    tables = cursor.fetchall()
    
    print("Chroma 數據庫中的表格:")
    for table in tables:
        print(f"- {table[0]}")
        # 獲取每個表格的結構
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")
        
        # 顯示每個表格的前幾行數據
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
        rows = cursor.fetchall()
        if rows:
            print(f"  示例數據:")
            for row in rows:
                print(f"    {row}")
        
        # 獲取表格中的總記錄數
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        total_rows = cursor.fetchone()[0]
        print(f"  總記錄數: {total_rows}")
        print()

    conn.close()

# 指定 Chroma 數據庫的路徑
db_path = "./db/chroma.sqlite3"

# 檢查 SQLite 數據庫內容
if os.path.exists(db_path):
    inspect_chroma_sqlite(db_path)
else:
    print(f"數據庫文件 {db_path} 不存在")

print("\nChroma 文件結構說明:")
print("1. chroma.sqlite3: 主數據庫文件，存儲元數據和索引信息")
print("2. d54d3188-5a5a-4a40-b637-ebd47eb803e6/: 向量數據目錄")
print("   - data_level0.bin: 存儲實際的向量數據")
print("   - header.bin: 向量索引的頭信息")
print("   - length.bin: 存儲向量長度信息")
print("   - link_lists.bin: 用於高效近似最近鄰搜索的鏈接結構")