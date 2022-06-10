from distutils.log import error
from pathlib import Path
from typing import Dict
import psycopg2
import psycopg2.extras
from psycopg2.sql import SQL, Identifier, Literal, Composable
import os

class DB:
    def __init__(self, conn_string=os.environ.get("DATABASE_URL"), create_script=os.path.dirname(__file__) + '/db/init.sql'):
        self.conn = psycopg2.connect(
            conn_string
        )
        self.table_script = create_script
        self.connect()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            results = self.cursor.fetchall()
            return results
        except psycopg2.Error as e:
            return e

    def connect(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.cursor = cursor

    def create_table(self):
        try:
            sql = ""
            with open(self.table_script, 'r') as f:
                sql = f.read()
            self.cursor.execute(sql)
            self.conn.commit()
        except psycopg2.Error as e:
            error(e)

    def insert_record(self, table, columns, values):
        try:
            columns = ", ".join(columns)

            values_string = []
            for value in values:
                if "(" in value:
                    values_string.append(value)
                else:
                    values_string.append(f"'{value}'")
            values = ", ".join(values_string)

            sql = SQL(f"INSERT INTO {{}} ({columns}) VALUES ({values})").format(Identifier(table))
            print(self.cursor.mogrify(sql))
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error in insert record {e}")

    def update_record(self, table, values: Dict, id):
        try:
            key_value = []
            for item in values.items():
                key_value.append(f"{item[0]}='{item[1]}'")

            values = ", ".join(key_value)

            sql = SQL("UPDATE {} SET {} WHERE id = %s").format(
                Identifier(table),
                Literal(values)
            )
            print(self.cursor.mogrify(sql))
            self.cursor.execute(sql, [id])
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            return e

    def delete_record(self, table, id):
        try:
            sql = SQL("DELETE FROM {} WHERE id = %s").format(
                Identifier(table),
            )
            self.cursor.execute(sql, [id])
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            return e

    def get_record(self, table, values="*", where=None):
        try:
            is_all = (values == "*" and len(values) <= 1)
            where = f" WHERE id = {where}" if where != None else ""

            if is_all:
                sql = SQL(f"SELECT * FROM {{}}{where}").format(Identifier(table))
            else:
                values = ", ".join(values)
                sql = SQL(f"SELECT {{}} FROM {{}}{where}").format(Identifier(values), Identifier(table))

            self.cursor.execute(sql)

            if is_all:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchone()
        except psycopg2.Error as e:
            return e