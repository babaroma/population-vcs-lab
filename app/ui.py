import tkinter as tk
from tkinter import filedialog, messagebox
from app.io_service import load_population_data


def run_app():
    root = tk.Tk()
    root.title("Population Forecast (Moving Average)")
    root.geometry("520x260")

    selected_file = tk.StringVar(value="")
    n_var = tk.StringVar(value="5")
    N_var = tk.StringVar(value="5")

    def choose_file():
        path = filedialog.askopenfilename(
            title="Выберите файл данных",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("JSON files", "*.json"),
            ],
        )
        if path:
            selected_file.set(path)

    def on_run():
        path = selected_file.get().strip()
        if not path:
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

        try:
            df = load_population_data(path)
        except Exception as e:
            messagebox.showerror("Ошибка загрузки файла", str(e))
            return

        messagebox.showinfo(
            "Файл загружен",
            f"Данные успешно загружены.\nКоличество записей: {len(df)}"
        )

    tk.Label(
        root,
        text="Вариант 5: население РФ и прогноз\n(скользящая средняя)",
        font=("Segoe UI", 11, "bold"),
        justify="center"
    ).pack(pady=10)

    frm_file = tk.Frame(root)
    frm_file.pack(pady=6, fill="x", padx=12)

    tk.Button(frm_file, text="Выбрать файл", command=choose_file).pack(side="left")
    tk.Label(frm_file, textvariable=selected_file, wraplength=360, justify="left").pack(side="left", padx=10)

    frm_params = tk.Frame(root)
    frm_params.pack(pady=10)

    tk.Label(frm_params, text="n (окно скользящей средней):").grid(row=0, column=0, sticky="e", padx=6, pady=4)
    tk.Entry(frm_params, textvariable=n_var, width=10).grid(row=0, column=1, padx=6, pady=4)

    tk.Label(frm_params, text="N (лет прогноза):").grid(row=1, column=0, sticky="e", padx=6, pady=4)
    tk.Entry(frm_params, textvariable=N_var, width=10).grid(row=1, column=1, padx=6, pady=4)

    tk.Button(
        root,
        text="Запустить расчёт",
        command=on_run,
        height=2,
        width=22
    ).pack(pady=12)

    root.mainloop()
