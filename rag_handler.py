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


"""## Input"""
# kid, teen, adult
audience = "kid"
question = "有哪些畫是關於愛情的"


"""## Setup"""

# 載入 .env 檔案中的環境變數
load_dotenv()

# 初始化 Chroma 向量数据库
persist_directory = "db"
vectordb = Chroma(persist_directory=persist_directory)

"""## RAG Chain"""

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

"""### Retriever"""

retriever = vectordb.as_retriever()

"""### Prompt"""

# 根據 audience 拿到不同的 toml，读取 template.toml 文件的内容
audience_toml = f"./ai_handlers/settings/audience/{audience}_prompt.toml"
template_data = toml.load(audience_toml)
template = template_data['template']['content']

prompt = ChatPromptTemplate.from_template(template=template)

def format_docs(docs):
    return "\n------------------\n".join(doc.page_content for doc in docs)

chain = ({"context": retriever | RunnableLambda(format_docs),
          "question": RunnablePassthrough()}
         | prompt
         | model
         | StrOutputParser())

result = chain.invoke(question)
pprint(result)
