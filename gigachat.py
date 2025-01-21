import requests
import uuid
from config import auth
import json
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
giga_token = ""
def init_gigachat():
    response = get_token(auth)
    if response != 1:
        giga_token = response.json()['access_token']

        url = "https://gigachat.devices.sberbank.ru/api/v1/models"
        payload={}
        headers = {
          'Accept': 'application/json',
          'Authorization': f'Bearer {giga_token}'
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

def get_chat_completion(auth_token, user_message):

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": user_message
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
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return -1
