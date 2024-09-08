from enum import Enum, auto

class Language(Enum):
    TW = auto()
    EN = auto()
    JP = auto()
# 待新增

class Style(Enum):
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

type_dict = {
    "引導提問":QestionType.OPEN,
    "問單選選擇題":QestionType.OPTION,
    "問開放式問題":QestionType.OPEN,
    "推薦下個景點":QestionType.NEXT
}

style_dict = {
   Style.HAPPY:"一個開朗有趣的，講話很多驚嘆號的",
   Style.DISGUST:"一個厭世，講話很嗆的，不是很開心，負面的，悲觀的，不耐煩的，講話很多...的，很喜歡講隨便拉",
}

language_dict = {
   Language.TW:"繁體中文",
   Language.EN:"英文",
   Language.JP:"日本",
}