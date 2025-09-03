import pandas as pd
from .helper import clean_transaction_data, add_month_column


def load_excel(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    df = clean_transaction_data(df)
    df = add_month_column(df)
    return df
