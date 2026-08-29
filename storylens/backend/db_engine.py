import os
import sqlite3
import pandas as pd

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

class DBEngine:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self._load_datasets()

    def _load_datasets(self):
        sales_path = os.path.join(DATA_DIR, "sales_orders.csv")
        shipments_path = os.path.join(DATA_DIR, "shipments.csv")
        support_path = os.path.join(DATA_DIR, "support_tickets.csv")

        if os.path.exists(sales_path):
            df_sales = pd.read_csv(sales_path)
            df_sales.to_sql("sales_orders", self.conn, if_exists="replace", index=False)

        if os.path.exists(shipments_path):
            df_shipments = pd.read_csv(shipments_path)
            df_shipments.to_sql("shipments", self.conn, if_exists="replace", index=False)

        if os.path.exists(support_path):
            df_support = pd.read_csv(support_path)
            df_support.to_sql("support_tickets", self.conn, if_exists="replace", index=False)

    def execute_query(self, sql: str):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        return columns, rows

    def query_to_dataframe(self, sql: str) -> pd.DataFrame:
        return pd.read_sql_query(sql, self.conn)

db_engine = DBEngine()
