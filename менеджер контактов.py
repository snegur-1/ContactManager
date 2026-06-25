import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "contacts.json"

class ContactManagerApp:
def __init__(self, root):
self.root = root
self.root.title("Менеджер контактов")
self.root.geometry("600x400")
self.contacts = []
self.selected_contact_index = None

self.load_contacts()
self.create_widgets()

def create_widgets(self):
frame = tk.Frame(self.root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tk.Label(frame, text="Имя:").grid(row=0, column=0, sticky=tk.W, pady=2)
self.entry_name = tk.Entry(frame, width=40)
self.entry_name.grid(row=0, column=1, columnspan=2, pady=2)

tk.Label(frame, text="Телефон:").grid(row=1, column=0, sticky=tk.W, pady=2)
self.entry_phone = tk.Entry(frame, width=20)
self.entry_phone.grid(row=1, column=1, pady=2)

tk.Label(frame, text="E-mail:").grid(row=2, column=0, sticky=tk.W, pady=2)
self.entry_email = tk.Entry(frame, width=40)
self.entry_email.grid(row=2, column=1, columnspan=2, pady=2)

ttk.Button(frame, text="Добавить контакт", command=self.add_contact).grid(row=3, column=1, pady=5)
ttk.Button(frame, text="Изменить контакт", command=self.edit_contact).grid(row=3, column=2, pady=5)

self.tree = ttk.Treeview(frame, columns=("name", "phone", "email"), show='headings')
self.tree.heading("name", text="Имя")
self.tree.heading("phone", text="Телефон")
self.tree.heading("email", text="E-mail")

yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
xscroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
self.tree.configure(yscroll=yscroll.set, xscroll=xscroll.set)

self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=5)
yscroll.grid(row=4, column=4, sticky='ns')
xscroll.grid(row=5, column=0, columnspan=4, sticky='ew')

self.tree.bind("<<TreeviewSelect>>", self.on_contact_select)

ttk.Button(frame, text="Удалить контакт", command=self.delete_contact).grid(row=6, column=1, pady=5)

frame.grid_rowconfigure(4, weight=1)
frame.grid_columnconfigure(1, weight=1)

def is_valid_phone(self, phone):
"""Проверяет, что телефон содержит только цифры и имеет длину от 10 до 15."""
return phone.isdigit() and 10 <= len(phone) <= 15

def is_valid_email(self, email):
"""Базовая проверка формата E-mail."""
return '@' in email and '.' in email

def is_email_unique(self, email_to_check):
"""Проверяет уникальность E-mail среди всех контактов.
Игнорирует текущий редактируемый контакт."""
for i, contact in enumerate(self.contacts):
if contact.get("email") == email_to_check and i != self.selected_contact_index:
return False
return True

def add_contact(self):
name = self.entry_name.get().strip()
phone = self.entry_phone.get().strip()
email = self.entry_email.get().strip()

if not name or not phone:
messagebox.showwarning("Ошибка", "Введите имя и телефон")
return

if not self.is_valid_phone(phone):
messagebox.showerror("Ошибка", "Неверный формат телефона. Введите от 10 до 15 цифр.")
return

if email and (not self.is_valid_email(email) or not self.is_email_unique(email)):
messagebox.showerror("Ошибка", "E-mail некорректен или уже используется другим контактом.")
return

contact = {
"name": name,
"phone": phone,
"email": email
}

self.contacts.append(contact)
self.update_tree()
self.save_contacts()

self.entry_name.delete(0, tk.END)
self.entry_phone.delete(0, tk.END)
self.entry_email.delete(0, tk.END)

def edit_contact(self):
if self.selected_contact_index is None:
messagebox.showwarning("Ошибка", "Выберите контакт для редактирования")
return

new_name = self.entry_name.get().strip()
new_phone = self.entry_phone.get().strip()

if not new_name or not new_phone:
messagebox.showwarning("Ошибка", "Имя и телефон не могут быть пустыми")
return

if not self.is_valid_phone(new_phone):
messagebox.showerror("Ошибка", "Неверный формат телефона. Введите от 10 до 15 цифр.")
return

new_email = self.entry_email.get().strip()

if new_email and (not self.is_valid_email(new_email) or not self.is_email_unique(new_email)):
messagebox.showerror("Ошибка", "E-mail некорректен или уже используется другим контактом.")
return

self.contacts[self.selected_contact_index]["name"] = new_name
self.contacts[self.selected_contact_index]["phone"] = new_phone
self.contacts[self.selected_contact_index]["email"] = new_email

self.update_tree()
self.save_contacts()

def update_tree(self):
for item in self.tree.get_children():
self.tree.delete(item)

for contact in self.contacts:
self.tree.insert("", "end", values=(contact["name"], contact["phone"], contact.get("email", "")))

def on_contact_select(self, event):
selected_items = self.tree.selection()
if not selected_items:
return

self.selected_contact_index = self.tree.index(selected_items[0])
contact = self.contacts[self.selected_contact_index]

self.entry_name.delete(0, tk.END)
self.entry_name.insert(0, contact["name"])

self.entry_phone.delete(0, tk.END)
self.entry_phone.insert(0, contact["phone"])

self.entry_email.delete(0, tk.END)
self.entry_email.insert(0, contact.get("email", ""))

def delete_contact(self):
if self.selected_contact_index is None:
messagebox.showwarning("Ошибка", "Выберите контакт для удаления")
return

del self.contacts[self.selected_contact_index]
self.selected_contact_index = None

self.update_tree()
self.save_contacts()

def save_contacts(self):
try:
with open(DATA_FILE, 'w', encoding='utf-8') as f:
json.dump(self.contacts, f, ensure_ascii=False, indent=4)
except Exception as e:
messagebox.showerror("Ошибка сохранения", str(e))

def load_contacts(self):
if os.path.exists(DATA_FILE):
try:
with open(DATA_FILE, 'r', encoding='utf-8') as f:
data = json.load(f)
if isinstance(data, list):
self.contacts = data
else:
raise ValueError("Некорректный формат данных в файле.")
except Exception as e:
messagebox.showerror("Ошибка загрузки", str(e))

if __name__ == "__main__":
root = tk.Tk()
app = ContactManagerApp(root)
root.mainloop()
