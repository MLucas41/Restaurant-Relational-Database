import mysql.connector
import os

from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def insert_customer(fname, lname, usual_menuitem, times_visited, last_visit, notes):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO customers
            (customer_fname, customer_lname, customer_usual_menuitem,
             customer_timesvisited, customer_lastvisit_date, customer_notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (fname, lname, usual_menuitem, times_visited, last_visit, notes))
    conn.commit()
    cursor.close()
    conn.close()
