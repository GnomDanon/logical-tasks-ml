import re
def search_topics_in_text(text):
    sentences = text.split("\n")
    pattern = r'\b(Глава|ГЛАВА|глава|ЧАСТЬ|часть|Часть|Параграф|ПАРАГРАФ|параграф)\s+((\d{1,2})|(I|V|X|L|C|D|M)+)\b'
    next_line_pattern = r'^[А-Яа-я]'
    lenS = len(sentences)
    # Проверяем единственный случай, когда только СНИЗУ может быть отступ, чтобы не делать это в цикле
    if re.search(pattern,sentences[0]):

        if sentences [1].strip() == '':
          if sentences [2].strip() != '' and sentences [3].strip() == '' and re.match(next_line_pattern, sentences[2]):
            print(sentences[0], sentences[2])
          else:
            print(sentences[0])

        else:
          if sentences [2].strip() == '' and re.match(next_line_pattern, sentences[1]):
            print(sentences[0], sentences[1])
          else:
            print(sentences[0])

    for i in range(1,len(sentences)):
        line = sentences [i]
        if re.search(pattern, line):
              if sentences [i - 1].strip() == '':
                if i < lenS-2:

                  if sentences [i+1].strip() == '':
                    if i < lenS-3:
                      if sentences [i+2].strip() != '' and sentences [i+3].strip()=='' and re.match(next_line_pattern, sentences[i+2]):
                        print(sentences[i],sentences[i+2])
                      else:
                        print(sentences[i])
                  elif sentences [i+2].strip() == '' and re.match(next_line_pattern, sentences[i+1]):
                    print(sentences[i], sentences[i+1])
                  else:
                    print(sentences[i])