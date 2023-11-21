class SQLChallengeTemplates:
    def __init__(self, table_name):
        self.table_name = table_name

    def generate_challenge(self, window_function):
        method_suffix = window_function.lower().replace('()', '')
        method_name = f"{method_suffix}_{self.table_name}"
        print(f"Trying to call method: {method_name}")
        challenge_method = getattr(self, method_name, None)
        if challenge_method:
            return challenge_method()
        else:
            raise NotImplementedError(f"Challenge for {window_function} not implemented for {self.table_name}")

    # Product table templates
    def sum_over_product(self):
        question = "What is the total cumulative price of all products by the most recent launch date?"
        sql = "SELECT MAX(SUM(price) OVER (ORDER BY launch_date)) FROM product"
        return question, sql

    def row_number_product(self):
        question = "What is the ranking position of the most expensive product in the entire product table?"
        sql = "SELECT MAX(ROW_NUMBER() OVER (ORDER BY price DESC)) FROM product"
        return question, sql

    def avg_over_product(self):
        question = "What is the overall average price of products considering the latest launch date?"
        sql = "SELECT MAX(AVG(price) OVER (ORDER BY launch_date)) FROM product"
        return question, sql

    def count_over_product(self):
        question = "As of the latest launch date, how many products have been launched in total?"
        sql = "SELECT MAX(COUNT(*) OVER (ORDER BY launch_date)) FROM product"
        return question, sql

    def rank_product(self):
        question = "In the category with the most products, what is the highest rank based on price?"
        sql = "SELECT MAX(RANK() OVER (PARTITION BY category ORDER BY price DESC)) FROM product"
        return question, sql

    def lead_product(self):
        question = "What is the price difference between the most expensive product and the subsequent product launched?"
        sql = "SELECT MAX(price - LEAD(price) OVER (ORDER BY price DESC, launch_date)) FROM product WHERE price IS NOT NULL"
        return question, sql

    def lag_product(self):
        question = "Find the price difference between each product and the product launched immediately before it, ordered by launch date."
        sql = "SELECT MAX(price - LAG(price) OVER (ORDER BY launch_date)) FROM product WHERE price IS NOT NULL"
        return question, sql

    def first_value_product(self):
        question = "What is the highest initial launch price recorded in any product category?"
        sql = "SELECT MAX(FIRST_VALUE(price) OVER (PARTITION BY category ORDER BY launch_date)) FROM product"
        return question, sql

    def last_value_product(self):
        question = "Among the final products launched in each category, what is the lowest launch price?"
        sql = "SELECT MIN(LAST_VALUE(price) OVER (PARTITION BY category ORDER BY launch_date ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)) FROM product"
        return question, sql

    def nth_value_product(self):
        question = "What is the highest launch price of the third product in any category?"
        sql = "SELECT MAX(NTH_VALUE(price, 3) OVER (PARTITION BY category ORDER BY launch_date)) FROM product"
        return question, sql

    def percent_rank_product(self):
        question = "Within each category, what is the maximum percentile rank based on the price of products?"
        sql = "SELECT MAX(PERCENT_RANK() OVER (PARTITION BY category ORDER BY price DESC)) FROM product"
        return question, sql

    def cume_dist_product(self):
        question = "For the most expensive product in its category, what is its cumulative distribution?"
        sql = "SELECT MAX(CUME_DIST() OVER (PARTITION BY category ORDER BY price DESC)) FROM product"
        return question, sql

    def percentile_cont_product(self):
        question = "Across all categories, what is the highest median price?"
        sql = "SELECT MAX(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) OVER (PARTITION BY category)) FROM product"
        return question, sql

    def percentile_disc_product(self):
        question = "What is the maximum discrete median price across all product categories?"
        sql = "SELECT MAX(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY price) OVER (PARTITION BY category)) FROM product"
        return question, sql
    
    # User table templates
    def sum_over_user(self):
        question = "What is the total cumulative order count for all users as of the most recent join date?"
        sql = "SELECT MAX(SUM(order_count) OVER (ORDER BY join_date)) FROM user"
        return question, sql

    def row_number_user(self):
        question = "What is the position of the user with the highest order count?"
        sql = "SELECT MAX(ROW_NUMBER() OVER (ORDER BY order_count DESC)) FROM user"
        return question, sql

    def avg_over_user(self):
        question = "What is the average order count for users as of the most recent join date?"
        sql = "SELECT MAX(AVG(order_count) OVER (ORDER BY join_date)) FROM user"
        return question, sql

    def count_over_user(self):
        question = "How many users have joined up to the most recent join date?"
        sql = "SELECT MAX(COUNT(*) OVER (ORDER BY join_date)) FROM user"
        return question, sql

    def rank_user(self):
        question = "Among all languages, what is the highest rank based on order count?"
        sql = "SELECT MAX(RANK() OVER (PARTITION BY language ORDER BY order_count DESC)) FROM user"
        return question, sql

    def lead_user(self):
        question = "What is the order count difference between the user with the most orders and the next user?"
        sql = "SELECT MAX(order_count - LEAD(order_count) OVER (ORDER BY order_count DESC)) FROM user WHERE order_count IS NOT NULL"
        return question, sql

    def lag_user(self):
        question = "What is the order count difference between a user and the user who joined just before them, sorted by join date?"
        sql = "SELECT MAX(order_count - LAG(order_count) OVER (ORDER BY join_date)) FROM user WHERE order_count IS NOT NULL"
        return question, sql

    def first_value_user(self):
        question = "What is the highest initial order count recorded for any language group?"
        sql = "SELECT MAX(FIRST_VALUE(order_count) OVER (PARTITION BY language ORDER BY join_date)) FROM user"
        return question, sql

    def last_value_user(self):
        question = "What is the lowest order count among the latest users who joined in each language group?"
        sql = "SELECT MIN(LAST_VALUE(order_count) OVER (PARTITION BY language ORDER BY join_date ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)) FROM user"
        return question, sql

    def nth_value_user(self):
        question = "What is the highest order count of the third user who joined in any language group?"
        sql = "SELECT MAX(NTH_VALUE(order_count, 3) OVER (PARTITION BY language ORDER BY join_date)) FROM user"
        return question, sql

    def percent_rank_user(self):
        question = "What is the maximum percentile rank of users based on order count within each language group?"
        sql = "SELECT MAX(PERCENT_RANK() OVER (PARTITION BY language ORDER BY order_count DESC)) FROM user"
        return question, sql

    def cume_dist_user(self):
        question = "For the user with the highest order count in their language group, what is their cumulative distribution?"
        sql = "SELECT MAX(CUME_DIST() OVER (PARTITION BY language ORDER BY order_count DESC)) FROM user"
        return question, sql

    def percentile_cont_user(self):
        question = "Across all language groups, what is the highest median order count?"
        sql = "SELECT MAX(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_count) OVER (PARTITION BY language)) FROM user"
        return question, sql

    def percentile_disc_user(self):
        question = "What is the maximum discrete median order count across all language groups?"
        sql = "SELECT MAX(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY order_count) OVER (PARTITION BY language)) FROM user"
        return question, sql
    
    # Customer table templates
    def sum_over_customer(self):
        question = "What is the total cumulative amount spent by all customers as of the most recent order?"
        sql = "SELECT MAX(SUM(order_total) OVER (ORDER BY last_order)) FROM customer"
        return question, sql

    def row_number_customer(self):
        question = "What is the position of the customer who spent the most in total?"
        sql = "SELECT MAX(ROW_NUMBER() OVER (ORDER BY order_total DESC)) FROM customer"
        return question, sql

    def avg_over_customer(self):
        question = "What is the average amount spent by customers as of the most recent order date?"
        sql = "SELECT MAX(AVG(order_total) OVER (ORDER BY last_order)) FROM customer"
        return question, sql

    def count_over_customer(self):
        question = "How many customers have placed orders up to the most recent order date?"
        sql = "SELECT MAX(COUNT(*) OVER (ORDER BY last_order)) FROM customer"
        return question, sql

    def rank_customer(self):
        question = "What is the highest rank in order total among all loyalty levels?"
        sql = "SELECT MAX(RANK() OVER (PARTITION BY loyalty ORDER BY order_total DESC)) FROM customer"
        return question, sql

    def lead_customer(self):
        question = "What is the difference in total amount spent between the top spender and the next customer?"
        sql = "SELECT MAX(order_total - LEAD(order_total) OVER (ORDER BY order_total DESC)) FROM customer WHERE order_total IS NOT NULL"
        return question, sql
    
    def lag_customer(self):
        question = "Determine the maximum difference in order total between each customer and the one whose last order was immediately before them."
        sql = "SELECT MAX(order_total - LAG(order_total) OVER (ORDER BY last_order)) FROM customer WHERE order_total IS NOT NULL"
        return question, sql

    def first_value_customer(self):
        question = "What is the highest initial amount spent by any customer within each loyalty level?"
        sql = "SELECT MAX(FIRST_VALUE(order_total) OVER (PARTITION BY loyalty ORDER BY last_order)) FROM customer"
        return question, sql

    def last_value_customer(self):
        question = "What is the lowest amount spent among the latest customers in each loyalty level?"
        sql = "SELECT MIN(LAST_VALUE(order_total) OVER (PARTITION BY loyalty ORDER BY last_order ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)) FROM customer"
        return question, sql

    def nth_value_customer(self):
        question = "What is the highest amount spent by the third most recent customer in any loyalty level?"
        sql = "SELECT MAX(NTH_VALUE(order_total, 3) OVER (PARTITION BY loyalty ORDER BY last_order)) FROM customer"
        return question, sql

    def percent_rank_customer(self):
        question = "What is the maximum percentile rank of customers based on total amount spent within each loyalty level?"
        sql = "SELECT MAX(PERCENT_RANK() OVER (PARTITION BY loyalty ORDER BY order_total DESC)) FROM customer"
        return question, sql

    def cume_dist_customer(self):
        question = "For the customer who spent the most within their loyalty level, what is their cumulative distribution?"
        sql = "SELECT MAX(CUME_DIST() OVER (PARTITION BY loyalty ORDER BY order_total DESC)) FROM customer"
        return question, sql

    def percentile_cont_customer(self):
        question = "Across all loyalty levels, what is the highest median amount spent by customers?"
        sql = "SELECT MAX(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_total) OVER (PARTITION BY loyalty)) FROM customer"
        return question, sql

    def percentile_disc_customer(self):
        question = "What is the maximum discrete median amount spent across all loyalty levels?"
        sql = "SELECT MAX(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY order_total) OVER (PARTITION BY loyalty)) FROM customer"
        return question, sql
    
    # Employee table templates
    def sum_over_employee(self):
        question = "What is the total cumulative salary paid to employees as of the most recent hire date?"
        sql = "SELECT MAX(SUM(salary) OVER (ORDER BY hire_date)) FROM employee"
        return question, sql

    def row_number_employee(self):
        question = "What is the position of the highest-paid employee?"
        sql = "SELECT MAX(ROW_NUMBER() OVER (ORDER BY salary DESC)) FROM employee"
        return question, sql

    def avg_over_employee(self):
        question = "What is the average salary of employees as of the most recent hire date?"
        sql = "SELECT MAX(AVG(salary) OVER (ORDER BY hire_date)) FROM employee"
        return question, sql

    def count_over_employee(self):
        question = "How many employees have been hired up to the most recent hire date?"
        sql = "SELECT MAX(COUNT(*) OVER (ORDER BY hire_date)) FROM employee"
        return question, sql

    def rank_employee(self):
        question = "Among all positions, what is the highest salary rank?"
        sql = "SELECT MAX(RANK() OVER (PARTITION BY position ORDER BY salary DESC)) FROM employee"
        return question, sql

    def lead_employee(self):
        question = "What is the salary difference between the top earner and the next highest-paid employee?"
        sql = "SELECT MAX(salary - LEAD(salary) OVER (ORDER BY salary DESC)) FROM employee WHERE salary IS NOT NULL"
        return question, sql
    
    def lag_employee(self):
        question = "Calculate the maximum salary difference between each employee and the one who was hired just before them."
        sql = "SELECT MAX(salary - LAG(salary) OVER (ORDER BY hire_date)) FROM employee WHERE salary IS NOT NULL"
        return question, sql

    def first_value_employee(self):
        question = "What is the highest starting salary among all positions?"
        sql = "SELECT MAX(FIRST_VALUE(salary) OVER (PARTITION BY position ORDER BY hire_date)) FROM employee"
        return question, sql

    def last_value_employee(self):
        question = "What is the lowest salary among the most recently hired employees in each position?"
        sql = "SELECT MIN(LAST_VALUE(salary) OVER (PARTITION BY position ORDER BY hire_date ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)) FROM employee"
        return question, sql

    def nth_value_employee(self):
        question = "What is the highest salary of the third most recently hired employee in any position?"
        sql = "SELECT MAX(NTH_VALUE(salary, 3) OVER (PARTITION BY position ORDER BY hire_date)) FROM employee"
        return question, sql

    def percent_rank_employee(self):
        question = "What is the maximum percentile rank of employees based on salary within each position?"
        sql = "SELECT MAX(PERCENT_RANK() OVER (PARTITION BY position ORDER BY salary DESC)) FROM employee"
        return question, sql

    def cume_dist_employee(self):
        question = "For the highest-paid employee in their position, what is their cumulative distribution?"
        sql = "SELECT MAX(CUME_DIST() OVER (PARTITION BY position ORDER BY salary DESC)) FROM employee"
        return question, sql

    def percentile_cont_employee(self):
        question = "Across all positions, what is the highest median salary?"
        sql = "SELECT MAX(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) OVER (PARTITION BY position)) FROM employee"
        return question, sql

    def percentile_disc_employee(self):
        question = "What is the maximum discrete median salary across all positions?"
        sql = "SELECT MAX(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY salary) OVER (PARTITION BY position)) FROM employee"
        return question, sql
    
    # Sales table templates
    def sum_over_sales(self):
        question = "What is the total cumulative sale amount up to the most recent sale date?"
        sql = "SELECT MAX(SUM(sale_amount) OVER (ORDER BY sale_date)) FROM sales"
        return question, sql

    def row_number_sales(self):
        question = "What is the position of the sale with the highest amount?"
        sql = "SELECT MAX(ROW_NUMBER() OVER (ORDER BY sale_amount DESC)) FROM sales"
        return question, sql

    def avg_over_sales(self):
        question = "What is the average sale amount up to the most recent sale date?"
        sql = "SELECT MAX(AVG(sale_amount) OVER (ORDER BY sale_date)) FROM sales"
        return question, sql

    def count_over_sales(self):
        question = "How many sales have been made up to the most recent sale date?"
        sql = "SELECT MAX(COUNT(*) OVER (ORDER BY sale_date)) FROM sales"
        return question, sql

    def rank_sales(self):
        question = "What is the highest rank of sales based on the sale amount?"
        sql = "SELECT MAX(RANK() OVER (ORDER BY sale_amount DESC)) FROM sales"
        return question, sql

    def lead_sales(self):
        question = "What is the difference in sale amount between the largest sale and the following sale?"
        sql = "SELECT MAX(sale_amount - LEAD(sale_amount) OVER (ORDER BY sale_amount DESC)) FROM sales WHERE sale_amount IS NOT NULL"
        return question, sql

    def lag_sales(self):
        question = "What is the sale amount difference between each sale and the sale that occurred just before it, sorted by sale date?"
        sql = "SELECT MAX(sale_amount - LAG(sale_amount) OVER (ORDER BY sale_date)) FROM sales WHERE sale_amount IS NOT NULL"
        return question, sql

    def first_value_sales(self):
        question = "What is the initial highest sale amount recorded?"
        sql = "SELECT MAX(FIRST_VALUE(sale_amount) OVER (ORDER BY sale_date)) FROM sales"
        return question, sql

    def last_value_sales(self):
        question = "What is the lowest sale amount among the most recent sales?"
        sql = "SELECT MIN(LAST_VALUE(sale_amount) OVER (ORDER BY sale_date ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)) FROM sales"
        return question, sql

    def nth_value_sales(self):
        question = "What is the sale amount of the third most recent sale?"
        sql = "SELECT MAX(NTH_VALUE(sale_amount, 3) OVER (ORDER BY sale_date)) FROM sales"
        return question, sql

    def percent_rank_sales(self):
        question = "What is the maximum percentile rank of sales based on the sale amount?"
        sql = "SELECT MAX(PERCENT_RANK() OVER (ORDER BY sale_amount DESC)) FROM sales"
        return question, sql

    def cume_dist_sales(self):
        question = "For the largest sale, what is its cumulative distribution?"
        sql = "SELECT MAX(CUME_DIST() OVER (ORDER BY sale_amount DESC)) FROM sales"
        return question, sql

    def percentile_cont_sales(self):
        question = "What is the highest median sale amount?"
        sql = "SELECT MAX(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sale_amount) OVER ()) FROM sales"
        return question, sql

    def percentile_disc_sales(self):
        question = "What is the maximum discrete median sale amount?"
        sql = "SELECT MAX(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY sale_amount) OVER ()) FROM sales"
        return question, sql