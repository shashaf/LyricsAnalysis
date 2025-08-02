import os
import tkinter as tk
from tkinter import filedialog, ttk
from collections import Counter
import csv
import string

EXCLUDED_WORDS_FILE = "excluded_words_full.txt"


def load_excluded_words():
    excluded_words = set()
    if os.path.exists(EXCLUDED_WORDS_FILE):
        with open(EXCLUDED_WORDS_FILE, "r", encoding="utf-8") as file:
            excluded_words = {line.strip().lower() for line in file}
    return excluded_words


def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        process_files(folder_selected)


def process_files(folder):
    word_count = Counter()
    excluded_words = load_excluded_words()

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                text = file.read().lower()
                text = text.translate(str.maketrans("", "", string.punctuation + "\"'“”‘’«»"))
                words = text.split()
                words = [word for word in words if word not in excluded_words]
                word_count.update(words)

    display_results(word_count)


def display_results(word_count):
    for row in tree.get_children():
        tree.delete(row)

    for word, count in word_count.most_common():
        tree.insert("", "end", values=(word, count))


def save_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Слово", "Частота"])
            for row in tree.get_children():
                writer.writerow(tree.item(row)["values"])


root = tk.Tk()
root.title("Количественный анализ текстов")
root.geometry("500x400")

tk.Button(root, text="Выбрать папку", command=choose_folder).pack(pady=5)

columns = ("Слово", "Частота")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Слово", text="Слово")
tree.heading("Частота", text="Частота")
tree.pack(expand=True, fill="both", padx=5, pady=5)

tk.Button(root, text="Сохранить в CSV", command=save_to_csv).pack(pady=5)

root.mainloop()
