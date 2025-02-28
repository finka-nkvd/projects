import customtkinter as ctk
import random
from tkinter import messagebox

class DigitalSignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital signature")
        self.root.geometry("300x335")
        ctk.set_appearance_mode("light")

        self.widgets()

    def widgets(self):
        self.input_field = ctk.CTkTextbox(self.root, width=290, height=130)
        self.input_field.place(x=5, y=5)

        self.button = ctk.CTkButton(self.root, text="Create signature", command=self.process_text)
        self.button.place(x=85, y=153)

        self.output_text = ctk.CTkTextbox(self.root, width=290, height=250)  # Увеличил размер поля вывода
        self.output_text.place(x=5, y=200)

    def hash_text(self, text):
        import hashlib
        hashed_text = hashlib.sha256(text.encode()).hexdigest().upper()
        return hashed_text

    def generate_keys(self):
        primes = [59, 73, 83, 113, 127, 151, 169, 187, 193, 211, 223, 241, 259, 269, 289, 301, 319, 331, 337, 353, 367, 383, 389, 401, 409, 421, 431, 433, 443, 449, 461, 463, 467, 479, 487, 503, 541, 547, 557, 569, 571, 577, 587, 593, 601, 613, 617, 619, 631, 641, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859]
        p, q = random.choice(primes), random.choice(primes)
        N = p * q
        fi = (p - 1) * (q - 1)
        e = random.choice(primes)
        while e >= fi:
            e = random.choice(primes)
        d = next(i for i in range(1, N) if (i * e) % fi == 1)
        return (e, N), (d, N)

    def sign_text(self, text, secret_key):
        hashed_text = self.hash_text(text)
        try:
            num = int(hashed_text, 16)
            signature = pow(num, secret_key[0], secret_key[1])
            return signature
        except:
            messagebox.showerror('Error', 'The fields must be filled in!')

    def verify_signature(self, signature, open_key, hashed_text):
        decrypted_num = pow(signature, open_key[0], open_key[1])
        decrypted_hash = hex(decrypted_num)[2:].upper()
        return decrypted_hash == hashed_text

    def process_text(self):
        text = self.input_field.get("1.0", "end-1c")
        if not text:
            messagebox.showerror('Error', 'The input field must be filled!')
            return

        open_key, secret_key = self.generate_keys()
        hashed_text = self.hash_text(text)
        signature = self.sign_text(text, secret_key)
        decrypted_hash = hex(pow(signature, open_key[0], open_key[1]))[2:].upper()

        self.output_text.delete('1.0', 'end')
        self.output_text.insert('end', f"Hashed text: {hashed_text}\n")
        self.output_text.insert('end', f"Open key: {open_key}\n")
        self.output_text.insert('end', f"Secret key: {secret_key}\n")
        self.output_text.insert('end', f"Signature: {signature}\n")
        self.output_text.insert('end', f"Decrypted hash: {decrypted_hash}\n")

        if self.verify_signature(signature, open_key, hashed_text):
            self.output_text.insert('end', "Signature verified\n")
        else:
            self.output_text.insert('end', "Signature unverified\n")

root = ctk.CTk()
app = DigitalSignatureApp(root)
root.mainloop()
