"""
This file contains functions which are used to ingest data from the source files
to the sqlite3 database.
"""

import csv
import pandas as pd

from database import *

"""

"""
def ingest_data(fileName:str):
    df = parse_file(fileName)
    write_df_to_db(df[["Code", "Description"]], "PRODUCTS")
    write_df_to_db(df[["Code", "Quantity", "Value", "ExtractionDateTime"]], "SALES")

"""
Parses the sales .csv file and extracts all of the required information.

Params:
    fileName: The name of the .csv file to be ingested.

Return:
    DataFrame: A pandas DataFrame containing all the relevant data to be
        inserted into the SALES table.

"""
def parse_file(fileName:str) -> pd.DataFrame:

    extractionDateTime = None
    dfColNames = None
    salesData = []    

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
                extractionDateTime = line[2]
            # This line should contain the column headers.
            elif line[0] == "Code":
                dfColNames = line
                dfColNames.append("ExtractionDateTime")
            # This is only found at the end of the file and at this point the
            # is no more useful data.
            elif line[0] == "Receipt Number":
                break
            else:
                # ToDo remove this
                # for data in salesData:
                #     if line[0] == data[0]:
                #         print(f"Key violation {line[0]}")
                line.append(extractionDateTime)
                salesData.append(line)

    return pd.DataFrame(salesData, columns=dfColNames)
