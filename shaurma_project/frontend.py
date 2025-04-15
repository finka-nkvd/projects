# frontend.py
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import data
import re
from datetime import datetime
from backend import Backend


class Frontend:
    def __init__(self, backend):
        self.backend = backend
        self.window = ctk.CTk()
        self._setup_main_window()
        self.cart_items = []

    def _setup_main_window(self):
        self.window.title("Шаурма-шоп")
        self.window.geometry("750x800")

        cart_frame = ctk.CTkFrame(self.window, width=300)
        cart_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(cart_frame, text="Корзина", font=("Arial", 16)).pack(pady=10)
        self.cart_listbox = ctk.CTkScrollableFrame(cart_frame, width=280, height=500)
        self.cart_listbox.pack()

        self.total_label = ctk.CTkLabel(cart_frame, text="Итого: 0 руб", font=("Arial", 14))
        self.total_label.pack(pady=10)

        ctk.CTkButton(cart_frame, text="Очистить корзину", command=self._clear_cart).pack(pady=5)
        ctk.CTkButton(cart_frame, text="Заказать", command=self._open_payment).pack(pady=10)

        products_frame = ctk.CTkScrollableFrame(self.window)
        products_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        for idx, item in enumerate(data.shaurma_items):
            item_frame = self._create_product_item(products_frame, item, idx)
            item_frame.grid(row=idx // 2, column=idx % 2, padx=10, pady=10)

    def _create_product_item(self, parent, item, idx):
        try:
            img = ctk.CTkImage(Image.open(f"{item['name']}.png"), size=(150, 200))
        except FileNotFoundError:
            img = ctk.CTkImage(Image.new("RGB", (150, 150), "#333"), size=(150, 150))

        frame = ctk.CTkFrame(parent)

        ctk.CTkLabel(frame, image=img, text="").grid(row=0, column=0)
        ctk.CTkLabel(frame, text=item['name'], font=("Arial", 14)).grid(row=1, column=0)

        size_var = ctk.StringVar(value="Средняя")
        size_menu = ctk.CTkOptionMenu(frame, values=["Маленькая", "Средняя", "Большая"], variable=size_var)
        size_menu.grid(row=2, column=0, pady=5)

        price_label = ctk.CTkLabel(frame, text=f"{item['price'][size_var.get()]} руб")
        price_label.grid(row=3, column=0)

        def update_price(*args):
            price_label.configure(text=f"{item['price'][size_var.get()]} руб")

        size_var.trace("w", update_price)

        ctk.CTkButton(
            frame,
            text="Добавить",
            command=lambda i=item, s=size_var: self._add_to_cart(i, s.get())
        ).grid(row=4, column=0, pady=5)

        return frame

    def _add_to_cart(self, item, size):
        price = item['price'][size]
        cart_item = {
            'name': item['name'],
            'size': size,
            'price': price,
            'description': item['description']
        }
        self.backend.add_to_cart(cart_item)
        self._update_cart_display()

    def _update_cart_display(self):
        for widget in self.cart_listbox.winfo_children():
            widget.destroy()

        for idx, item in enumerate(self.backend.cart):
            item_frame = ctk.CTkFrame(self.cart_listbox, width=260)
            item_frame.pack(fill="x", pady=2)

            ctk.CTkLabel(
                item_frame,
                text=f"{item['name']} ({item['size']}) - {item['price']} руб",
                width=200
            ).pack(side="left")

            ctk.CTkButton(
                item_frame,
                text="×",
                width=30,
                command=lambda i=idx: self._remove_from_cart(i)
            ).pack(side="right")

        self.total_label.configure(text=f"Итого: {self.backend.get_total()} руб")

    def _remove_from_cart(self, index):
        if 0 <= index < len(self.backend.cart):
            self.backend.cart.pop(index)
            self._update_cart_display()

    def _clear_cart(self):
        self.backend.clear_cart()
        self._update_cart_display()

    def _open_payment(self):
        if not self.backend.cart:
            messagebox.showwarning("Корзина пуста", "Добавьте товары в корзину перед оформлением заказа")
            return

        payment_window = ctk.CTkToplevel(self.window)
        payment_window.title("Оплата")
        payment_window.geometry("400x400")
        payment_window.grab_set()
        fields = ["Номер карты:", "Срок действия (MM/YY):", "CVV:", "Имя на карте:"]
        entries = []

        for field in fields:
            ctk.CTkLabel(payment_window, text=field).pack(pady=5)
            entry = ctk.CTkEntry(payment_window)
            entry.pack(pady=5)
            entries.append(entry)

        ctk.CTkButton(
            payment_window,
            text="Оплатить",
            command=lambda: self._process_payment(payment_window, entries)
        ).pack(pady=20)

    def _process_payment(self, window, entries):
        if any(not entry.get() for entry in entries):
            messagebox.showerror("Ошибка", "Заполните все поля платежных данных")
            return

        receipt_number = self.backend.process_payment()
        total = self.backend.get_total()
        window.destroy()
        messagebox.showinfo(
            "Чек",
            f"Заказ №{receipt_number} оформлен!\nСумма: {total} руб\nСпасибо за покупку!"
        )
        self._clear_cart()

    def _validate_card(self, card_number, expiry, cvv, card_name):
        """Валидация данных карты с помощью регулярных выражений"""

        # Проверка номера карты (16 цифр, может быть с пробелами)
        if not re.fullmatch(r'(\d{4}\s?){4}', card_number):
            return "Номер карты должен содержать 16 цифр"

        # Проверка срока действия (MM/YY)
        if not re.fullmatch(r'\d{2}/\d{2}', expiry):
            return "Неверный формат срока действия (используйте MM/YY)"

        try:
            month, year = map(int, expiry.split('/'))
            current_year = datetime.now().year % 100
            current_month = datetime.now().month

            if not (1 <= month <= 12):
                return "Месяц должен быть от 01 до 12"

            if year < current_year or (year == current_year and month < current_month):
                return "Срок действия карты истек"

        except ValueError:
            return "Неверный формат срока действия"

        # Проверка CVV (3 или 4 цифры)
        if not re.fullmatch(r'\d{3,4}', cvv):
            return "CVV должен содержать 3 или 4 цифры"

        # Проверка имени (только буквы и пробелы)
        if not re.fullmatch(r'[a-zA-Zа-яА-Я\s]+', card_name):
            return "Имя на карте должно содержать только буквы"

        return None

    def _process_payment(self, window, entries):
        card_data = [entry.get() for entry in entries]
        validation_error = self._validate_card(*card_data)

        if validation_error:
            messagebox.showerror("Ошибка", validation_error)
            return

        try:
            receipt_number = self.backend.process_payment()
            total = self.backend.get_total()
            window.destroy()
            messagebox.showinfo(
                "Чек",
                f"Заказ №{receipt_number} оформлен!\nСумма: {total} руб\nСпасибо за покупку!"
            )
            self._clear_cart()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def run(self):
        self.window.mainloop()