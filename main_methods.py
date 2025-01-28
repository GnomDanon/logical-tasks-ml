import random

from uploadFile import uploadFile
from parsing.topics_in_text_parser import search_topics_in_text
from parsing.topics_parser import extract_topics
from parsing.split_text_per_topics import unite_topics_and_indexies
from splitting.intervals import createIntervalsTopics,getRequiredParagraphs
from gigachat import get_chat_completion,get_token,refresh_token
from prompts import prompt_extract_termins,prompt_describe_termin,prompt_multiple_answer,prompt_parse_multiple
from splitting.gigachat_splitting import getFragments
import requests
import uuid
from config import auth
import json
import re

def parse_text_for_prompt(content, test_user_choice):
    try:
        topics = extract_topics(content)
        if topics is None:
            raise Exception("Пустой topics")
        topics_and_Idxs = unite_topics_and_indexies(content, topics)
    except Exception as e:
        print(f"Ошибка в extract_topics или unite_topics_and_indexies: {e}")
        try:
            topics_and_Idxs = search_topics_in_text(content)
            if topics_and_Idxs is None:
                raise Exception("Пустой topics")
        except Exception as e:
            print(f"Ошибка в search_topics_in_text: {e}")
            topics_and_Idxs = (content,0)
    finally:
        intervals = createIntervalsTopics(topics_and_Idxs, len(content))
        paragraphs = "\n".join(getRequiredParagraphs(test_user_choice, content, intervals))
        return getFragments(paragraphs)

def generatu_multiple_questions(amount, token, fragments):
    res = []
    lenF = len(fragments)
    if amount < lenF:
        reqs_texts = random.sample(fragments,amount)
        total_per_prompt = 1
        for i in reqs_texts:
            res.append(get_chat_completion(token,prompt_multiple_answer(total_per_prompt)+i).json()['choices'][0]['message']['content'])
    elif amount == lenF:
        total_per_prompt = 1
        for i in fragments:
            res.append(get_chat_completion(token,prompt_multiple_answer(total_per_prompt)+i).json()['choices'][0]['message']['content'])
    else:
        fill = amount//lenF
        totals = [fill for _ in range(lenF)]
        idxs = random.sample(range(lenF), amount-fill*lenF)
        for i in idxs:
            totals[i] += 1
        for i,e in enumerate(fragments):
            res.append(get_chat_completion(token,prompt_multiple_answer(totals[i])+e).json()['choices'][0]['message']['content'])
    return res

def parse_terms(text):
    lines = text.split('\n')
    matching_lines = [line for line in lines if len(line.split()) == 2]
    clean = lambda x: re.sub(r'[^а-яА-ЯёЁa-zA-Z\s]', '', x)
    cleaned_lines = [clean(i).strip() for i in matching_lines]
    # Объединяем разбитые слова обратно
    result = [''.join(word.split()) for word in cleaned_lines]
    return result

def generatu_termins(token, fragments, amount):
    # get_chat_completion(token, prompt_extract_termins(amount) + i).json()['choices'][0]['message']['content']
    # if amount>40:
        # amount = 40
    # if amount < 21:
        # amount = amount*2
    res = []
    lenF = len(fragments)
    if amount < lenF:
        reqs_texts = random.sample(fragments,amount)
        total_per_prompt = 1
        for i in reqs_texts:
            res.append(get_chat_completion(token, prompt_extract_termins(amount) + i).json()['choices'][0]['message']['content'])
    elif amount == lenF:
        total_per_prompt = 1
        for i in fragments:
            res.append(get_chat_completion(token, prompt_extract_termins(amount) + i).json()['choices'][0]['message']['content'])
    else:
        fill = amount//lenF
        totals = [fill for _ in range(lenF)]
        idxs = random.sample(range(lenF), amount-fill*lenF)
        for i in idxs:
            totals[i] += 1
        for i,e in enumerate(fragments):
            res.append(get_chat_completion(token,prompt_extract_termins(totals[i])+e).json()['choices'][0]['message']['content'])

    return '\n'.join([j for i in res for j in parse_terms(i)])

def generate_questions_crossword(terms,token):
    return get_chat_completion(token,prompt_describe_termin+terms).json()['choices'][0]['message']['content']
