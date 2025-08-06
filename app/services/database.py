import mysql.connector
from flask import current_app
from config import Config

class Database:
    def __init__(self):
        self.config = Config()
        
    def get_connection(self):
        return mysql.connector.connect(
            host=self.config.MYSQL_HOST,
            user=self.config.MYSQL_USER,
            password=self.config.MYSQL_PASSWORD,
            database=self.config.MYSQL_DB
        )
    
    def execute_query(self, query, params=None, fetch_all=True):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall() if fetch_all else cursor.fetchone()
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            cursor.close()
            conn.close()