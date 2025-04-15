# auth.py
import customtkinter as ctk
from auth_utils import register_user, authenticate_user

class AuthWindow:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.window = ctk.CTk()
        self._setup_ui()
        self.is_login_mode = True

    def _setup_ui(self):
        self.window.title("Авторизация")
        self.window.geometry("400x400")

        # Frame for auth widgets
        auth_frame = ctk.CTkFrame(self.window)
        auth_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(auth_frame, text="Логин:").pack(pady=5)
        self.login_entry = ctk.CTkEntry(auth_frame)
        self.login_entry.pack(pady=5)

        ctk.CTkLabel(auth_frame, text="Пароль:").pack(pady=5)
        self.password_entry = ctk.CTkEntry(auth_frame, show="*")
        self.password_entry.pack(pady=5)

        self.auth_button = ctk.CTkButton(auth_frame, text="Войти", command=self._handle_auth)
        self.auth_button.pack(pady=20)

        self.toggle_mode_button = ctk.CTkButton(
            auth_frame, 
            text="Регистрация", 
            command=self._toggle_mode,
            fg_color="transparent",
            hover=False,
            text_color=("black", "white")
        )
        self.toggle_mode_button.pack(pady=10)

        self.message_label = ctk.CTkLabel(auth_frame, text="", text_color="red")
        self.message_label.pack()

    def _toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        if self.is_login_mode:
            self.auth_button.configure(text="Войти")
            self.toggle_mode_button.configure(text="Регистрация")
        else:
            self.auth_button.configure(text="Зарегистрироваться")
            self.toggle_mode_button.configure(text="Вход")
        self.message_label.configure(text="")

    def _handle_auth(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.message_label.configure(text="Введите логин и пароль")
            return

        if self.is_login_mode:
            if authenticate_user(username, password):
                self.window.destroy()
                self.on_login_success()
            else:
                self.message_label.configure(text="Неверный логин или пароль")
        else:
            if register_user(username, password):
                self.message_label.configure(text="Регистрация успешна!", text_color="green")
            else:
                self.message_label.configure(text="Пользователь уже существует")

    def run(self):
        self.window.mainloop()