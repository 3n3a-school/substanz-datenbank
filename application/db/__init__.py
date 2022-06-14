from distutils.log import error
from pathlib import Path
from typing import Dict
import psycopg2
import psycopg2.extras
from psycopg2.sql import SQL, Identifier, Literal, Composable
import os

class DB:
    def __init__(self, conn_string=os.environ.get("DATABASE_URL"), create_script=os.path.dirname(__file__) + '/init.sql'):
        self.conn = psycopg2.connect(
            conn_string
        )
        self.table_script = create_script
        self.connect()

    def execute(self, sql, values=None, return_string=False):
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            if return_string:
                return self.cursor.fetchall()
            return True
        except Exception as e:
            self.conn.rollback()
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
        except Exception as e:
            self.conn.rollback()
            error(f"Error while creating tables {e}")

    def insert_record(self, table, columns, values, return_string=""):
        try:
            columns = ", ".join(columns)

            values_string = []
            for value in values:
                if "(" in str(value):
                    values_string.append(value)
                else:
                    values_string.append(f"'{value}'")
            values = ", ".join(values_string)

            sql = SQL(f"INSERT INTO {{}} ({columns}) VALUES ({values}){return_string}").format(Identifier(table))
            print(self.cursor.mogrify(sql))
            self.cursor.execute(sql)
            self.conn.commit()
            if return_string != "":
                return self.cursor.fetchone()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error in insert record {e}")
            return e

    def update_record(self, table, values: Dict, id, return_string=""):
        try:
            key_value = []
            for item in values.items():
                key_value.append(f"{item[0]}='{item[1]}'")

            values = ", ".join(key_value)

            sql = SQL(f"UPDATE {{}} SET {values} WHERE id = %s{return_string}").format(
                Identifier(table)
            )
            print(self.cursor.mogrify(sql))
            self.cursor.execute(sql, [id])
            self.conn.commit()
            if return_string != "":
                return self.cursor.fetchone()
            return True
        except Exception as e:
            self.conn.rollback()
            return e

    def delete_record(self, table, id):
        try:
            sql = SQL("DELETE FROM {} WHERE id = %s").format(
                Identifier(table),
            )
            self.cursor.execute(sql, [id])
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return e

    def get_record(self, table, values="*", where=None):
        try:
            is_all = (values == "*" and len(values) <= 1)
            where_string = f" WHERE {where['key']} {where['operator']} {where['value']}" if where != None else ""

            if is_all:
                sql = SQL(f"SELECT * FROM {{}}{where_string}").format(Identifier(table))
            else:
                values = ", ".join(values)
                sql = SQL(f"SELECT {{}} FROM {{}}{where}").format(Identifier(values), Identifier(table))

            self.cursor.execute(sql)
            self.conn.commit()
            if is_all:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchone()
        except Exception as e:
            self.conn.rollback()
            return e