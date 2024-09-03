from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

llm = ChatOpenAI()
llm.invoke("Hello, world!")