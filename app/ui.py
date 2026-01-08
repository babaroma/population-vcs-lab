import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

from app.io_service import load_population_data, take_last_years
from app.report_service import build_population_report


def run_app():
    root = tk.Tk()
    root.title("Population Forecast (Moving Average)")
    root.geometry("520x360")

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

    # Таблица: показываем ВСЕ столбцы отчёта (year, population, change, percent, percent_rounded)
    def show_table(df):
        table_window = tk.Toplevel()
        table_window.title("Данные о населении РФ")
        table_window.geometry("780x420")

        df_to_show = df.copy()
        if "percent" in df_to_show.columns:
            df_to_show["percent"] = df_to_show["percent"].round(4)

        columns = list(df_to_show.columns)
        tree = ttk.Treeview(table_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="center")

        scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for _, row in df_to_show.iterrows():
            vals = []
            for col in columns:
                v = row[col]
                if col in ("year",):
                    vals.append(int(v))
                elif col in ("population",):
                    vals.append(int(v) if v == v else "")  # NaN -> ""
                elif col in ("change",):
                    vals.append(int(v) if v == v else "")
                else:
                    # percent / percent_rounded и т.п.
                    vals.append("" if v != v else v)
            tree.insert("", "end", values=vals)

    def show_population_chart(df_fact, forecast_years, forecast_values):
        years = df_fact["year"].tolist()
        population = df_fact["population"].tolist()

        plt.figure()
        plt.plot(years, population, marker="o")

        if forecast_years and forecast_values:
            plt.plot(forecast_years, forecast_values, marker="o")

        plt.title("Численность населения РФ: факт и прогноз")
        plt.xlabel("Год")
        plt.ylabel("Численность населения")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def set_metrics_text(text: str):
        metrics_box.configure(state="normal")
        metrics_box.delete("1.0", tk.END)
        metrics_box.insert("1.0", text)
        metrics_box.configure(state="disabled")

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
            df = take_last_years(df, 15)
        except Exception as e:
            messagebox.showerror("Ошибка загрузки файла", str(e))
            return

        try:
            report = build_population_report(df, window=n, years=N)
        except Exception as e:
            messagebox.showerror("Ошибка расчётов", str(e))
            return

        # 1) Таблица — теперь показываем report["table"], где есть change/percent
        show_table(report["table"])

        # 2) Итоги анализа
        ex = report["extremes"]
        metrics_text = (
            "Итоги анализа:\n"
            f"Макс. % прироста: {ex['max_growth_year']} ({ex['max_growth_percent']:.4f}%)\n"
            f"Макс. % убыли:   {ex['max_decline_year']} ({ex['max_decline_percent']:.4f}%)"
        )
        set_metrics_text(metrics_text)

        # 3) График факт + прогноз
        show_population_chart(
            df,
            report["forecast_years"],
            report["forecast_values_rounded"],
        )

    # ---- UI ----
    tk.Label(
        root,
        text="Вариант 5: население РФ и прогноз\n(скользящая средняя)",
        font=("Segoe UI", 11, "bold"),
        justify="center",
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
        width=22,
    ).pack(pady=12)

    frm_metrics = tk.LabelFrame(root, text="Итоги анализа")
    frm_metrics.pack(fill="both", expand=True, padx=12, pady=8)

    metrics_box = tk.Text(frm_metrics, height=3, wrap="word", font=("Segoe UI", 10))
    metrics_box.pack(fill="both", expand=True, padx=8, pady=6)
    metrics_box.insert("1.0", "Итоги анализа появятся здесь после расчёта.")
    metrics_box.configure(state="disabled")

    root.mainloop()
