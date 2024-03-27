# **********************************************************
# * CATEGORY  SOFTWARE
# * GROUP     FINANCE
# * AUTHOR    LANCE HAYNIE <LHAYNIE@SCCITY.ORG>
# **********************************************************
# Pelorus Past Due Balance API
# Copyright Santa Clara City
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pyodbc, json
from flask_restful import Resource, request
from datetime import datetime, timedelta
from decimal import Decimal
from .settings import *


class PelorusConnector:
    def __init__(
        self,
        host,
        instance,
        database,
        username,
        password,
        ssl_enabled=True,
        trust_server_certificate=True,
    ):
        self.host = host
        self.instance = instance
        self.database = database
        self.username = username
        self.password = password
        self.ssl_enabled = ssl_enabled
        self.trust_server_certificate = trust_server_certificate
        self.conn = None
        self.cursor = None

    def connect(self):
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.host}\{self.instance};DATABASE={self.database};UID={self.username};PWD={self.password};Encrypt=yes;TrustServerCertificate=yes"
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None


class AccountBalance:
    def __init__(self, connector):
        self.connector = connector

    def calculate_look_back(self):
        current_date = datetime.now()
        balance_month = (
            current_date.month - 2
            if current_date.month >= 3
            else current_date.month + 10
        )
        balance_year = (
            current_date.year if current_date.month >= 3 else current_date.year - 1
        )
        look_back_date = datetime(balance_year, balance_month, 25)
        return look_back_date

    def execute_stored_proc(self, balance_date):
        self.connector.connect()
        cursor = self.connector.cursor
        cursor.execute(
            "EXEC [999].[GetAccountBalances] @BalanceDate = ?", (balance_date,)
        )
        rows = cursor.fetchall()

        rows = [
            [float(value) if isinstance(value, Decimal) else value for value in row]
            for row in rows
        ]

        result = [
            dict(zip([column[0] for column in cursor.description], row)) for row in rows
        ]
        self.connector.disconnect()
        return result

    def get_balances(self):
        self.connector.connect()
        look_back_date = self.calculate_look_back()
        result = self.execute_stored_proc(look_back_date)
        self.connector.disconnect()

        total_accounts = len(result)

        summary = {
            "balance_date": look_back_date.strftime("%Y-%m-%d"),
            "total_accounts": total_accounts,
        }

        data = result

        response = {"summary": summary, "data": data}

        return response


class Accounts(Resource):
    def get(self):
        pelorus = PelorusConnector(
            host=db_host,
            instance=db_instance,
            database=db_database,
            username=db_user,
            password=db_password,
        )
        result = AccountBalance(pelorus).get_balances()
        return result
