"""
This file contains functions which operate on the sqlite3 database.
"""

import sqlite3
import pandas as pd

# sqlite3 database file name
DB_FILE = "sales.db"

# Establish connection to sqlite database
DB_CON = sqlite3.connect(DB_FILE)

"""
Performs initial database setup operations such as connecting to the database
and creating the tables if they don't already exist.
"""
def db_init():
    DB_CON.execute(
        '''
        CREATE TABLE IF NOT EXISTS PRODUCTS(
            Code TEXT,
            Description TEXT,
            PRIMARY KEY (Code)
        )
        '''
    )
    
    DB_CON.execute(
        '''
        CREATE TABLE IF NOT EXISTS SALES(
            Code TEXT,
            Quantity INTEGER,
            Value INTEGER,
            ExtractionDateTime DATETIME,
            PRIMARY KEY (Code, ExtractionDateTime),
            FOREIGN KEY (Code) REFERENCES PRODUCTS (Code)
        )
        '''
    )
    DB_CON.commit()

"""
Writes information from a DataFrame to an existing sqlite table.

Params:
    df: DataFrame containing the information to be written.
   
    tableName: Name of the sqlite table we want the DataFrame info to be
        written to.
"""
def write_df_to_db(df:pd.DataFrame, tableName:str):
    df.to_sql(tableName, DB_CON, index=False, if_exists='append')

"""
Executes an SQL query and returns the result as a DataFrame.

Params:
    query: The SQL query to be executed.

Return:
    DataFrame: A pandas DataFrame containing the result of the SQL query.
"""
def read_db_to_df(query:str) -> pd.DataFrame:
    return pd.read_sql_query(query, DB_CON)


