import torch
from transformers import AutoTokenizer
from splitting.intervals import getRequiredParagraphs
# Загрузка токенизатора для модели BERT
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


def split_text_into_fragments(text, max_tokens=1024):
    tokens = tokenizer.tokenize(text)

    # Разбиение токенов на фрагменты
    fragments = []
    for i in range(0, len(tokens), max_tokens):
        fragment = tokens[i:i + max_tokens]
        fragments.append(tokenizer.convert_tokens_to_string(fragment))

    return fragments


def getFragments(text,intervals):
    text = ("\n".join(getRequiredParagraphs([0,2,5],text,intervals)))

    fragments = split_text_into_fragments(text, max_tokens=2048)
    for i, fragment in enumerate(fragments):
        print(f"Fragment {i + 1}:\n{fragment}\n")
    return fragments