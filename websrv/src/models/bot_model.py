from .rag_handler import rag_handler
from .defined_enum import Language, Style, SectionStage, type_dict, style_dict, language_dict
from enum import Enum, auto


class Bot:
    def __init__(self, language: Language, age: int, style: Style, user_location: str,all_locations: list[str],visited_locations:list[str]):
        self.language = language
        self.age = age
        self.style = style
        self.user_location = user_location
        self.all_locations = all_locations
        self.visited_locations = visited_locations


    def interact(self, sectionStage: SectionStage,inputText: str):
        # rag_handler(audience, language, location, character,stage, all_locations,visited_locations, userInput= "")
        audience = "幼稚園小朋友，不能用太艱深的詞彙"

        if self.age >= 30: 
            audience = "台灣歷史文化古蹟專家"
         #這邊之後要改成傳入age
        print("demo:",audience,style_dict[self.style],language_dict[self.language])

        res_data = rag_handler(
            audience=audience,
            language=language_dict[self.language],
            location=self.user_location,
            character=style_dict[self.style],
            stage=sectionStage,
            all_locations=self.all_locations,
            visited_locations=self.visited_locations,
            userInput=inputText
        )
        questionType = res_data["type"]
        print("type:",questionType)
        res_data["type"] = type_dict[questionType]
        # sectionStage: Beginning, inputText: ""
        # res_data = {
        #     "content": "嗨，小朋友們！我們今天要來認識一個非常有趣的地方喔！...",
        #     "question": "好了，小朋友們，現在我們來玩個小遊戲吧！我有一個問題要問你們：大稻埕碼頭最有名的出口商品是什麼呢？",
        #     "type": QestionType.OPTION,
        #     "options": [
        #         {"label": "A", "option": "糖果", "answer": True},
        #         {"label": "B", "option": "茶葉", "answer": False},
        #         {"label": "C", "option": "冰淇淋", "answer": False}
        #     ], 
        #     "want_more": True
        # }
        # sectionStage: Progress, inputText: "好了，小朋友們，現在我們來玩個小遊戲吧！我有一個問題要問你們：大稻埕碼頭最有名的出口商品是什麼呢？A. 糖果B. 茶葉C. 玩具，我覺得是A"
        # res_data = {
        #     "content": "你的回答正確喔！...",
        #     "question": "還想問你另外一個問題是...",
        #     "type": QestionType.OPEN,
        #     "want_more": True
        # }
        # sectionStage: End, inputText: "我覺得大稻埕很好玩"
        # res_data = {
        #     "content": "感謝你的分享...",
        #     "question": "接下來想推薦給你一些值得去的其他地方...",
        #     "type": QestionType.NEXT,
        #     "want_more": False
        # }
        return res_data
  