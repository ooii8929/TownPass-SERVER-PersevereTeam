from enum import Enum, auto

class Language(Enum):
    CHINESE = auto()
    ENGLISH = auto()
# 待新增

class Preference(Enum):
    HISTORY = auto()
    NATURE = auto()
# 待新增

class Character(Enum):
    HAPPY = auto()
    DISGUST = auto()
# 待新增

class SectionStage(Enum):
    BEGINNING = auto()
    PROGRESS = auto()
    END = auto()
# 待新增

class QestionType(Enum):
    OPTION = auto()
    OPEN = auto()
    NEXT = auto()
# 待新增


class Bot:
    def __init__(self, language: Language, preference: Preference, age: int, character: Character, user_location: str,all_locations: list[str],visited_locations:list[str]):
        self.language = language
        self.preference = preference
        self.age = age
        self.character = character
        self.user_location = user_location
        self.all_locations = all_locations
        self.visited_locations = visited_locations


    def interact(self, sectionStage: SectionStage,inputText: str):
        # sectionStage: Beginning, inputText: ""
        res_data = {
            "content": "嗨，小朋友們！我們今天要來認識一個非常有趣的地方喔！...",
            "question": "好了，小朋友們，現在我們來玩個小遊戲吧！我有一個問題要問你們：大稻埕碼頭最有名的出口商品是什麼呢？",
            "type": "option",
             "options": [
                {"label": "A", "option": "糖果"},
                {"label": "B", "option": "茶葉"},
                {"label": "C", "option": "冰淇淋"}
             ],  
            "want_more": True
        }
        # sectionStage: Progress, inputText: "好了，小朋友們，現在我們來玩個小遊戲吧！我有一個問題要問你們：大稻埕碼頭最有名的出口商品是什麼呢？A. 糖果B. 茶葉C. 玩具，我覺得是A"
        # res_data = {
        #     "content": "你的回答正確喔！...",
        #     "question": "還想問你另外一個問題是...",
        #     "type": "open",
        #     "want_more": True
        # }
        # sectionStage: End, inputText: "我覺得大稻埕很好玩"
        # res_data = {
        #     "content": "感謝你的分享...",
        #     "question": "接下來想推薦給你一些值得去的其他地方...",
        #     "type": "next",
        #     "want_more": False
        # }
        return res_data
  