import tkinter as tk
from tkinter import filedialog, messagebox

def run_app():
    root = tk.Tk()
    root.title("Population Forecast (Moving Average)")
    root.geometry("520x240")

    selected_file = tk.StringVar(value="Файл не выбран")
    n_var = tk.StringVar(value="5")
    N_var = tk.StringVar(value="5")

    def choose_file():
        path = filedialog.askopenfilename(
            title="Выберите файл данных",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("JSON files", "*.json"),
                ("All files", "*.*"),
            ],
        )
        if path:
            selected_file.set(path)

    def on_run():
        if selected_file.get() == "Файл не выбран":
            messagebox.showwarning("Внимание", "Сначала выберите файл с данными.")
            return
        try:
            n = int(n_var.get())
            N = int(N_var.get())
            if n <= 0 or N <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "n и N должны быть положительными целыми числами.")
            return

        messagebox.showinfo(
            "Ок",
            f"Файл: {selected_file.get()}\nОкно n: {n}\nПрогноз N: {N}\n\nДальше подключим расчёты и графики."
        )

    tk.Label(root, text="Вариант 5: население РФ + прогноз скользящей средней", font=("Segoe UI", 11, "bold")).pack(pady=10)

    frm = tk.Frame(root)
    frm.pack(pady=6, fill="x", padx=12)

    tk.Button(frm, text="Выбрать файл", command=choose_file).pack(side="left")
    tk.Label(frm, textvariable=selected_file, wraplength=360, justify="left").pack(side="left", padx=10)

    frm2 = tk.Frame(root)
    frm2.pack(pady=10)

    tk.Label(frm2, text="n (окно):").grid(row=0, column=0, sticky="e", padx=6, pady=4)
    tk.Entry(frm2, textvariable=n_var, width=10).grid(row=0, column=1, padx=6, pady=4)

    tk.Label(frm2, text="N (лет прогноза):").grid(row=1, column=0, sticky="e", padx=6, pady=4)
    tk.Entry(frm2, textvariable=N_var, width=10).grid(row=1, column=1, padx=6, pady=4)

    tk.Button(root, text="Запустить расчёт", command=on_run, height=2, width=20).pack(pady=12)

    root.mainloop()
