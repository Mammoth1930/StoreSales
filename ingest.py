"""
This file contains functions which are used to ingest data from the source files
to the sqlite3 database.
"""

import csv
import pandas as pd

import database as db

"""

"""
def ingest_data(fileName:str):
    df = parse_file(fileName)
    db.write_df_to_db(df, "SALES")

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
            #  neither do any of the lines that start with an empty string
            if i < 2 or line[0] == '':
                continue
            # This line should contain the extraction datetime
            elif i == 2:
                extractionDateTime = line[2]
            # This line should contain the column headers
            elif i == 4:
                dfColNames = line
            # This is only found at the end of the file and at this point the
            # is no more useful data.
            elif line[0] == "Receipt Number":
                break
            else:
                line.append(extractionDateTime)
                salesData.append(line)

    return pd.DataFrame(salesData, columns=dfColNames)
