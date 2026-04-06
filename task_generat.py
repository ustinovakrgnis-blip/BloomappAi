
# module: hf_questions_module.py
import os
import requests
import streamlit as st
from dotenv import load_dotenv  # для локального .env

# Если запускаешь локально, раскомментируй
# load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def generate_questions(topic: str) -> str:
    """Генерация 5 вопросов по теме через Hugging Face"""
    prompt = f"Сгенерируй 5 вопросов по теме: {topic} для школьников"
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return str(data)
    else:
        return f"Ошибка API: {response.status_code} {response.text}"


def run():
    """Функция запуска Streamlit интерфейса"""
    st.set_page_config(page_title="Генератор вопросов", page_icon="📝", layout="centered")
    st.title("Генератор вопросов для школьников")
    
    topic = st.text_input("Введите тему (например: C++, циклы в Python, LAN/WAN)")

    if st.button("Сгенерировать"):
        if not HF_TOKEN:
            st.error("Токен HF_TOKEN не найден! Добавьте его в Secrets или .env")
        elif topic.strip() == "":
            st.warning("Введите тему!")
        else:
            with st.spinner("Генерируем вопросы..."):
                questions = generate_questions(topic)
                st.subheader("Сгенерированные вопросы:")
                st.write(questions)
