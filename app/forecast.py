import pandas as pd


def moving_average_forecast(series: pd.Series, window: int, years: int) -> list:
    values = series.tolist()

    for _ in range(years):
        if len(values) < window:
            avg = sum(values) / len(values)
        else:
            avg = sum(values[-window:]) / window
        values.append(avg)

    return values[-years:]
