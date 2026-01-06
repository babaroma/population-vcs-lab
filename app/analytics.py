import pandas as pd


def calculate_yearly_change(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["change"] = result["population"].diff()
    result["percent"] = result["change"] / result["population"].shift(1) * 100
    return result
