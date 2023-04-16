import sqlite3

dbname = 'mydb.db'
tablename = 'Tasks'

class TasksDb:
    def __init__(self):
        
        import os.path

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, dbname)

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def insert_task(self, link, src, desc):

        query = '''
            INSERT INTO {table} VALUES (null, '{link}', '{src}','{desc}', CURRENT_TIMESTAMP)
        '''.format(link=link,table=tablename, src=src, desc=desc)

        self.cursor.execute(query)
        self.conn.commit()

    def get_tasks(self):

        query = '''
            SELECT * FROM {table}
        '''.format(tablename=tablename, table=tablename)

        self.conn.row_factory = sqlite3.Row

        self.cursor.execute(query)

        result = self.cursor.fetchall()
        self.conn.commit()

        return result

    def close(self):
        self.conn.close()

if __name__ == "__main__":

    import os.path

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, dbname)

    #Connecting to sqlite
    conn = sqlite3.connect(dbname)

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Creating table as per requirement
    sql ='''
        CREATE TABLE "Tasks" (
            "id"	INTEGER,
            "link"	TEXT,
            "src"	TEXT NOT NULL,
            "desc"	TEXT,
            "date"	TEXT,
            PRIMARY KEY("id")
    );
    '''

    cursor.execute(sql)
    print("Table created successfully........")

    # Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

