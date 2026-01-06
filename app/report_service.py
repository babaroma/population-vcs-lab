import pandas as pd
from app.analytics import calculate_yearly_change, find_max_growth_decline
from app.forecast import moving_average_forecast, build_forecast_years


def build_population_report(df: pd.DataFrame, window: int, years: int) -> dict:
    """
    Собирает все результаты варианта 5 в один словарь:
    - таблица с percent/change
    - max прирост/убыль
    - прогноз (годы + значения)
    """
    df2 = calculate_yearly_change(df)
    extremes = find_max_growth_decline(df2)

    last_year = int(df2["year"].max())
    forecast_years = build_forecast_years(last_year, years)
    forecast_values = moving_average_forecast(df2["population"], window, years)

    return {
        "table": df2,  # DataFrame
        "extremes": extremes,  # dict
        "forecast_years": forecast_years,  # list[int]
        "forecast_values": forecast_values,  # list[float]
    }
