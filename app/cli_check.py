from app.io_service import load_population_data, take_last_years
from app.report_service import build_population_report


def main():
    path = "data/population_sample.csv"
    window = 5
    years = 5

    df = load_population_data(path)
    df = take_last_years(df, 15)

    report = build_population_report(df, window=window, years=years)

    extremes = report["extremes"]
    print("Загружено записей:", len(df))
    print("Макс. прирост: ", extremes["max_growth_year"], f'{extremes["max_growth_percent"]:.4f}%')
    print("Макс. убыль:  ", extremes["max_decline_year"], f'{extremes["max_decline_percent"]:.4f}%')

    print("\nПрогноз (первые 3 значения):")
    for y, v in list(zip(report["forecast_years"], report["forecast_values"]))[:3]:
        print(y, round(v))


if __name__ == "__main__":
    main()
