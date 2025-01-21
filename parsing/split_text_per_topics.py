import re
from parsing.topics_parser import clean_sequence,clean_topic
def find_sequence_index(text, sequence):
    cleaned_sequence = clean_sequence(sequence)

    words = cleaned_sequence.split()

    pattern = r'\b' + r'\W*'.join(re.escape(word) for word in words) + r'\b'

    # Ищем все совпадения в тексте
    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    if len(matches) >= 2:
        second_match = matches[1]
        start_index = second_match.start()

        # начало первого слова во втором совпадении
        first_word_pattern = r'\b' + re.escape(words[0]) + r'\b'
        first_word_match = re.search(first_word_pattern, text[start_index:], re.IGNORECASE)

        if first_word_match:
            # Индекс первого слова во втором совпадении
            first_word_index = start_index + first_word_match.start()
            return first_word_index
        else:
            return -1
    else:
        return -1


def unite_topics_and_indexies(text, topics):
    res = []
    for topic in topics:
        topic=clean_sequence(clean_topic(topic))
        idx = find_sequence_index(text, topic)
        if idx > 0:
          res.append((topic, idx))
    return res
# topicsIdxs = unite_topics_and_indexies(unite_lines_topics(extract_topics(sentences)))
# print(topicsIdxs)