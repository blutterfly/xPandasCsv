# cPandas CSV

As a seasoned Python Developer expert in Pandas.  
1. Create a CLI program to chat with a CSV file.  {chatcsv.py}
2. Function: def get_csv_from_args the {csv_file}
   Check {csv_file} exists.  If not list the csv files in the current directory
3. Function: def read_csv
   Read CSV and display metadata
   df = pd.read_csv(uploaded_file)
   meta_head = str(df.head().to_dict())
   meta_desc = str(df.describe().to_dict())
   meta_cols = str(df.columns.to_list())
   meta_dtype = str(df.dtypes.to_dict())
4. Function: def chat_csv
   Create commands using SQL like syntax.
   
   
