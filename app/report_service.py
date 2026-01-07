import pandas as pd

from app.analytics import (
    calculate_yearly_change,
    find_max_growth_decline,
    find_max_abs_change,
)
from app.forecast import moving_average_forecast, build_forecast_years


def build_population_report(df: pd.DataFrame, window: int, years: int) -> dict:
    """
    Собирает все результаты варианта 5 в один словарь:
    - table: DataFrame (year, population, change, percent, percent_rounded)
    - extremes: max прирост/убыль (год и %)
    - abs_extremes: max рост/падение в абсолютных значениях
    - forecast_years: годы прогноза
    - forecast_values: значения прогноза
    - forecast_values_rounded: округлённый прогноз для UI
    """
    df2 = calculate_yearly_change(df)

    # округление для отображения
    df2["percent_rounded"] = df2["percent"].round(4)

    # ВАЖНО: percent-экстремумы и абсолютные экстремумы — это разные вещи
    extremes = find_max_growth_decline(df2)
    abs_extremes = find_max_abs_change(df2)

    last_year = int(df2["year"].max())
    forecast_years = build_forecast_years(last_year, years)
    forecast_values = moving_average_forecast(df2["population"], window, years)
    forecast_values_rounded = [round(v) for v in forecast_values]

    return {
        "table": df2,
        "extremes": extremes,
        "abs_extremes": abs_extremes,
        "forecast_years": forecast_years,
        "forecast_values": forecast_values,
        "forecast_values_rounded": forecast_values_rounded,
    }
