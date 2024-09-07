from models.bot_model import Bot, Language, Preference, Character, SectionStage

def main():
    # 创建一个 Bot 实例
    my_bot = Bot(
        language=Language.CHINESE,
        preference=Preference.HISTORY,
        age=10,
        character=Character.HAPPY,
        user_location='永樂市場',
        all_locations = ["大稻埕碼頭", "龍山寺", "中正紀念堂", "九份老街","十分瀑布", "松山文創園區", "北投溫泉", "淡水老街"],
        visited_locations = ["大稻埕碼頭", "龍山寺", "淡水老街"]
    )

    user_input = "你好，我想了解大稻埕碼頭"

    response = my_bot.interact(SectionStage.BEGINNING, user_input)

    print(response)

if __name__ == "__main__":
    main()