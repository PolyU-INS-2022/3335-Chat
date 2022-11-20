import os
import random

from connection import get_connection
from flask import make_response, redirect, request
from hashlib import *
from session import session_logout, session_login


def salt_hash(password, salt, count):
    hashed = salt + password
    salt = b"SHA256:" + str(count).encode() + salt
    for i in range(count):
        hashed = sha256(hashed).hexdigest().encode()
    hashed = salt.decode() + hashed.decode()
    return hashed


def password_to_hash(password: str):
    password = password.encode()
    count = random.randint(500, 900)
    salt = ""
    for i in range(20):
        salt += chr(random.randint(33, 126))
    salt = sha256(salt.encode()).hexdigest()[:26].encode()
    return salt_hash(password, salt, count)


def verify_password_hash(password, hashed):
    count = int(hashed[7:10])
    salt = hashed[10:36].encode()
    return salt_hash(password.encode(), salt, count) == hashed


def get_user_id(username):
    conn = get_connection("mysql-auth")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT ID from user WHERE name=%s", (username,))
    result = cursor.fetchall()
    if result == []:
        return None
    (result,) = result[0]
    return result


def get_user_name(userid):
    conn = get_connection("mysql-auth")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT Name from user WHERE id=%s", (userid,))
    result = cursor.fetchall()
    if result == []:
        return None
    (result,) = result[0]
    return result


def login(data):
    conn = get_connection("mysql-login")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    username = data["name"]
    cursor.execute("SELECT ID, password from user WHERE name=%s", (username,))
    result = cursor.fetchall()
    if len(result) > 0:
        (userid, hashed) = result[0]
        if verify_password_hash(data["password"], hashed):
            session_login(userid)
            return True
    return False


def logout():
    session_logout()


def register(resp, data):
    if data["password"] != data["password2"]:
        print("failed")
        return resp, ["<p>Password Not Same</p>"]
    if len(data["name"]) <= 0:
        print("failed")
        return resp, ["<p>User Name Too short</p>"]
    conn = get_connection("mysql-auth")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT name FROM user WHERE name=%s", (data["name"],))
    result = cursor.fetchall()
    if len(result) > 0:
        return resp, ["<p>User Name existed</p>"]
    hashed = password_to_hash(data["password"])
    cursor.execute("INSERT INTO user (Name, password, email) VALUES (%s, %s, %s)", (data["name"], hashed, data["email"]))
    cursor.execute("SELECT ID FROM user WHERE name=%s", (data["name"],))
    userid = cursor.fetchall()[0][0]
    conn.commit()
    session_login(userid)
    resp = make_response(redirect("/chat"))
    return resp, []


if __name__ == "__main__":
    password = "test"
    hashed = password_to_hash(password)
    print(password)
    print(hashed)
    print(verify_password_hash(password, hashed))

