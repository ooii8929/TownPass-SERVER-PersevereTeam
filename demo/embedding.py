
"""## Embedding Model"""

from langchain_openai import OpenAIEmbeddings

# embebbing model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

text = "This is a test document."

data = embeddings.embed_query(text)

print(f"embedding data: {len(data)}")
print(data[:5])