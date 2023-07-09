import mysql.connector

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_DB = "django_vue_admin"
TABLE_NAME="sensory_data_app_thsensordata"


def add_th_data(humidity_value,temperature_value,sensor_location,date_recorded):
    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

    # Create a cursor object to interact with the database
    cursor = cnx.cursor()

    # Define the SQL statement to insert a record
    sql = "INSERT INTO "+TABLE_NAME+" (humidity_value,temperature_value,sensor_location,date_recorded) VALUES (%s, %s,%s,%s)"

    # Define the values for the new record
    values = (humidity_value,temperature_value,sensor_location,date_recorded)

    try:
        # Execute the SQL statement with the provided values
        cursor.execute(sql, values)

        # Commit the transaction to make the changes permanent
        cnx.commit()

        print("Record inserted successfully!")

    except mysql.connector.Error as error:
        print(f"Error inserting record: {error}")

    finally:
        # Close the cursor and the database connection
        cursor.close()
        cnx.close()
