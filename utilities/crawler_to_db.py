from rich.pretty import pprint
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from pathlib import Path
import json

# Load environment variables
load_dotenv()

# Load JSON data
file_path = "../crawler/demo.json"
data = json.loads(Path(file_path).read_text())
pprint(data)

# Use JSONLoader
loader = JSONLoader(
    file_path=file_path,
    jq_schema='.',
    text_content=False)

docs = loader.load()
print(f"docs: {len(docs)}")

# Initialize the RecursiveJsonSplitter
splitter = RecursiveJsonSplitter(
    max_chunk_size=100,  # 減小最大 chunk 大小
    min_chunk_size=20,   # 設置最小 chunk 大小
)

# Process each document
all_chunks = []
for doc in docs:
    # Convert the document's page_content (which is a string) back to a JSON object
    json_content = json.loads(doc.page_content)
    # Split the JSON content
    chunks = splitter.split_json(json_data=json_content)
    all_chunks.extend(chunks)

print(f"text chunks: {len(all_chunks)}")
pprint(all_chunks[0])

# Set up embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
collection_name = "my_artwork_collection"

# Create Chroma vectorstore
persist_directory = "../db"
vectordb = Chroma.from_texts(
    texts=[json.dumps(chunk) for chunk in all_chunks],
    embedding=embeddings,
    persist_directory=persist_directory,
    collection_name=collection_name
)

print(f"total documents: {len(vectordb.get()['ids'])}")