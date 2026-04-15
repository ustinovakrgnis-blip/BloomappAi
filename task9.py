import streamlit as st
import pandas as pd
import os
import requests
import re

# ===========================
# HF ROUTER ИИ
# ===========================
HF_MODEL_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = st.secrets["HF_TOKEN"]

def gpt_explain(task_text):

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "user",
                "content": f"Объясни задачу ученику просто:\n{task_text}"
            }
        ],
        "max_tokens": 200
    }

    try:
        r = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=60)
        data = r.json()

        if isinstance(data, dict) and "error" in data:
            return f"💡 ИИ недоступен: {data['error']}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"💡 Ошибка: {e}"


# ===========================
# MAIN APP
# ===========================
def run():

    file_path = "blooms_dataset.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8")
    else:
        df = pd.DataFrame({
            "text": ["Пример задачи $$P(A)=1/6$$"],
            "answer": ["1/6"],
            "topic": ["probability"],
            "bloom": ["remembering"],
            "image": [""]
        })

    df = df.fillna("")

    # ===========================
    # SESSION STATE
    # ===========================
    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "total" not in st.session_state:
        st.session_state.total = 0

    if "topic_stats" not in st.session_state:
        st.session_state.topic_stats = {}

    # ===========================
    # HEADER
    # ===========================
    st.title("📚 LMS PRO + ANALYTICS")

    st.progress(st.session_state.score / max(st.session_state.total, 1))
    st.write(f"⭐ {st.session_state.score} / {st.session_state.total}")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Задачи",
        "💻 Решение",
        "💡 ИИ",
        "📊 Анализ"
    ])

    # ===========================
    # TAB 1 - TASKS
    # ===========================
    with tab1:

        topic = st.text_input("Фильтр темы")

        filtered = df.copy()

        if topic:
            filtered = filtered[filtered["topic"].str.contains(topic.lower(), na=False)]

        tasks = filtered.reset_index()

        choice = st.selectbox(
            "Выбери задачу",
            tasks.index,
            format_func=lambda i: tasks.loc[i, "text"][:80]
        )

        st.session_state.selected_task = tasks.loc[choice, "index"]

    # ===========================
    # TAB 2 - SOLVE
    # ===========================
    with tab2:

        if st.session_state.selected_task is None:
            st.info("Выбери задачу")
            return

        task = df.loc[st.session_state.selected_task]

        st.markdown("## 📌 Задача")

        # ===========================
        # IMAGE
        # ===========================
        if "image" in task and task["image"]:
            if os.path.exists(task["image"]):
                st.image(task["image"], use_container_width=True)
            else:
                st.warning("Картинка не найдена")

        # ===========================
        # TEXT + LATEX RENDER
        # ===========================
        text = str(task["text"])

        parts = re.split(r"(\$\$.*?\$\$)", text, flags=re.DOTALL)

        for part in parts:
            part = part.strip()

            if not part:
                continue

            if part.startswith("$$") and part.endswith("$$"):
                latex = part.strip("$")
                st.latex(latex)
            else:
                st.markdown(part)

        # ===========================
        # ANSWER CHECK
        # ===========================
        st.markdown("### ✍️ Ответ")
        ans = st.text_input("Ответ")

        if st.button("Проверить"):

            st.session_state.total += 1

            topic = task["topic"]

            if topic not in st.session_state.topic_stats:
                st.session_state.topic_stats[topic] = {"total": 0, "correct": 0}

            st.session_state.topic_stats[topic]["total"] += 1

            if ans.strip() == task["answer"].strip():
                st.success("Верно ✅")
                st.session_state.score += 1
                st.session_state.topic_stats[topic]["correct"] += 1
            else:
                st.error("Неверно ❌")
                st.info(f"Ответ: {task['answer']}")

        # ===========================
        # CODE EXECUTOR
        # ===========================
        st.markdown("### 💻 Код")
        code = st.text_area("Python")

        if st.button("Run"):

            try:
                local = {}
                exec(code, {}, local)

                result = list(local.values())[-1] if local else None

                st.write("Результат:", result)

                st.session_state.total += 1

                topic = task["topic"]

                if topic not in st.session_state.topic_stats:
                    st.session_state.topic_stats[topic] = {"total": 0, "correct": 0}

                st.session_state.topic_stats[topic]["total"] += 1

                if str(result).strip() == task["answer"].strip():
                    st.success("Код верный ✅")
                    st.session_state.score += 1
                    st.session_state.topic_stats[topic]["correct"] += 1
                else:
                    st.error("Код неверный ❌")

            except Exception as e:
                st.error(f"Ошибка: {e}")

    # ===========================
    # TAB 3 - AI
    # ===========================
    with tab3:

        if st.session_state.selected_task is None:
            st.info("Выбери задачу")
            return

        task = df.loc[st.session_state.selected_task]

        if st.button("💡 Объяснить ИИ"):
            st.info(gpt_explain(task["text"]))

    # ===========================
    # TAB 4 - ANALYTICS
    # ===========================
    with tab4:

        st.subheader("📊 Анализ класса по темам")

        if not st.session_state.topic_stats:
            st.info("Пока нет данных")
        else:

            data = []

            for topic, stats in st.session_state.topic_stats.items():

                total = stats["total"]
                correct = stats["correct"]

                acc = correct / total if total > 0 else 0

                data.append({
                    "Тема": topic,
                    "Всего": total,
                    "Верно": correct,
                    "Успешность (%)": round(acc * 100, 1)
                })

            df_stats = pd.DataFrame(data)

            st.dataframe(df_stats)

            strong = df_stats[df_stats["Успешность (%)"] >= 75]["Тема"].tolist()
            weak = df_stats[df_stats["Успешность (%)"] < 60]["Тема"].tolist()

            st.markdown("### 💪 Сильные темы")
            st.success(", ".join(strong) if strong else "Нет сильных тем")

            st.markdown("### ⚠️ Слабые темы")
            st.error(", ".join(weak) if weak else "Нет слабых тем")


if __name__ == "__main__":
    run()
