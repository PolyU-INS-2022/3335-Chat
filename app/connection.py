import json
import mysql.connector


def get_connection(account):
    with open("mysql.json", "r") as f:
        data = json.load(f)
    ac = data[account]
    conn = mysql.connector.connect(
        host = "mysql",
        port = 3306,
        user = ac["username"],
        passwd = ac["password"]
    )
    return conn