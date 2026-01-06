import pandas as pd
import os


def load_population_data(path: str) -> pd.DataFrame:
    _, ext = os.path.splitext(path.lower())

    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext == ".xlsx":
        df = pd.read_excel(path)
    elif ext == ".json":
        df = pd.read_json(path)
    else:
        raise ValueError("Неподдерживаемый формат файла")

    required_columns = {"year", "population"}
    if not required_columns.issubset(df.columns):
        raise ValueError("Файл должен содержать колонки: year, population")

    df = df.sort_values("year")
    return df
