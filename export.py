"""
This file contains the functions that are used to export the information from
the database to an external .xlsx file.
"""

import pandas as pd
from tkinter.filedialog import asksaveasfilename

from database import *

# Options for the group by format of the export file. Columns can either be
# created for each extraction date, month or year.
GROUP_BY_OPTIONS = {
    'ExtractionDate': 'ExtractionDateTime',
    'Month': 'strftime("%m-%Y", ExtractionDateTime)',
    'Year': 'strftime("%Y", ExtractionDateTime)'
}

"""
Exports all the information in stored in the database into an excel file with a
format specified by the user. The user will be prompted to provide a location
to save the file.

Params:
    group_by_option: Specification on how the user would like the excel file to
    be formatted. It is expected that this parameter will a key of the
    GROUP_BY_OPTIONS dictionary.
"""
def export_data(group_by_option:str):
    # Create the dataframe for the data we are exporting.
    export_df = create_export_df(GROUP_BY_OPTIONS[group_by_option])

    # Prompt the user for a location to save the file in
    file_name = asksaveasfilename(filetypes=[('Excel files', '.xlsx')], defaultextension='.xlsx', initialfile='StoreSales.xlsx')

    # If the user provided a location then write the file there.
    if file_name != '':
        write_to_excel(file_name, export_df)

"""
Writes a dataframe to an excel file at the specified location.

Params:
    file_name: The full path of the file that's to be written.
    df: The dataframe that will have its information written to the excel file.
"""
def write_to_excel(file_name:str, df:pd.DataFrame):
    writer = pd.ExcelWriter(file_name)
    df.to_excel(writer, sheet_name='sales_data')

    # Auto adjust column width to be as wide as the data/headings.
    for col in df:
        col_width = max(df[col].astype(str).map(len).max(), len(col))
        col_index = df.columns.get_loc(col) + 1
        writer.sheets['sales_data'].set_column(col_index, col_index, col_width)

    writer.close()

"""
Creates the dataframe which is to be exported to the excel file. The dataframe
will contain all of the products in the database along with the quantity and
value which will be grouped as specified by time_filter. The dataframe will also
contain a totals column for the quantity and value. Finally a row with the
totals of each numeric column will be created as the last row of the dataframe.

Params:
    time_filter: The manner in which the quantity and value columns will be
    grouped. This is expected to be one of the values of the GROUP_BY_OPTIONS
    dictionary.

Return:
    DataFrame: The dataframe described above, based on the information in the
    database and the time_filter grouping parameter.
"""
def create_export_df(time_filter:str) -> pd.DataFrame:
    # Get all of the products in the database.
    result_df = read_db_to_df("SELECT * FROM PRODUCTS")
    # Grab the date aggregate.
    dates_df = read_db_to_df(
        f"SELECT {time_filter} FROM SALES GROUP BY {time_filter}"
    )

    # For each date aggregate return the quantity and value of each product.
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

    # Create a totals column for both quantity and value.
    quantity_cols = [col for col in result_df if col.startswith('Quantity')]
    result_df['Quantity_total'] = result_df[quantity_cols].sum(axis=1)

    value_cols = [col for col in result_df if col.startswith('Value')]
    result_df['Value_total'] = result_df[value_cols].sum(axis=1)

    # Create a row of totals for each of the date aggregate columns and the two
    # totals columns.
    totals_row = ['', '']
    for i, col in enumerate(result_df):
        if i > 1:
            totals_row.append(result_df[col].sum(axis=0))

    result_df.loc['Total'] = totals_row

    return result_df