from flask import Flask, request, jsonify
from main_methods import parse_text_for_prompt, refresh_token, generatu_multiple_questions, generatu_termins, generate_questions_crossword
from gigachat import get_chat_completion
from prompts import prompt_parse_multiple, prompt_parse_termin

app = Flask(__name__)

@app.route('/crossword', methods=['POST'])
def generateCrosswordQuestions():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    questions_count = request.form.get('questions_count', type=int)
    if questions_count is None:
        return jsonify({'error': 'Missing questions_count parameter'}), 400
    
    result = generateCrosswordProcess(file, questions_count)
    return jsonify({'result': result})

@app.route('/test', methods=['POST'])
def generateTestQuestions():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    questions_count = request.form.get('questions_count', type=int)
    if questions_count is None:
        return jsonify({'error': 'Missing questions_count parameter'}), 400
    
    result = generateTestProcess(file, questions_count)
    return jsonify({'result': result})


def generateCrosswordProcess(file, questions_count):
    file_content = file.read().decode('ansi')
    test_user_choice = [0,2,5]
    fragments = parse_text_for_prompt(file_content, test_user_choice)
    token = refresh_token()
    termins = generatu_termins(token, fragments, questions_count)
    questions = generate_questions_crossword(termins, token)
    res = get_chat_completion(token, prompt_parse_termin + '\n'.join(questions)).json()['choices'][0]['message']['content']
    res = res.replace('```', '').replace('json', '').replace('term', 'answer').replace('definition', 'question')
    return res

def generateTestProcess(file, questions_count):
    file_content = file.read().decode('ansi')
    test_user_choice = [0,2,5]
    fragments = parse_text_for_prompt(file_content, test_user_choice)
    token = refresh_token()
    questions = generatu_multiple_questions(questions_count, token, fragments)
    res = get_chat_completion(token, prompt_parse_multiple + '\n'.join(questions)).json()['choices'][0]['message']['content']
    res = res.replace('```', '').replace('json', '').replace(':0}',':"A"}').replace(':1}',':"B"}').replace(':2}',':"C"}').replace(':3}',':"D"}')
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)