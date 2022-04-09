from datetime import timedelta

from flask import Flask, render_template, request, make_response, redirect, url_for, session
import random


app = Flask(__name__)
app.secret_key = "qazxdr4321"
app.permanent_session_lifetime = timedelta(minutes=2)


@app.route('/')
def home_page():
    if "user" in session:
        return render_template('home.html')
    else:
        return redirect(url_for("login_page"))




@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        session.permanent = True
        user_name = request.form["user_name"]
        session["user"] = user_name
        return redirect(url_for("user_page"))
    else:
        if "user" in session:
            return redirect(url_for("user_page"))
        return render_template('login.html')


@app.route('/user')
def user_page():
    if "user" in session:
        user_name = session['user']
        return render_template('user.html', data=user_name)
    else:
        return redirect(url_for("login_page"))


@app.route("/logout")
def logout_page():
    session.pop("user", None)
    return redirect(url_for("login_page"))



@app.route('/cookie')
def cookie_page():
    response = make_response('<h1>Ten dokument zawiera plik cookie!</h1>')
    response.set_cookie('odpowiedz', '42')
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return f'Server fall down for {random.randint(3,256)} time'

if __name__ == '__main__':
    app.run(debug=True)
