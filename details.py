import pandas as pd

# --- Step 1: Load Excel file ---
excel_path = r"" # replace with your file path
xls = pd.ExcelFile(excel_path)

# --- Step 2: Iterate through all sheets ---
summary = {}
for sheet_name in xls.sheet_names:
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    summary[sheet_name] = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "sample_data": df.head(3).to_dict(orient="records")
    }

# --- Step 3: Print summary for inspection ---
for sheet, details in summary.items():
    print(f"\n=== Sheet: {sheet} ===")
    print(f"Rows: {details['rows']}, Columns: {details['columns']}")
    print("Columns:", details["column_names"])
    print("Sample Data:", details["sample_data"])
