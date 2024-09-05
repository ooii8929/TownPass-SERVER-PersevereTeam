# 如何完成一次專案上線
## 1. Crawler 拿到網站資料
## 2. 前往 utilities 使用 crawler_to_db 在資料塞入 local chroma 內
## 3. 使用 main.py 跑 RAG 拿到回應
### RAG Setup
1. 申請 OPENAI_API_KEY, LANGCHAIN, LangSmith
2. 填入 .env.example 並修改為 .env
2. Run below code
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
```
python rag_handler.py
```
## Repo infra
- demo -> 幫助學習 RAG 各個 Components
- lang-smith-setup -> 測試 LandSmith 安裝
- data -> 存 crawler 的資料
- ai_handlers -> 存 prompt
