import json_files
import mysql.connector

connection = mysql.connector.MySQLConnection(host=json_files.get_field('projects.tnlrp.dbcredentials.host'),
                                             database=json_files.get_field('projects.tnlrp.dbcredentials.database'),
                                             user=json_files.get_field('projects.tnlrp.dbcredentials.user'),
                                             password=json_files.get_field('projects.tnlrp.dbcredentials.password'))
cursor = connection.cursor()


def open_connection():
    try:
        connection.connect()
        if connection.is_connected():
            return True
    except mysql.connector.Error as e:
        return False


def connect_cursor():
    if connection.is_connected():
        cursor = connection.cursor()
        return cursor

# Function that inserts data into said table


def insert_data(insert_query, data):
    try:
        # Executing the SQL command
        cursor.execute(insert_query, data)

        # Commit your changes in the database
        connection.commit()

    except:
        # Roll back in case of error
        connection.rollback()


def close_connection():
    if connection.is_connected():
        connection.close()
