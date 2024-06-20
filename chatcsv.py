import os
import sys
import pandas as pd

def get_csv_from_args():
    if len(sys.argv) < 2:
        print("Usage: python chatcsv.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"{csv_file} does not exist. Available CSV files in the current directory:")
        for file in os.listdir('.'):
            if file.endswith('.csv'):
                print(file)
        sys.exit(1)
    
    return csv_file

def read_csv(csv_file):
    df = pd.read_csv(csv_file)
    meta_head = df.head().to_dict()
    meta_desc = df.describe().to_dict()
    meta_cols = df.columns.to_list()
    meta_dtype = df.dtypes.to_dict()

    print("First 5 rows:")
    print(meta_head)
    print("\nDescription:")
    print(meta_desc)
    print("\nColumns:")
    print(meta_cols)
    print("\nData Types:")
    print(meta_dtype)
    
    return df

def chat_csv(df):
    print("\nEnter SQL-like commands to interact with the CSV file. Type 'exit' to quit.")
    while True:
        command = input(">>> ").strip()
        if command.lower() == 'exit':
            break
        try:
            result = df.query(command)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    csv_file = get_csv_from_args()
    df = read_csv(csv_file)
    chat_csv(df)
