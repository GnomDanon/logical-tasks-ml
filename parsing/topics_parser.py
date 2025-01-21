from collections import deque
import re
def extract_topics(text):
    sentences = text.split("\n")
    list_pattern = r'^\s*(содержание|оглавление|Содержание|СОДЕРЖАНИЕ|Оглавление|ОГЛАВЛЕНИЕ)\s*$'
    lenS = len(sentences)
    topics= []
    queue = deque()
    queue_dot_count = 0
    isFound = True
    for i in range(lenS):
      line = sentences [i]
      if re.search(list_pattern, line):
        for j in range(i+1,lenS):

            if isFound or queue_dot_count:
                if len(queue) > 5:
                    if queue[0][1]:
                        queue_dot_count -= 1
                    # print(queue_dot_count)
                    queue.popleft()
                topics.append(sentences[j])
                if sentences[j].count('…') > 1 or sentences[j].count('.') > 6:
                    queue_dot_count += 1
                    isFound = False
                    queue.append((sentences[j],1))
                else:
                    queue.append((sentences[j], 0))
                # print(queue)
            else:
                break
        topics = topics[:-6]
        return unite_lines_topics(topics)
# topics = extract_topics(sentences)

def unite_lines_topics(topics):
    topic = []
    res = []
    for i in topics:
        if not(i.count('…') > 1 or i.count('.') > 6):
            topic.append(i)
        else:
            topic.append(i)
            res.append(" ".join(topic))
            topic = []
    return res

clean_sequence = lambda x: re.sub(r'[^а-яА-ЯёЁa-zA-Z0-9\s-]', '', x)

def clean_topic(topic):
    # is_num_page = True
    l = len(topic)
    final_idx = 0
    for i in range(l-1,-1,-1):
        if topic[i].isdigit():
            continue
        for j in range(i,-1,-1):
            if topic[j] == '…' or topic[j] == '.':
                final_idx = j
            else:
                break
        break
    return topic[:final_idx]