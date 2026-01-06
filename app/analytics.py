import pandas as pd


def calculate_yearly_change(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет столбцы:
    - change: абсолютное изменение численности населения
    - percent: процентное изменение по сравнению с предыдущим годом
    """
    result = df.copy()
    result["change"] = result["population"].diff()
    result["percent"] = (result["change"] / result["population"].shift(1)) * 100
    return result


def find_max_growth_decline(df_with_percent: pd.DataFrame) -> dict:
    """
    Находит максимальный процент прироста и убыли населения.
    Первый год (NaN) игнорируется.
    """
    tmp = df_with_percent.dropna(subset=["percent"])

    max_growth = tmp.loc[tmp["percent"].idxmax()]
    max_decline = tmp.loc[tmp["percent"].idxmin()]

    return {
        "max_growth_year": int(max_growth["year"]),
        "max_growth_percent": float(max_growth["percent"]),
        "max_decline_year": int(max_decline["year"]),
        "max_decline_percent": float(max_decline["percent"]),
    }
