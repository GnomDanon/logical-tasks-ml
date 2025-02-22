def prompt_extract_termins (amount):
    return f"""Извлеки {amount} терминов состоящие из одного слова или обобщи составные термины в ОДНО СЛОВО
 из заданного текста, если термин составной то сделай аббревиатуру. Извлеченные термины верни в виде списка:
 . Вот сам текст:
"""

def prompt_multiple_answer(amount):
    return f"""Представь что ты преподаватель и составляешь тест для онлайн курса.Задай мне {amount} вопросов по заданному тексту.
 Вопросы должны иметь 4 варианта ответа, из которых правильный только один, остальные варианты должны запутать твоих учеников.
 Вопрос и варианты ответа должны быть разделены следующим образом:
   Вопрос: [Вопрос]
   Варианты ответа:
   A) [Вариант 1]
   B) [Вариант 2]
   C) [Вариант 3]
   D) [Вариант 4]
   
"""

prompt_describe_termin = """Представь, что ты играешь в Элиас, тебе дали список слов.
 Опиши в одно-два предложения каждое из этих слов и выведи результат следующим образом:
 1. скутер - как мотоцикл только самокат
"""

prompt_parse_multiple = """Произведи парсинг тестовых заданий к JSON виду и верни ответ в JSON формате, не пиши ничего кроме результата парсинга: 
[{"question":"string","answers":["string","string","string","string"],"correctAnswer":int},{"question":"string","answers":["string","string","string","string"],"correctAnswer":int}]

"""

prompt_parse_termin = """Произведи парсинг терминов и определений к JSON виду и верни ответ в JSON формате, никак не изменяй содержимое и не пиши ничего кроме результата парсинга:
[{"term":"string","definition":"string"},{"term":"string","definition":"string"}]
"""