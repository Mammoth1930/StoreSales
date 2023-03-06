"""
This is the main file of the StoreSales project.

This is a simple application which ingests sales data from raw .csv files and
stores key information in a sqlite3 database. The information in the database
can also be exported to .xlsx to be analyses.

Author: Riley Farrell
Date: 03/03/2023
"""

import database as db
import ingest
import export

if (__name__=="__main__"):
    db.db_init()


