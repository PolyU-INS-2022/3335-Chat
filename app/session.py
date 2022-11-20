import os
import time

from connection import get_connection
from flask import make_response, redirect, request
from hashlib import *


def initial_session():
    conn = get_connection("mysql-session")
    cursor = conn.cursor()
    sessionid = generate_session()
    cursor.execute("USE ChatRoom")
    cursor.execute("INSERT INTO Session VALUES (%s, NULL, ADDDATE(NOW(), INTERVAL 30 MINUTE))", (sessionid,))
    conn.commit()
    return sessionid


def generate_session(user = ""):
    now = str(time.time()).encode()
    salt = os.urandom(16)
    result = salt + user.encode() + now
    return sha256(result).hexdigest()


def get_session_user_id():
    sessionid = request.cookies.get("sessionid")
    conn = get_connection("mysql-session")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT userID from Session WHERE SessionID=%s", (sessionid,))
    result = cursor.fetchall()
    if len(result) > 0:
        return result[0][0]
    else:
        return None


def get_session_user_name():
    userid = get_session_user_id()
    conn = get_connection("mysql-login")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT Name from user WHERE id=%s", (userid,))
    result = cursor.fetchall()
    if result == []:
        return None
    (result,) = result[0]
    return result


def check_login(sessionid):
    conn = get_connection("mysql-session")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT userID from Session WHERE SessionID=%s", (sessionid,))
    result = cursor.fetchall()
    return len(result) > 0, len(result) > 0 and result[0][0] != None


def extend_session(sessionid):
    conn = get_connection("mysql-session")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("UPDATE Session set ExpireTime=ADDDATE(NOW(), INTERVAL 30 MINUTE) WHERE SessionID=%s", (sessionid,))
    conn.commit()


def check_session(resp, login=True):
    sessionid = request.cookies.get("sessionid")
    if sessionid == None:
        if login:
            resp = make_response(redirect("/login"))
        resp.set_cookie("sessionid", initial_session())
        return resp, False
    session_exist, logined = check_login(sessionid)
    if not session_exist:
        resp.set_cookie("sessionid", initial_session())
        return resp, False
    if logined == False and login:
        return make_response(redirect("/login")), logined
    extend_session(sessionid)
    return resp, logined


def session_login(userid):
    sessionid = request.cookies.get("sessionid")
    conn = get_connection("mysql-session")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("UPDATE Session SET userID=%s WHERE sessionid=%s", (userid, sessionid))
    conn.commit()


def session_logout():
    sessionid = request.cookies.get("sessionid")
    conn = get_connection("mysql-session")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("UPDATE Session SET userID=NULL WHERE sessionid=%s", (sessionid,))
    conn.commit()


if __name__ == "__main__":
    conn = get_connection("mysql-session")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT * from Session")
    result = cursor.fetchall()
    print(result)