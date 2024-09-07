import os
from rich.pretty import pprint
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import toml

def rag_handler(audience, language, location, character, userInput, isEnd, wantMore=False):
    # Load environment variables
    load_dotenv()

    # Initialize Chroma vector database
    persist_directory = "../../../db"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(
        collection_name="my_artwork_collection",
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )

    # Initialize OpenAI model
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Set up retriever
    retriever = vector_store.as_retriever()

    # Load prompt template
    audience_toml = f"../../../ai_handlers/settings/demo.toml"
    template_data = toml.load(audience_toml)
    template = template_data['template']['content']
    prompt = ChatPromptTemplate.from_template(template=template)

    # Helper function to format documents
    def format_docs(docs):
        return "\n------------------\n".join(doc.page_content for doc in docs)

    # Set up the chain
    chain = (
        {
            "context": lambda x: format_docs(retriever.get_relevant_documents(x["userInput"])),
            "audience": lambda x: x["audience"],
            "language": lambda x: x["language"],
            "userInput": lambda x: x["userInput"],
            "isEnd": lambda x: x["isEnd"],
            "output": lambda x: x.get("output", ""),
            "interaction": lambda x: x.get("interaction", ""),
            "location": lambda x: ", ".join(["大稻埕", "永樂布市", "霞海城隍廟", "迪化街中街", "大稻埕碼頭", "波麗路西餐廳"]),
            "wantMore": lambda x: x.get("wantMore", False),
            "character": lambda x: x.get("character", False),
        }
        | prompt
        | model
        | JsonOutputParser()
    )

    # Invoke the chain with the provided inputs
    result = chain.invoke({
        "audience": audience,
        "language": language,
        "userInput": userInput,
        "isEnd": isEnd,
        "wantMore": wantMore,
        "character": character,
    })

    return result

# Example usage:
result = rag_handler(
    audience="kid",
    language="Korean",
    location="大稻埕",
    character="disgust",
    userInput="大家好！我是你們今天超級開心的導覽員！...",
    isEnd=False,
    wantMore=False
)
pprint(result)