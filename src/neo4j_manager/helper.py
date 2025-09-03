import pandas as pd


def clean_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    df['Debit Amount'] = df['Debit Amount'].fillna(0).astype(float)
    df['Credit Amount'] = df['Credit Amount'].fillna(0).astype(float)
    df['Description'] = df['Description'].fillna("No Description")
    df['Account Code'] = df['Account Code'].astype(str)
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors="coerce")
    return df


def add_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df['Month'] = df['Transaction Date'].dt.to_period('M').astype(str)
    return df
