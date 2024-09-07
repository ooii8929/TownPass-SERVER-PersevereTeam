import chromadb
chroma_client = chromadb.Client()

persist_directory = "../db"
# 重新打開客戶端和集合
chroma_client = chromadb.PersistentClient(path=persist_directory)
collection = chroma_client.get_collection(name="my_artwork_collection")

print(f"重新打開後，集合中有 {collection.count()} 個文檔")

# 查看集合中的所有文檔
all_docs = collection.get()
print("\n集合中的所有文檔:")
for doc, id in zip(all_docs['documents'], all_docs['ids']):
    print(f"ID: {id}, 內容: {doc}")


# collection.add(
#     documents=[
#         "貓咪喜歡在陽光下打盹",
#         "狗狗喜歡追逐飛盤",
#         "倉鼠喜歡在輪子上奔跑",
#         "鸚鵡能模仿人類的說話",
#         "金魚有3秒鐘的記憶"
#     ],
#     ids=["cat_1", "dog_1", "hamster_1", "parrot_1", "goldfish_1"]
# )
