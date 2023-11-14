import mysql.connector
import datetime
import csv

class Database:
    def __init__(self, formatted_date):
        self.config = None
        self.current_table = f"table_{formatted_date}"
        self.employee_table = "table_employees"

    def configure_database(self, host='10.152.5.142', port=3306, database='facerecdatabase', user='interns',
                           password='InternsPassword!'):
        """
        Function that configures the database being used
        :param host: IP address or hostname of the database server
        :param port: Port number on which the database server is listening
        :param database: Name of the database to connect to
        :param user: Username for authentication
        :param password: Password for the specified username
        """
        # Configure the database
        config = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }

        self.config = config

    def create_employee_table(self, formatted_date=None):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        if not formatted_date:
            self.employee_table = f"table_{formatted_date}"

        # Create table
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {self.employee_table} (
                name TEXT,
                employee_id TEXT
            )
        '''

        cursor.execute(create_table_query)
        conn.close()

    def insert_into_employee_table(self, name, employee_id):
        """
        Inserts into the employee table the name and ID of
        :param name: the name of the employee
        :param employee_id: the id of the employee
        :return:
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        # Insert data into table
        insert_query = '''
            INSERT INTO {table_name} (name, employee_id)
            VALUES (%s, %s)
        '''
        table_name = self.employee_table
        # The values being entered. exit_time is none because the employee has not left yet
        values = (name, employee_id)

        cursor.execute(insert_query.format(table_name=table_name), values)
        conn.commit()

        conn.close()

    def create_table(self, date):
        """
        Creates a new table to insert data in to
        :param date: the date the table is being created in string format
                Dates are written in the format 05242023 which means May 24th, 2023
        :return: True if the table could be created, False if not
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        # Create table
        table_name = f"table_{date}"  # Using string formatting
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                name TEXT,
                employee_id TEXT,
                entry_time TEXT,
                exit_time TEXT
            )
        '''

        cursor.execute(create_table_query)
        conn.close()

        # Set the current table
        self.current_table = table_name

    def insert_into_table(self, name, employee_id, entry_time=None):
        """
        Inserts the employee information into the table. Used when registering an employee
        :param name: The name of the employee
        :param employee_id: The id of the employee
        :param entry_time: the entry time of the employee
        :return: True if the table could be created, False if not
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        # Insert data into table
        insert_query = '''
            INSERT INTO {table_name} (name, employee_id, entry_time, exit_time)
            VALUES (%s, %s, %s, %s)
        '''
        table_name = self.current_table
        # The values being entered. exit_time is none because the employee has not left yet
        values = (name, employee_id, entry_time, None)

        cursor.execute(insert_query.format(table_name=table_name), values)
        conn.commit()

        conn.close()

    def update_times(self, name, new_entry_time, new_exit_time):
        """
        Updates the entry and exit time of the employee correspondingly
        :param name: the name of the employee whose times need to be updated
        :param new_entry_time: the time the employee entered
        :param new_exit_time: the time the employee left
        :return: True if the table could be created, False if not
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        # Update entry and exit time
        update_query = '''
            UPDATE {table_name}
            SET entry_time = %s, exit_time = %s
            WHERE name = %s
        '''
        table_name = self.current_table
        values = (new_entry_time, new_exit_time, name)

        cursor.execute(update_query.format(table_name=table_name), values)
        conn.commit()

        conn.close()

    def select_from_table(self, name, current=None):
        """
        selects rows or values from the table
        :param name: The name of the person that the data is wanted for.
                    If name is '*' that means data is wanted for everyone in the table
        :return: a list of the data needed. List is empty if name does
        not exist
        """
        if current is None:
            table_name = self.current_table
        else:
            table_name = current
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()

            if name != '*':
                # Select data by name
                select_query = '''
                    SELECT *
                    FROM {table_name}
                    WHERE name = %s
                '''
                values = (name,)

                cursor.execute(select_query.format(table_name=table_name), values)
                result = cursor.fetchall()
            elif name == '*':
                # Select data for everyone
                select_query = '''
                    SELECT *
                    FROM {table_name}
                '''

                cursor.execute(select_query.format(table_name=table_name))
                result = cursor.fetchall()

            conn.close()
            return result
        except Exception:
            return []

    def clean_database(self):
        """
        Cleans the database and deletes all the tables and data
        :return: void
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        # Get all table names in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Delete each table
        for table in tables:
            table_name = table[0]
            drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
            cursor.execute(drop_table_query)

        conn.commit()
        conn.close()

    def export_to_csv(self):
        """
        Exports all tables and their data to a new Excel CSV file with a dynamic filename
        """
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()

            # Get the current date and time
            current_datetime = datetime.datetime.now()
            formatted_date = current_datetime.strftime("%Y%m%d_%H%M%S")

            # Construct the dynamic filename
            csv_filename = f"database_export_{formatted_date}.csv"

            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)

                # Get all table names in the database
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()

                # Export each table's data to the CSV file
                for table in tables:
                    table_name = table[0]
                    csvwriter.writerow([f"Table: {table_name}"])

                    # Fetch data from the table
                    data = self.select_from_table('*', table_name)
                    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    column_headers = [column[0] for column in cursor.fetchall()]
                    csvwriter.writerow(column_headers)

                    if data:
                        # Write the data in the file
                        csvwriter.writerows(data)

            conn.close()
            print(f"Data exported to {csv_filename} successfully.")
        except Exception as e:
            print(f"Error exporting data to CSV: {e}")

