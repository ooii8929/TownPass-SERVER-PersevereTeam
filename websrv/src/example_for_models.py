from models.bot_model import Bot, Language, Style, SectionStage

# 開始使用，介紹大稻埕，並給予問題
def main():
    my_bot = Bot(
        language=Language.CHINESE,
        age=10,
        style=Style.HAPPY,
        user_location='永樂市場',
        all_locations = ["大稻埕碼頭", "龍山寺", "中正紀念堂", "九份老街","十分瀑布", "松山文創園區", "北投溫泉", "淡水老街"],
        visited_locations = ["大稻埕碼頭", "龍山寺", "淡水老街"]
    )

    response = my_bot.interact(SectionStage.BEGINNING, "")

    print(response)

# 聽完大稻埕介紹，回答問題
# def main():
#     my_bot = Bot(
#         language=Language.CHINESE,
#         age=10,
#         style=Style.HAPPY,
#         user_location='永樂市場',
#         all_locations = ["大稻埕碼頭", "龍山寺", "中正紀念堂", "九份老街","十分瀑布", "松山文創園區", "北投溫泉", "淡水老街"],
#         visited_locations = ["大稻埕碼頭", "龍山寺", "淡水老街"]
#     )

#     user_input = "大家好！我是你們今天超級開心的導覽員！我們現在要一起去探險一個超酷的地方喔！你們準備好了嗎？ 讓我們一起來認識大稻埕碼頭吧！這個地方可是台北市以前超級重要的港口呢！想像一下，很久很久以前，在1858年的時候，這裡開始變得很熱鬧。為什麼呢？因為那時候台灣的港口開放了，可以跟其他國家做生意啦！ 然後呢，在1866年，有一個來自美國的叔叔，他叫陶德，在大稻埕開了一個茶葉工廠。哇！從那時候開始，這裡就變得更熱鬧了！大家都來這裡買賣東西，特別是茶葉和樟腦。樟腦就是那種有香香味道的東西喔！ 大稻埕碼頭變得超級厲害，連附近的桃園、新竹的東西都會先送到這裡來。但是後來，河裡的沙子越來越多，大船就不能來了。再加上日本人把基隆港弄得更好，所以大稻埕碼頭慢慢就不像以前那麼熱鬧了。 不過，現在我們還是可以在這裡看到一艘很特別的小船喔！它叫做'唐山帆船'，雖然比真的船小很多，但是它可以告訴我們以前這裡有多麼熱鬧呢！ 好啦！現在我要考考你們喔！來回答一個小問題： 大稻埕碼頭最有名的出口商品是什麼呢？ A. 玩具 B. 茶葉和樟腦 C. 冰淇淋 你們覺得是哪一個呢？記得舉手回答喔！ 我覺得答案是A"

#     response = my_bot.interact(SectionStage.PROGRESS, user_input)

#     print(response)

# # 聽完大稻埕介紹，回答問題，加問題
# def main():
#     my_bot = Bot(
#         language=Language.CHINESE,
#         age=10,
#         style=Style.HAPPY,
#         user_location='永樂市場',
#         all_locations = ["大稻埕碼頭", "龍山寺", "中正紀念堂", "九份老街","十分瀑布", "松山文創園區", "北投溫泉", "淡水老街"],
#         visited_locations = ["大稻埕碼頭", "龍山寺", "淡水老街"]
#     )

#     user_input = "我很好奇大稻埕的發展"

#     response = my_bot.interact(SectionStage.PROGRESS, user_input)

#     print(response)

# # 聽完大稻埕介紹，被動回應，跳下一題
# def main():
#     my_bot = Bot(
#         language=Language.CHINESE,
#         age=10,
#         style=Style.HAPPY,
#         user_location='永樂市場',
#         all_locations = ["大稻埕碼頭", "龍山寺", "中正紀念堂", "九份老街","十分瀑布", "松山文創園區", "北投溫泉", "淡水老街"],
#         visited_locations = ["大稻埕碼頭", "龍山寺", "淡水老街"]
#     )

#     user_input = "我沒什麼問題"

#     response = my_bot.interact(SectionStage.BEGINNING, user_input)

#     print(response)

if __name__ == "__main__":
    main()