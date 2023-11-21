import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cursor = None

    def connect(self):
        print("Establishing database connection...")
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.connection

    def execute_query(self, query):
        try:
            print(f"Executing query: {query}")
            self.cursor.execute(query)
            if query.strip().lower().startswith("select"):
                result = self.cursor.fetchall()
                print(f"Query result: {result}")
                return result
            else:
                print("Query executed successfully.")
        except Error as e:
            print(f"Error: {str(e)}")
            return f"Error: {str(e)}"

    def close(self):
        print("Closing database connection...")
        if self.cursor:
            self.cursor.close()
        self.connection.close()