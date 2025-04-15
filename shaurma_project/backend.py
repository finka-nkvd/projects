# backend.py
import random
from abc import ABC, abstractmethod


class CartOperations(ABC):
    @abstractmethod
    def add_to_cart(self, item):
        pass

    @abstractmethod
    def get_total(self):
        pass

    @abstractmethod
    def clear_cart(self):
        pass


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class SimplePaymentProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Сумма платежа должна быть положительной")
        return random.randint(100000, 999999)


class Backend(CartOperations):
    def __init__(self, payment_processor: PaymentProcessor = None):
        self.cart = []
        self.payment_processor = payment_processor or SimplePaymentProcessor()

    def add_to_cart(self, item):
        self.cart.append(item)

    def get_total(self):
        return sum(item['price'] for item in self.cart)

    def process_payment(self):
        if not self.cart:
            raise ValueError("Корзина пуста")
        total = self.get_total()
        return self.payment_processor.process_payment(total)

    def clear_cart(self):
        self.cart.clear()