from flask import Flask, render_template, request, make_response, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = "qazxdr4321"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


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

        found_user = users.query.filter_by(name=user_name).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user_name, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Succesful!")
        return redirect(url_for("user_page"))
    else:
        if "user" in session:
            return redirect(url_for("user_page"))
        return render_template('login.html')


@app.route('/user', methods=["POST", "GET"])
def user_page():
    email = None
    if "user" in session:
        user_name = session['user']

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user_name).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template('user.html', user_name=user_name, email=email)
    else:
        return redirect(url_for("login_page"))


@app.route("/logout")
def logout_page():
    if "user" in session:
        user_name = session['user']
        flash(f"You have been logged out {user_name}", "info")

    session.pop("user", None)
    session.pop("email", None)
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
    return f'Server fall down for {random.randint(3, 256)} time'





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)














