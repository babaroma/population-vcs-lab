import pandas as pd
from app.analytics import calculate_yearly_change, find_max_growth_decline
from app.forecast import moving_average_forecast, build_forecast_years
from app.analytics import calculate_yearly_change, find_max_growth_decline, find_max_abs_change


def build_population_report(df: pd.DataFrame, window: int, years: int) -> dict:
    """
    Собирает все результаты варианта 5 в один словарь:
    - table: DataFrame (year, population, change, percent)
    - extremes: max прирост/убыль (год и %)
    - forecast_years: годы прогноза
    - forecast_values: значения прогноза
    """
    df2 = calculate_yearly_change(df)

    # Округлим проценты для вывода (в расчётах можно оставлять как есть)
    df2["percent_rounded"] = df2["percent"].round(4)

    extremes = abs_extremes = find_max_abs_change(df2)


    last_year = int(df2["year"].max())
    forecast_years = build_forecast_years(last_year, years)
    forecast_values = moving_average_forecast(df2["population"], window, years)

    # Для UI удобно иметь округлённые значения прогноза
    forecast_values_rounded = [round(v) for v in forecast_values]

    return {
        "table": df2,
        "extremes": extremes,
        "forecast_years": forecast_years,
        "forecast_values": forecast_values,
        "forecast_values_rounded": forecast_values_rounded,
        "abs_extremes": abs_extremes,
    }
