import requests
import uuid
from  config import auth
from prompts import prompt_extract_termins,prompt_describe_termin,prompt_multiple_answer
from main import fraqs
def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.

      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - область (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».

      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

response = get_token(auth)
if response != 1:
  print(response.text)
  giga_token = response.json()['access_token']

url = "https://gigachat.devices.sberbank.ru/api/v1/models"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': f'Bearer {giga_token}'
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print(response.text)

import json

def get_chat_completion(auth_token, user_message):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": user_message  # Содержание сообщения
            }
        ],
        "temperature": 0,  # Температура генерации
        "top_p": 0,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 2048,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1.2,  # Штраф за повторения
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })

    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1

prompt = """Извлеки все термины состоящие из одного слова или обобщи составные термины в ОДНО СЛОВО из заданного текста, если термин составной то сделай аббревиатуру. Извлеченные термины верни в виде списка безо всяких комментариев. Вот сам текст:
"""
prompt2 = """Представь что ты преподаватель и составляешь тест для онлайн курса.Задай мне 20 вопросов по заданному тексту.
 Вопросы должны иметь 4 варианта ответа, из которых правильный только один, остальные варианты должны запутать твоих учеников.
 Вопрос и варианты ответа должны быть разделены следующим образом:
   Вопрос: [Вопрос]
   Варианты ответа:
   A) [Вариант 1]
   B) [Вариант 2]
   C) [Вариант 3]
   D) [Вариант 4]

"""

prompt3 = """Представь, что ты играешь в Элиас, тебе дали список слов.
 Опиши в одно-два предложения каждое из этих слов и варианты ответа должны быть разделены следующим образом:
 1. скутер - как мотоцикл только самокат
"""

test_res = """В результате обработки текста были получены следующие термины:

- Кибербезопасность
- Эволюция
- Феномен
- Технический прогресс
- Правовая база
- Методы хищения
- Искажение информации
- Уничтожение информации
- Информационные ресурсы
- Киберпространство
- Контрмеры
- Актуальность
- Модели прогрессивного развития
- Международный контроль
- Обособленный орган
- Международные институты
- Национальный уровень
- Международная система
- Целостная модель
- Меры
- Теоретическая значимость"""

# ask_termins = get_chat_completion(giga_token,prompt + getFragments()[9])
# ask_termins = get_chat_completion(giga_token,prompt3 + test_res)
ask_termins = get_chat_completion(giga_token,prompt_multiple_answer + fraqs)

txt_answ_termins = ask_termins.json()['choices'][0]['message']['content']
print(txt_answ_termins )