import os
import pandas as pd


def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # Приведём имена колонок к нижнему регистру (на случай "Year", "Population")
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    required = {"year", "population"}
    if not required.issubset(df.columns):
        raise ValueError("Файл должен содержать колонки: year, population")

    # Убираем строки с пустыми значениями
    df = df.dropna(subset=["year", "population"])

    # Приводим типы
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["population"] = pd.to_numeric(df["population"], errors="coerce")

    df = df.dropna(subset=["year", "population"])

    # Округлим население до целого (как правило это целое)
    df["population"] = df["population"].round().astype("int64")

    # Удалим дубликаты по году, оставим последнюю запись
    df = df.drop_duplicates(subset=["year"], keep="last")

    # Отсортируем по году
    df = df.sort_values("year").reset_index(drop=True)

    # Минимальные проверки здравого смысла
    if (df["year"] <= 0).any():
        raise ValueError("Некорректные значения года в файле.")
    if (df["population"] <= 0).any():
        raise ValueError("Некорректные значения численности населения в файле.")

    return df


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

    return _normalize_df(df)


def take_last_years(df: pd.DataFrame, years: int = 15) -> pd.DataFrame:
    """
    Возвращает последние N лет по году (если данных больше).
    Если данных меньше N — возвращает как есть.
    """
    if years <= 0:
        return df
    if len(df) <= years:
        return df
    return df.tail(years).reset_index(drop=True)
