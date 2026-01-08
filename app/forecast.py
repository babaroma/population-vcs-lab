import pandas as pd


def moving_average_forecast(
    series: pd.Series,
    window: int,
    years: int
) -> list[float]:
    """
    Экстраполяция методом скользящей средней.
    - series: исходные значения (например, население за 15 лет)
    - window: n (размер окна)
    - years: N (сколько лет прогнозировать)

    Алгоритм итеративный:
    каждый следующий прогноз = среднее последних n значений
    (включая ранее спрогнозированные).
    """
    if years <= 0:
        return []

    values = [float(x) for x in series.tolist()]

    if window <= 0:
        raise ValueError("window (n) должно быть положительным числом")

    for _ in range(years):
        last_n = values[-window:] if len(values) >= window else values
        next_value = sum(last_n) / len(last_n)
        values.append(next_value)

    return values[-years:]


def build_forecast_years(last_year: int, years: int) -> list[int]:
    """
    Вспомогательная функция: список годов прогноза.
    """
    return [last_year + i for i in range(1, years + 1)]
