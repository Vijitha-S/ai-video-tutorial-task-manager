import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def ensure_reminder_log_table():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Create table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS REMINDER_LOG (
                reminder_id INT PRIMARY KEY AUTO_INCREMENT,
                task_item_id VARCHAR(100) NOT NULL,
                lesson_id VARCHAR(100) NOT NULL,
                reminder_type VARCHAR(30) NOT NULL,
                reminder_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Get existing columns
        cursor.execute("SHOW COLUMNS FROM REMINDER_LOG")
        columns = [row[0] for row in cursor.fetchall()]

        # Add missing columns
        if "reminder_id" not in columns:
            cursor.execute("""
                ALTER TABLE REMINDER_LOG
                ADD COLUMN reminder_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST
            """)

        if "task_item_id" not in columns:
            cursor.execute("""
                ALTER TABLE REMINDER_LOG
                ADD COLUMN task_item_id VARCHAR(100) NOT NULL
            """)

        if "lesson_id" not in columns:
            cursor.execute("""
                ALTER TABLE REMINDER_LOG
                ADD COLUMN lesson_id VARCHAR(100) NOT NULL
            """)

        if "reminder_type" not in columns:
            cursor.execute("""
                ALTER TABLE REMINDER_LOG
                ADD COLUMN reminder_type VARCHAR(30) NOT NULL
            """)

        if "reminder_date" not in columns:
            cursor.execute("""
                ALTER TABLE REMINDER_LOG
                ADD COLUMN reminder_date DATETIME DEFAULT CURRENT_TIMESTAMP
            """)

        connection.commit()

        print("REMINDER_LOG table checked successfully.")

    except Exception as error:
        if connection:
            connection.rollback()

        print("REMINDER_LOG setup failed:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    try:
        connection = get_connection()

        if connection.is_connected():
            print("======================================")
            print("MySQL CONNECTION SUCCESSFUL")
            print("======================================")
            print("Database:", os.getenv("DB_NAME"))

        connection.close()

    except mysql.connector.Error as error:
        print("MySQL connection failed!")
        print("Error:", error)

if __name__ == "__main__":
    try:
        connection = get_connection()

        if connection.is_connected():
            print("======================================")
            print("MySQL CONNECTION SUCCESSFUL")
            print("======================================")
            print("Database:", os.getenv("DB_NAME"))

        connection.close()

    except mysql.connector.Error as error:
        print("MySQL connection failed!")
        print("Error:", error)