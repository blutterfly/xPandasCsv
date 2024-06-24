import os
import sys
import pandas as pd
import duckdb
from tabulate import tabulate

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
    
    # Replace 'bs_percentage' with 'bspct'
    if 'bs_percentage' in df.columns:
        df.rename(columns={'bs_percentage': 'bspct'}, inplace=True)
    
    meta_head = df.head()
    meta_desc = df.describe()
    meta_cols = df.columns.to_list()
    meta_dtype = df.dtypes.to_dict()

    print("First 5 rows:")
    print(tabulate(meta_head, headers='keys', tablefmt='plain'))
    print("\nDescription:")
    print(tabulate(meta_desc, headers='keys', tablefmt='plain'))
    print("\nColumns:")
    print(meta_cols)
    print("\nData Types:")
    print(meta_dtype)
    
    return df

def chat_csv(df):
    con = duckdb.connect(database=':memory:')
    con.register('csv_table', df)
    
    print("\nEnter SQL commands to interact with the CSV file. Type 'exit' to quit.")
    while True:
        command = input(">>> ").strip()
        if command.lower() == 'exit':
            break
        try:
            result = con.execute(command).df()
            print(tabulate(result, headers='keys', tablefmt='plain'))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    csv_file = get_csv_from_args()
    df = read_csv(csv_file)
    chat_csv(df)
&*