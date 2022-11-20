from auth import get_user_id, get_user_name
from connection import get_connection
from flask import make_response, redirect, request
from session import get_session_user_id


def get_chat_list(username):
    users = []
    if username != None and get_user_id(username) != None:
        users.append(get_user_id(username))
    current_user_id = get_session_user_id()
    conn = get_connection("mysql-chatroom")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT DISTINCT sender, receiver, CreateTime from ChatRecord WHERE sender=%s OR receiver=%s ORDER by CreateTime ASC", (current_user_id, current_user_id))
    results = cursor.fetchall()
    for result in results:
        if result[0] not in users and result[0] != current_user_id:
            users.append(result[0])
        if result[1] not in users and result[1] != current_user_id:
            users.append(result[1])
    data = []
    for i in users:
        data.append({"name": get_user_name(i)})
    return data


def get_message(targetuser):
    current_user_id = get_session_user_id()
    targetuser_id = get_user_id(targetuser)
    conn = get_connection("mysql-chatroom")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("SELECT message, DATE_FORMAT(CreateTime, '%T'), sender from ChatRecord WHERE sender=%s and receiver=%s OR sender=%s and receiver=%s ORDER by CreateTime ASC", (current_user_id, targetuser_id, targetuser_id, current_user_id))
    results = cursor.fetchall()
    data = []
    for result in results:
        data.append({"message": result[0], "time": result[1], "send": result[2] == current_user_id})
    return data



def chat_to(data):
    print(data)
    username = data["receiver"]
    message = data["message"]
    userid = get_user_id(username)
    current_userid = get_session_user_id()
    if userid == None:
        return False
    conn = get_connection("mysql-chatroom")
    cursor = conn.cursor()
    cursor.execute("USE ChatRoom")
    cursor.execute("INSERT INTO ChatRecord (message, receiver, sender, CreateTime) VALUES (%s, %s, %s, NOW())", (message, userid, current_userid))
    conn.commit()
    #print(message, userid, current_userid)
    return True