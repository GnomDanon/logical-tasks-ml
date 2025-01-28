# import tkinter as tk
# from tkinter import filedialog
from docx import Document
# from langchain.document_loaders import PyPDFLoader
import fitz
import chardet
import os



# Функции для чтения файлов
def read_txt(file_name):
    with open(file_name, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"Определенная кодировка для {file_name}: {encoding}")
        return raw_data.decode(encoding)

def read_docx(file_name):
    doc = Document(file_name)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file_name):
    doc = fitz.open(file_name)
    full_text = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text.append(page.get_text())
    return '\n'.join(full_text)

def read_file(file_name):
    if file_name.endswith('.txt'):
        return read_txt(file_name)
    elif file_name.endswith('.docx'):
        return read_docx(file_name)
    elif file_name.endswith('.pdf'):
        return read_pdf(file_name)
    else:
        return f"Неизвестный формат файла: {file_name}"

def uploadFile(file_name):
    downloads_folder = os.path.expanduser('C:\\Users\\Daniil\\Downloads')
    file_path = os.path.join(downloads_folder, file_name)
    content = ""
    try:
        content = read_file(file_path)
        print(f"Содержимое файла {file_path}:")
        # print(content)
        print("\n" + "-"*40 + "\n")
        return content
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        print("\n" + "-"*40 + "\n")
        return content
