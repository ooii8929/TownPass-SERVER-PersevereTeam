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