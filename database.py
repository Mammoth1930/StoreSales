import sqlite3

# sqlite3 database file name
DB_FILE = "sales.db"

"""
Performs initial database setup operations such as connecting to the database
and creating the tables if they don't already exist.
"""
def db_init():
    # Establish connection to sqlite database
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    # Create a table to store the sales information inside of
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS SALES(
            ProductCode INTEGER NOT NULL,
            Description TEXT,
            Quantity INTEGER,
            Value INTEGER,
            ExtractionDateTime DATETIME,
            PRIMARY KEY (ProductCode)
        )
        '''
    )

