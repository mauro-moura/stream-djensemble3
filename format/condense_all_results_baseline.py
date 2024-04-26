import sqlite3
import pandas as pd
import sys,os

def condense(directory):
    dfs = []
    for filename in os.listdir(directory):
        if not filename.endswith('.db'):
            continue
        
        db_name = os.path.basename(filename)
        db_name = os.path.splitext(db_name)[0]
        conn = sqlite3.connect(directory + filename)
        
        # Define SQL query to select all columns from the table
        table_name = "exp_condensed"
        query = f"SELECT iteration, configuration, avg(error) AS '{db_name}' FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        dfs.append(df)

    # Merge all DataFrames into a single DataFrame
    result_df = dfs[0]
    for df in dfs[1:]:
        result_df = pd.merge(result_df, df, on=['configuration', 'iteration'], how='inner')

    new_conn = sqlite3.connect(f'{directory}merged_database.db')
    result_df.to_sql('sum_winner_error', new_conn, if_exists='replace', index=False)
    new_conn.close()

    # Display the final DataFrame
    print(result_df)

if __name__ == "__main__":
    #directory = sys.argv[1]
    directory = "output/query-results/2015/"
    condense(directory)