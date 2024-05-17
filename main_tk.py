#Для создания описанной программы на Tkinter, мы разработаем приложение, которое будет состоять
#из нескольких частей: начальный
#экран для входа или регистрации, экран выбора темы
#викторины, саму викторину и результаты.Для начала создадим основу приложения:

import tkinter as tk
from tkinter import simpledialog, messagebox

# Данные для примера
users = {'user1': 'pass1'}
topics = {
  "История": [
    {"Вопрос1": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос2": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос3": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос4": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос5": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос6": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос7": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос8": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос9": ("Ответ1", "Ответ2", "Ответ3")},
    {"Вопрос10": ("Ответ1", "Ответ2", "Ответ3")}
  ],
    "Наука": ["Вопрос1", "Вопрос2", "Вопрос3", "Вопрос4", "Вопрос5", "Вопрос6", "Вопрос7", "Вопрос8", "Вопрос9",
              "Вопрос10"],
    "Искусство": ["Вопрос1", "Вопрос2", "Вопрос3", "Вопрос4", "Вопрос5", "Вопрос6", "Вопрос7", "Вопрос8", "Вопрос9",
                  "Вопрос10"],
    "Технологии": ["Вопрос1", "Вопрос2", "Вопрос3", "Вопрос4", "Вопрос5", "Вопрос6", "Вопрос7", "Вопрос8", "Вопрос9",
                   "Вопрос10"]
}


class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Викторина")

        self.login_frame = tk.Frame(self.master)
        self.quiz_frame = tk.Frame(self.master)
        self.topic_frame = tk.Frame(self.master)
        self.result_frame = tk.Frame(self.master)

        self.current_user = None
        self.current_topic = None
        self.question_index = 0

        self.setup_login_frame()

    def setup_login_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        self.login_frame.pack(fill="both", expand=True)
        tk.Label(self.login_frame, text="Логин:").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()
        tk.Label(self.login_frame, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()
        tk.Button(self.login_frame, text="Вход", command=self.login).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in users and users[username] == password:
            self.current_user = username
            self.login_frame.pack_forget()
            self.setup_topic_frame()
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль")

    def setup_topic_frame(self):
        for widget in self.topic_frame.winfo_children():
            widget.destroy()

        self.topic_frame.pack(fill="both", expand=True)
        tk.Label(self.topic_frame, text=f"Привет, {self.current_user}").pack()
        tk.Label(self.topic_frame, text="Выберите тему вопроса").pack()

        x=0
        x0 = 50
        for topic in topics.keys():
            x+=20
            tk.Button(self.topic_frame, text=topic, command=lambda t=topic: self.select_topic(t)).pack()

        #   Кнопка выход
        tk.Button(self.topic_frame, text="Выход", command=self.logout).pack()

    def select_topic(self, topic):
        self.current_topic = topic
        simpledialog.messagebox.showinfo("Старт викторины", f"Тема: {self.current_topic}")
        self.topic_frame.pack_forget()
        self.setup_quiz_frame()

    def display_question(self):
        # Очистка фрейма от предыдущих виджетов
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()

        if self.question_index < len(topics[self.current_topic]):
            question = topics[self.current_topic][self.question_index]
            tk.Label(self.quiz_frame, text=f"Вопрос {self.question_index + 1}: {question}").pack()

            # Создание кнопок для ответов (пример с демо-ответами)
            answers = ["Ответ 1", "Ответ 2", "Ответ 3"]
            for answer in answers:
                button = tk.Button(self.quiz_frame, text=answer, command=lambda a=answer: self.check_answer(a))
                button.pack()

    def check_answer(self, answer):
        # здесь можно добавить логику проверки ответа
        self.question_index += 1
        self.display_question()

    def setup_quiz_frame(self):
        self.quiz_frame.pack(fill="both", expand=True)
        self.display_question()

    def setup_result_frame(self):
        self.result_frame.pack(fill="both", expand=True)
        tk.Label(self.result_frame, text="Викторина завершена! Ваши результаты:").pack()
        # Пример результата
        tk.Label(self.result_frame,
                 text=f"{self.question_index} из {len(topics[self.current_topic])} правильных").pack()
        tk.Button(self.result_frame, text="Назад к темам", command=self.back_to_topics).pack()

    def back_to_topics(self):
        self.result_frame.pack_forget()
        self.setup_topic_frame()

    def logout(self):
        self.topic_frame.pack_forget()
        self.setup_login_frame()

#   Вход программы

root = tk.Tk()
root.geometry("800x600")
app = QuizApp(root)
root.mainloop()

