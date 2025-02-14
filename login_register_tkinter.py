import tkinter as tk
from tkinter import ttk, messagebox
import json
import hashlib


def hash_password(password):
    return hashlib.sha3_256(password.encode()).hexdigest()


def register():
    login = login_entry.get()
    password = password_entry.get()

    if not login or not password:
        messagebox.showerror("Ошибка", "Поля логина и пароля должны быть заполнены")
        return

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if login in data:
        messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
        return

    hashed_password = hash_password(password)

    data[login] = hashed_password

    with open('data.json', 'w') as file:
        json.dump(data, file)

    messagebox.showinfo("Успех", "Вы успешно зарегистрированы")


def login_user():
    login = login_entry.get()
    password = password_entry.get()

    if not login or not password:
        messagebox.showerror("Ошибка", "Поля логина и пароля должны быть заполнены")
        return

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)

            hashed_input_password = hash_password(password)

            if login in data and data[login] == hashed_input_password:
                messagebox.showinfo("Успех", "Вы успешно вошли в систему")
            else:
                messagebox.showerror("Ошибка", "Неправильный логин или пароль")

    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл данных не найден")


root = tk.Tk()
root.title("Регистрация и вход")
root.geometry("300x220")
root.resizable(False, False)

login_label = tk.Label(text="Log In")
login_label.place(x=1, y=40)
password_label = tk.Label(text="Password")
password_label.place(x=1, y=120)

login_entry = ttk.Entry(root)
login_entry.place(x=90, y=40)

password_entry = ttk.Entry(root)
password_entry.place(x=90, y=120)

reg_button_text = "Зарегистрироваться"
reg_button = tk.Button(text=f"{reg_button_text}", command=lambda: register())
reg_button.place(x=15, y=180)

log_button = tk.Button(text=f"         Войти          ", command=lambda: login_user())
log_button.place(x=185, y=180)

root.mainloop()
