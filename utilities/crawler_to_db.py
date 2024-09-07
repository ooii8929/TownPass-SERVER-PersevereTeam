# -*- coding: utf-8 -*-
from rich.pretty import pprint
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from langchain.document_loaders import JSONLoader



"""## Setup"""

# 載入 .env 檔案中的環境變數
load_dotenv()

"""## Vectorstore """

"""### PDF Loader """
# file_path = "./data/pdf/16th-century-western-artists.pdf"
# loader = PyPDFLoader(file_path)
# docs = loader.load()
# print(f"docs: {len(docs)}")

"""### JSON Loader """

file_path = "../crawler/artwork_info.json"
loader = JSONLoader(file_path=file_path, jq_schema='.', text_content=False)
docs = loader.load()
print(f"docs: {len(docs)}")

"""### Splitter """

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
text_chunks = text_splitter.split_documents(docs)

print (f"text chunks: {len(text_chunks)}")

pprint(text_chunks[1])

# embebbing model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
collection_name = "my_artwork_collection"  # Specify a collection name

persist_directory = "db"
vectordb = Chroma.from_documents(text_chunks,
                                 embedding=embeddings,
                                 persist_directory=persist_directory,collection_name=collection_name)

print(f"total documents: {len(vectordb.get()['ids'])}")

