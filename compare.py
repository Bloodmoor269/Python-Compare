import tkinter as tk
from tkinter import scrolledtext, messagebox
import keyboard

def process_text(text):
    """Обработка текста: оставить только часть до первого пробела."""
    lines = text.strip().split('\n')
    processed_lines = []
    for line in lines:
        # Если есть пробел, берем часть до него, иначе оставляем строку как есть
        if ' ' in line:
            processed_lines.append(line.split(' ', 1)[0])  # Разделяем по первому пробелу
        else:
            processed_lines.append(line)
    return processed_lines


def compare_texts():
    yesterday_text = yesterday_input.get("1.0", tk.END)
    today_text = today_input.get("1.0", tk.END)

    # Обработка текста
    yesterday_lines = process_text(yesterday_text)
    today_lines = process_text(today_text)

    # Найти уникальные строки во вчерашнем тексте
    unique_lines = sorted(set(yesterday_lines) - set(today_lines))

    # Очистить поле результата и вывести уникальные строки
    result_output.delete("1.0", tk.END)
    if unique_lines:
        result_output.insert(tk.END, "Точки вышедшие в доступ:\n")
        for unique_line in unique_lines:
            result_output.insert(tk.END, f"{unique_line}\n")
    else:
        result_output.insert(tk.END, "Точек вышедших в доступ - нет")


def compare_texts_by_lines():
    """Сравнить тексты построчно."""
    yesterday_text = yesterday_input.get("1.0", tk.END)
    today_text = today_input.get("1.0", tk.END)

    # Разделение на строки
    yesterday_lines = yesterday_text.strip().split('\n')
    today_lines = today_text.strip().split('\n')

    # Найти уникальные строки во вчерашнем тексте
    unique_lines = sorted(set(yesterday_lines) - set(today_lines))

    # Очистить поле результата и вывести уникальные строки
    result_output.delete("1.0", tk.END)
    if unique_lines:
        result_output.insert(tk.END, "Точки вышедшие в доступ:\n")
        for unique_line in unique_lines:
            result_output.insert(tk.END, f"{unique_line}\n")
    else:
        result_output.insert(tk.END, "Точек вышедших в доступ - нет")


def clear_yesterday():
    yesterday_input.delete("1.0", tk.END)


def clear_today():
    today_input.delete("1.0", tk.END)


def copy_text():
    """Копирование выделенного текста в буфер обмена."""
    try:
        focused_widget = window.focus_get()
        if isinstance(focused_widget, tk.Text):
            window.clipboard_clear()
            window.clipboard_append(focused_widget.get("sel.first", "sel.last"))
            window.update()  # Синхронизировать буфер обмена
    except tk.TclError:
        pass  # Ничего не выделено


def paste_text():
    """Вставка текста из буфера обмена."""
    try:
        focused_widget = window.focus_get()
        if isinstance(focused_widget, tk.Text):
            focused_widget.insert(tk.INSERT, window.clipboard_get())
    except tk.TclError:
        pass  # Буфер обмена пуст


# Создание основного окна
window = tk.Tk()
window.title("Доступность точек")

# Открытие окна во весь экран
window.state('zoomed')

# Настройка сетки для растягивания колонок
window.grid_columnconfigure(0, weight=1)  # Левая колонка (для "Вчера")
window.grid_columnconfigure(1, weight=1)  # Правая колонка (для "Сегодня")
window.grid_rowconfigure(1, weight=1)  # Строка для растяжения текстовых полей
window.grid_rowconfigure(3, weight=1)  # Строка для результата

# Поля для ввода текста "вчера"
yesterday_label = tk.Label(window, text="Список недоступных точек за вчерашний день:")
yesterday_label.grid(row=0, column=0, padx=10, pady=5, sticky="nw")

# Кнопка для очистки текста "Вчера"
clear_yesterday_button = tk.Button(window, text="Очистить", command=clear_yesterday, width=15)
clear_yesterday_button.grid(row=1, column=0, pady=5)

yesterday_input = scrolledtext.ScrolledText(window, width=40, height=38)
yesterday_input.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

# Поля для ввода текста "сегодня"
today_label = tk.Label(window, text="Список недоступных точек за сегодняшний день:")
today_label.grid(row=0, column=1, padx=10, pady=5, sticky="nw")

# Кнопка для очистки текста "Сегодня"
clear_today_button = tk.Button(window, text="Очистить", command=clear_today, width=15)
clear_today_button.grid(row=1, column=1, pady=5)

today_input = scrolledtext.ScrolledText(window, width=40, height=38)
today_input.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

# Кнопка для сравнения
compare_button = tk.Button(window, text="Сравнить по ID", command=compare_texts, width=15)
compare_button.grid(row=3, column=0, pady=5)

# Новая кнопка "Сравнить по строкам"
compare_lines_button = tk.Button(window, text="Сравнить по строкам", command=compare_texts_by_lines, width=20)
compare_lines_button.grid(row=3, column=1, pady=5)

# Поле для вывода результата
result_label = tk.Label(window, text="Результат:")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nw")

result_output = scrolledtext.ScrolledText(window, width=80, height=15)
result_output.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# Добавление глобальных горячих клавиш для копирования и вставки
keyboard.add_hotkey("ctrl+c", copy_text)
keyboard.add_hotkey("ctrl+v", paste_text)

# Запуск главного цикла приложения
window.mainloop()
