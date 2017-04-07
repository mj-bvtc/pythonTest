import mysql.connector
import common
import pandas as pd


def open_close(fn):
    def wrapped(self, *args, **kwargs):
        try:
            print("opening connection...")
            self.open()
            fn(self, *args, **kwargs)
        finally:
            self.close()
            print("...closed connection")
    return wrapped


class Database(common.Common):
    """mysql database connection and functions"""
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.is_connected = None
        self.user = "MK"
        self.password = "6860"
        self.host = "127.0.0.1"
        self.database = "bvtc"

    def open(self):
        self.connection = mysql.connector.connect(user=self.user,
                                                  password=self.password,
                                                  host=self.host,
                                                  database=self.database)
        return self.connection

    def close(self):
        self.connection.close()

    @open_close
    def insert_block(self, guid, style, style_number):

        query = f"""    
            insert into bvtc.blocks 
                (guid, style, style_number)
            values 
                ("{guid}", "{style}", {style_number})   

            """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    @open_close
    def insert_style(self, style, code, coefficient):

        query = f"""    
            insert into bvtc.style_guide 
                (style, code, coefficient)
            values 
                ("{style}", "{code}", {coefficient})   

            """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    @open_close
    def print_table(self):
        query = "select * from bvtc.blocks"
        df = pd.read_sql(query, self.open())
        print(df)

    def csv_to_sql(self):
        csv = open(r"V:\MeshLab\_FieldSurvey\MK\Spreadsheets\BLOCK_STYLES.csv", "r")

        for line in csv:
            style, code, coefficient = line.split(",")
            self.insert_style(style, code, coefficient)


def main():
    db = Database()
    db.insert_style("Brackeet", "BKK", 2.011)


if __name__ == "__main__":
    main()
