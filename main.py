# -*- coding: utf-8 -*-
import os
from rich.pretty import pprint
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnableLambda, RunnableSequence, RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import json
from langchain.document_loaders import JSONLoader
import toml


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

file_path = "./crawler/all_artwork_info.json"
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

persist_directory = "db"
vectordb = Chroma.from_documents(text_chunks,
                                 embedding=embeddings,
                                 persist_directory=persist_directory)

print(f"total documents: {len(vectordb.get()['ids'])}")



"""## RAG Chain"""

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

"""### Retriever"""

retriever = vectordb.as_retriever()

"""### Prompt"""

# 读取 template.toml 文件的内容
template_data = toml.load('./ai_handlers/settings/overall_prompt.toml')
template = template_data['template']['content']

prompt = ChatPromptTemplate.from_template(template=template)

def format_docs(docs):
    return "\n------------------\n".join(doc.page_content for doc in docs)

chain = ({"context": retriever | RunnableLambda(format_docs),
          "question": RunnablePassthrough()}
         | prompt
         | model
         | StrOutputParser())

result = chain.invoke("有哪些畫是關於愛情的")
pprint(result)
