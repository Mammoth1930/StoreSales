"""
This is the main file of the StoreSales project.

This is a simple application which ingests sales data from raw .csv files and
stores key information in a sqlite3 database. The information in the database
can also be exported to .xlsx to be analyses.

Author: Riley Farrell
Date: 03/03/2023
"""

from tabulate import tabulate

from database import *
from ingest import *
from export import *

if (__name__=="__main__"):
    db_init()
    ingest_data("C:/StoreSales/Data/TestData1.CSV")
    df = read_db_to_df("SELECT * FROM SALES")
    print(tabulate(df, headers='keys', tablefmt='psql'))
    print(tabulate(read_db_to_df("SELECT * FROM PRODUCTS"), headers='keys', tablefmt='psql'))
