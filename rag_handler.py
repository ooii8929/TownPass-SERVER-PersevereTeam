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
from langchain_chroma import Chroma
import json
from langchain.document_loaders import JSONLoader
import toml


"""## Input"""
# kid, teen, adult
audience = "kid"
# language = "繁體中文"
userInput = "大家好！我是你們今天超級開心的導覽員！我們現在要一起去探險一個超酷的地方喔！你們準備好了嗎？ 讓我們一起來認識大稻埕碼頭吧！這個地方可是台北市以前超級重要的港口呢！想像一下，很久很久以前，在1858年的時候，這裡開始變得很熱鬧。為什麼呢？因為那時候台灣的港口開放了，可以跟其他國家做生意啦！ 然後呢，在1866年，有一個來自美國的叔叔，他叫陶德，在大稻埕開了一個茶葉工廠。哇！從那時候開始，這裡就變得更熱鬧了！大家都來這裡買賣東西，特別是茶葉和樟腦。樟腦就是那種有香香味道的東西喔！ 大稻埕碼頭變得超級厲害，連附近的桃園、新竹的東西都會先送到這裡來。但是後來，河裡的沙子越來越多，大船就不能來了。再加上日本人把基隆港弄得更好，所以大稻埕碼頭慢慢就不像以前那麼熱鬧了。 不過，現在我們還是可以在這裡看到一艘很特別的小船喔！它叫做'唐山帆船'，雖然比真的船小很多，但是它可以告訴我們以前這裡有多麼熱鬧呢！ 好啦！現在我要考考你們喔！來回答一個小問題： 大稻埕碼頭最有名的出口商品是什麼呢？ A. 玩具 B. 茶葉和樟腦 C. 冰淇淋 你們覺得是哪一個呢？記得舉手回答喔！ 我覺得答案是A"


"""## Setup"""

# 載入 .env 檔案中的環境變數
load_dotenv()

# 初始化 Chroma 向量数据库
persist_directory = "db"
vectordb = Chroma(persist_directory=persist_directory)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="demo",
    embedding_function=embeddings,
    persist_directory=persist_directory,  # Where to save data locally, remove if not neccesary
)
"""## RAG Chain"""

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

"""### Retriever"""

retriever = vector_store.as_retriever()

"""### Prompt"""

# 根據 audience 拿到不同的 toml，读取 template.toml 文件的内容
audience_toml = f"./ai_handlers/settings/demo.toml"
template_data = toml.load(audience_toml)
template = template_data['template']['content']

prompt = ChatPromptTemplate.from_template(template=template)

def format_docs(docs):
    return "\n------------------\n".join(doc.page_content for doc in docs)

chain = ({"context": retriever | RunnableLambda(format_docs),
        #   "language": RunnablePassthrough(),
          "userInput": RunnablePassthrough()
          }
         | prompt
         | model
         | StrOutputParser())

# result = chain.invoke(f"{language} {userInput}")
result = chain.invoke(userInput)
pprint(result)
