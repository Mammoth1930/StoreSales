"""
This file contains functions which are used to ingest data from the source files
to the sqlite3 database.
"""

import csv
import pandas as pd
from tkinter.filedialog import askopenfilenames

from database import *

"""
Takes an appropriately formatted sales .csv file(s) and inserts the relevant
information into the database.
"""
def ingest_data():
    # Ask the user the files they want to ingest via file explorer.
    files = askopenfilenames(filetypes=[('CSV files', '.csv')])

    # For each file selected by the user, ingest it into the database.
    for file_name in files:
        df = parse_file(file_name)
        write_df_to_db(filter_product(df), "PRODUCTS")

        df['Quantity'] = pd.to_numeric(df['Quantity']).div(1000)
        df['Value'] = pd.to_numeric(df['Value']).div(100)

        write_df_to_db(df[["Code", "Quantity", "Value", "ExtractionDateTime"]], "SALES")

"""
Filters the input DataFrame to remove products which already exist in the
PRODUCTS table.

Params:
    df: The input DataFrame which will be filtered to contain only products
        missing from the PRODUCTS table.

Return:
    DataFrame: A filtered DataFrame which contains only products which are
        missing from the product table. The DataFrame also contains the columns
        which are useful for inserting into the PRODUCTS table.
"""
def filter_product(df:pd.DataFrame) -> pd.DataFrame:
    product_df = read_db_to_df("SELECT Code FROM PRODUCTS")
    missing_df = df[~df['Code'].isin(product_df['Code'])]
    return missing_df[['Code', 'Description']]

"""
Parses the sales .csv file and extracts all of the required information.

Params:
    fileName: The name of the .csv file to be ingested.

Return:
    DataFrame: A pandas DataFrame containing all the relevant data to be
        inserted into the SALES table.

"""
def parse_file(fileName:str) -> pd.DataFrame:

    extraction_datetime = None
    df_col_names = None
    sales_data = []    

    with open(fileName, "r") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            
            # These first few lines don't contain any useful information and
            # neither do any of the lines that start with an empty string.
            # We also ignore empty lines here.
            if i < 3 or not line or line[0] == '':
                continue
            # This line should contain the extraction datetime.
            elif line[0] == "Z-Reset Report":
                extraction_datetime = line[2]
            # This line should contain the column headers.
            elif line[0] == "Code":
                df_col_names = line
                df_col_names.append("ExtractionDateTime")
            # This is only found at the end of the file and at this point the
            # is no more useful data.
            elif line[0] == "Receipt Number":
                break
            else:
                line.append(extraction_datetime)
                sales_data.append(line)

    return pd.DataFrame(sales_data, columns=df_col_names)
