import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents=[
        "貓咪喜歡在陽光下打盹",
        "狗狗喜歡追逐飛盤",
        "倉鼠喜歡在輪子上奔跑",
        "鸚鵡能模仿人類的說話",
        "金魚有3秒鐘的記憶"
    ],
    ids=["cat_1", "dog_1", "hamster_1", "parrot_1", "goldfish_1"]
)

# 查詢示例
results = collection.query(
    query_texts=["寵物的有趣行為"],
    n_results=3
)

print(results)