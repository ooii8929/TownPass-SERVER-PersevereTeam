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

def rag_handler(audience, language, location, character,stage, all_locations,visited_locations, userInput= ""):
    isEnd = False
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
    audience_toml = ""
    if stage == "beginning":
        print("run beginning")
        audience_toml = f"../../../ai_handlers/settings/introduction.toml"
    else:
        print("run not beginning")
        if stage == "end":
            isEnd = True
        audience_toml = f"../../../ai_handlers/settings/feedback.toml"

    # Load prompt template
    template_data = toml.load(audience_toml)
    template = template_data['template']['content']
    prompt = ChatPromptTemplate.from_template(template=template)

    # Helper function to format documents
    def format_docs(docs):
        return "\n------------------\n".join(doc.page_content for doc in docs)
    if userInput:
        tmp = userInput
    else:
        userInput =""
        tmp = location


    # Set up the chain
    chain = (
        {
            "context": lambda x: format_docs(retriever.get_relevant_documents(x["tmp"])),
            "audience": lambda x: x["audience"],
            "language": lambda x: x["language"],
            "userInput": lambda x: x["userInput"],
            "isEnd": lambda x: x["isEnd"],
            "location": lambda x: ", ".join(["大稻埕", "永樂布市", "霞海城隍廟", "迪化街中街", "大稻埕碼頭", "波麗路西餐廳"]),
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
        "character": character,
        "isEnd": isEnd,
        "tmp": tmp
    })

    return result

# Example usage:
result = rag_handler(
    audience="kid",
    language="Korean",
    location="大稻埕",
    character="disgust",
    stage="end",userInput = "大家好！我是你們今天超級開心的導覽員！我們現在要一起去探險一個超酷的地方喔！你們準備好了嗎？ 讓我們一起來認識大稻埕碼頭吧！這個地方可是台北市以前超級重要的港口呢！想像一下，很久很久以前，在1858年的時候，這裡開始變得很熱鬧。為什麼呢？因為那時候台灣的港口開放了，可以跟其他國家做生意啦！ 然後呢，在1866年，有一個來自美國的叔叔，他叫陶德，在大稻埕開了一個茶葉工廠。哇！從那時候開始，這裡就變得更熱鬧了！大家都來這裡買賣東西，特別是茶葉和樟腦。樟腦就是那種有香香味道的東西喔！ 大稻埕碼頭變得超級厲害，連附近的桃園、新竹的東西都會先送到這裡來。但是後來，河裡的沙子越來越多，大船就不能來了。再加上日本人把基隆港弄得更好，所以大稻埕碼頭慢慢就不像以前那麼熱鬧了。 不過，現在我們還是可以在這裡看到一艘很特別的小船喔！它叫做'唐山帆船'，雖然比真的船小很多，但是它可以告訴我們以前這裡有多麼熱鬧呢！ 好啦！現在我要考考你們喔！來回答一個小問題： 大稻埕碼頭最有名的出口商品是什麼呢？ A. 玩具 B. 茶葉和樟腦 C. 冰淇淋 你們覺得是哪一個呢？記得舉手回答喔！ 我覺得答案是A。")
pprint(result)

# userInput = "大家好！我是你們今天超級開心的導覽員！我們現在要一起去探險一個超酷的地方喔！你們準備好了嗎？ 讓我們一起來認識大稻埕碼頭吧！這個地方可是台北市以前超級重要的港口呢！想像一下，很久很久以前，在1858年的時候，這裡開始變得很熱鬧。為什麼呢？因為那時候台灣的港口開放了，可以跟其他國家做生意啦！ 然後呢，在1866年，有一個來自美國的叔叔，他叫陶德，在大稻埕開了一個茶葉工廠。哇！從那時候開始，這裡就變得更熱鬧了！大家都來這裡買賣東西，特別是茶葉和樟腦。樟腦就是那種有香香味道的東西喔！ 大稻埕碼頭變得超級厲害，連附近的桃園、新竹的東西都會先送到這裡來。但是後來，河裡的沙子越來越多，大船就不能來了。再加上日本人把基隆港弄得更好，所以大稻埕碼頭慢慢就不像以前那麼熱鬧了。 不過，現在我們還是可以在這裡看到一艘很特別的小船喔！它叫做'唐山帆船'，雖然比真的船小很多，但是它可以告訴我們以前這裡有多麼熱鬧呢！ 好啦！現在我要考考你們喔！來回答一個小問題： 大稻埕碼頭最有名的出口商品是什麼呢？ A. 玩具 B. 茶葉和樟腦 C. 冰淇淋 你們覺得是哪一個呢？記得舉手回答喔！ 我覺得答案是A"