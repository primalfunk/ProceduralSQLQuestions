from faker import Faker
import random
from templates import SQLChallengeTemplates

class ChallengeManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.current_challenge = None
        self.current_schema = None  # Store the current schema name
        self.current_window_function = None  # Store the current window function
        self.schemas = {
            'product': [
                "CREATE TABLE IF NOT EXISTS product (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price DECIMAL(10,2), category VARCHAR(255), launch_date DATE)"
            ],
            'user': [
                "CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), email VARCHAR(255), order_count INT, join_date DATE, language ENUM('English', 'Spanish', 'Chinese', 'Russian', 'French', 'Arabic', 'Dutch', 'Japanese'))"
            ],
            'customer': [
                "CREATE TABLE IF NOT EXISTS customer (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255), loyalty ENUM('bronze', 'silver', 'gold', 'platinum'), last_order DATE, order_total DECIMAL(10, 2))"
            ],
            'employee': [
                "CREATE TABLE IF NOT EXISTS employee (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), position VARCHAR(50), salary DECIMAL(10,2), hire_date DATE)"
            ],
            'sales': [
                "CREATE TABLE IF NOT EXISTS sales (id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, customer_id INT, sale_amount DECIMAL(10,2), sale_date DATE)"
            ]
        }
        self.faker = Faker()

    def load_challenge(self):
        # Randomly select a schema and a window function
        print("Loading new challenge...")

        self.current_schema = random.choice(list(self.schemas.keys()))
        print(f"Selected schema: {self.current_schema}")
        self.current_window_function = random.choice(['SUM() OVER()', 'ROW_NUMBER()', 'AVG() OVER()', 'COUNT() OVER()', 'RANK()', 'LEAD()', 
                                         'LAG()', 'FIRST_VALUE()', 'LAST_VALUE()', 'NTH_VALUE()', 'PERCENT_RANK()', 'CUME_DIST()', 
                                         'PERCENTILE_CONT()', 'PERCENTILE_DISC()'])
        print(f"Selected window function: {self.current_window_function}")

        self.create_tables(self.current_schema)
        self.refill_tables(self.current_schema)

        challenge_template = SQLChallengeTemplates(self.current_schema)
        self.current_challenge = challenge_template.generate_challenge(self.current_window_function)

        print(f"Generated challenge: {self.current_challenge}")
        return self.current_challenge

    def create_tables(self, schema_name):
        print(f"Creating tables for schema: {schema_name}")
        queries = self.schemas[schema_name]
        for query in queries:
            self.db_manager.execute_query(query)

    def refill_tables(self, schema_name):
        # Empty the tables
        print(f"Emptying existing tables...")
        self.db_manager.execute_query(f"DELETE FROM {schema_name}")
        print(f"Refilling tables for schema: {schema_name}")
        if schema_name == 'product':
            self.fill_product_table()
        elif schema_name == 'user':
            self.fill_user_table()
        elif schema_name == 'customer':
            self.fill_customer_table()
        elif schema_name == 'employee':
            self.fill_employee_table()
        elif schema_name == 'sales':
            self.fill_sales_table()

    def fill_product_table(self):
        for _ in range(100):
            product_name = self.faker.catch_phrase()
            price = round(random.uniform(10, 500), 2)
            category = random.choice(['Electronics', 'Books', 'Clothing', 'Home'])
            launch_date = self.faker.date_between(start_date='-12y', end_date='today')
            insert_query = f"INSERT INTO product (name, price, category, launch_date) VALUES ('{product_name}', {price}, '{category}', '{launch_date}')"
            self.db_manager.execute_query(insert_query)

    def fill_user_table(self):
        for _ in range(100):
            username = self.faker.user_name()
            email = self.faker.email()
            join_date = self.faker.date_between(start_date='-10y', end_date='today')
            order_count = random.uniform(1, 1000)
            language = random.choice(['English', 'Spanish', 'Chinese', 'Russian', 'French', 'Arabic', 'Dutch', 'Japanese'])
            insert_query = f"INSERT INTO user (username, email, order_count, join_date) VALUES ('{username}', '{email}', {order_count}, '{join_date}', '{language}')"
            self.db_manager.execute_query(insert_query)

    def fill_customer_table(self):
        for _ in range(100):
            name = self.faker.name()
            address = self.faker.address()
            loyalty = random.choice(['bronze', 'silver', 'gold', 'platinum'])
            last_order = self.faker.date_between(start_date='-3y', end_date='today')
            order_total = round(random.uniform(20, 25000), 2)
            insert_query = f"INSERT INTO customer (name, address, loyalty) VALUES ('{name}', '{address}', '{loyalty}', '{last_order}', {order_total})"
            self.db_manager.execute_query(insert_query)

    def fill_employee_table(self):
        positions = ['Manager', 'Sales Associate', 'Clerk', 'Supervisor', 'Yoga Instructor']
        for _ in range(100):
            name = self.faker.name()
            position = random.choice(positions)
            salary = round(random.uniform(30000, 80000), 2)
            hire_date = self.faker.date_between(start_date='-5y', end_date='today')
            insert_query = f"INSERT INTO employee (name, position, salary, hire_date) VALUES ('{name}', '{position}', {salary}, '{hire_date}')"
            self.db_manager.execute_query(insert_query)

    def fill_sales_table(self):
        for _ in range(100):
            product_id = random.randint(1, 100)
            customer_id = random.randint(1, 100)
            sale_amount = round(random.uniform(20, 1000), 2)
            sale_date = self.faker.date_between(start_date='-1y', end_date='today')
            insert_query = f"INSERT INTO sales (product_id, customer_id, sale_amount, sale_date) VALUES ({product_id}, {customer_id}, {sale_amount}, '{sale_date}')"
            self.db_manager.execute_query(insert_query)

    def get_ascii_representation(self, schema_name):
        ascii_art = f"Schema: {schema_name}\n"
        for query in self.schemas[schema_name]:
            table_name = query.split()[5]
            ascii_art += f"Table: {table_name}\n"
            columns_str = self._extract_columns_str(query)
            columns = self._parse_columns(columns_str)
            for col in columns:
                ascii_art += f"  - {col.strip()}\n"
            ascii_art += "\n"
        return ascii_art

    def _extract_columns_str(self, query):
        start = query.find('(') + 1
        end = query.rfind(')')
        return query[start:end]

    def _parse_columns(self, columns_str):
        columns = []
        current_column = ''
        bracket_level = 0
        for char in columns_str:
            if char == ',' and bracket_level == 0:
                columns.append(current_column.strip())
                current_column = ''
            else:
                current_column += char
                if char == '(':
                    bracket_level += 1
                elif char == ')':
                    bracket_level -= 1
        if current_column:
            columns.append(current_column.strip())
        return columns
    
    def validate_answer(self, user_query):
        user_result = self.db_manager.execute_query(user_query)
        correct_result = self.db_manager.execute_query(self.current_challenge['sql'])
        return user_result == correct_result