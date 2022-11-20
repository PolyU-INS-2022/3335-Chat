from auth import register, logout, login
from chat import chat_to, get_chat_list, get_message
from flask import Flask, render_template, make_response, request, redirect
from session import check_session, check_login, get_session_user_name


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    resp = make_response(redirect("/chat"))
    resp, _ = check_session(resp)
    return resp


@app.route("/chat")
def chat():
    resp = make_response(render_template("index.html"))
    resp, logined = check_session(resp)
    if not logined:
        return resp
    targetuser = request.args.get("name")
    username = get_session_user_name()
    chat_list = get_chat_list(targetuser)
    if targetuser == None and len(chat_list) > 0:
        targetuser = chat_list[0]["name"]
    messages = get_message(targetuser)
    resp = make_response(render_template("index.html", chat_list=chat_list, messages=messages, username=username, targetuser=targetuser))
    return resp


@app.route("/chat/message", methods=["POST"])
def chat_message():
    if not check_login(request.cookies.get("sessionid")):
        return make_response(redirect("/login"))
    chat_to(request.form)
    return make_response(redirect("/chat"))


@app.route("/login", methods=["GET", "POST"])
def request_login():
    resp = make_response(render_template("login.html"))
    resp, logined = check_session(resp, False)
    if logined:
        resp = make_response(redirect("/chat"))
    elif request.method == "POST" and login(request.form):
        resp = make_response(redirect("/chat"))
    return resp


@app.route("/logout")
def request_logout():
    resp = make_response(redirect("/login"))
    logout()
    return resp


@app.route("/signup", methods=["GET", "POST"])
def request_signup():
    resp = make_response(render_template("signup.html"))
    resp, logined = check_session(resp, False)
    if request.method == "POST":
        resp, error = register(resp, request.form)
    elif logined:
        resp = make_response(redirect("/chat"))
    return resp

if __name__ == "__main__":
    app.run(debug=True,port=5555)