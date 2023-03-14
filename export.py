"""
This file contains the functions that are used to export the information from
the database to an external .xlsx file.
"""

import pandas as pd
from tabulate import tabulate

from database import *


"""

"""
def export_data():
    export_df = create_export_df("ExtractionDateTime")
    print(tabulate(export_df[:100], headers='keys', tablefmt='psql'))

"""

"""
def create_export_df(time_filter:str) -> pd.DataFrame:
    # Get all of the products in the database
    result_df = read_db_to_df("SELECT * FROM PRODUCTS")
    # Grab the date aggregate
    dates_df = read_db_to_df(
        f"SELECT {time_filter} FROM SALES GROUP BY {time_filter}"
    )

    # For each date aggregate return the quantity and value of each product
    for index, row in dates_df.iterrows():
        date = row[0]
        totals_df = read_db_to_df(
            "SELECT Code, Quantity, Value " 
            "FROM SALES "
            f"WHERE {time_filter} = '{date}'"
        )
        date_str = date.split('T')[0]
        totals_df = totals_df.groupby('Code').sum().rename(
            {'Quantity': f'Quantity_{date_str}','Value': f'Value_{date_str}'}, axis=1
        )
        result_df = result_df.merge(totals_df, how='left', on='Code')

    result_df = result_df.fillna(0)

    # Create a totals column for both quantity and value
    quantity_cols = [col for col in result_df if col.startswith('Quantity')]
    # print(result_df[quantity_cols])
    value_cols = [col for col in result_df if col.startswith('Value')]
    # print(value_cols)
    result_df['Quantity_total'] = result_df[quantity_cols].sum(axis=1)
    result_df['Value_total'] = result_df[value_cols].sum(axis=1)

    # Create a row of totals for each of the date aggregate columns and the two
    # totals columns
     

    return result_df