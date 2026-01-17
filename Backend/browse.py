# browse.py
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Lunarcy@1214", 
    "database": "relaxdash"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_restaurants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, address FROM restaurants")
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_menu(restaurant_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # UPDATED QUERY: Select id AND restaurant_id so we can track them
    query = """
        SELECT id, restaurant_id, name, description, price, dietary_type 
        FROM menu_items 
        WHERE restaurant_id = %s
    """
    cursor.execute(query, (restaurant_id,))
    data = cursor.fetchall()
    conn.close()
    return data