from uploadFile import uploadFile
from parsing.topics_in_text_parser import search_topics_in_text
from parsing.topics_parser import extract_topics
from parsing.split_text_per_topics import unite_topics_and_indexies
from splitting.intervals import createIntervalsTopics,getRequiredParagraphs
# from gigachat import init_gigachat,get_chat_completion,giga_token
from prompts import prompt_extract_termins,prompt_describe_termin,prompt_multiple_answer
from splitting.gigachat_splitting import getFragments
import requests
import uuid
from config import auth
import json


file_name = 'VKR.docx'
content = uploadFile(file_name)

search_topics_in_text(content)

topics = extract_topics(content)
topics_and_Idxs = unite_topics_and_indexies(content,topics)
print(topics_and_Idxs)

intervals = createIntervalsTopics(topics_and_Idxs,len(content))

test_user_choice = [0,2,5]
print(*getRequiredParagraphs(test_user_choice,content,intervals))
# init_gigachat()
def get_token(auth_token, scope='GIGACHAT_API_PERS'):

    rq_uid = str(uuid.uuid4())
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    payload = {
        'scope': scope
    }

    try:
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

fraqs=getFragments(content,intervals)[9]
# ask_termins = get_chat_completion(giga_token,prompt_multiple_answer + fraqs)
# print(ask_termins)





