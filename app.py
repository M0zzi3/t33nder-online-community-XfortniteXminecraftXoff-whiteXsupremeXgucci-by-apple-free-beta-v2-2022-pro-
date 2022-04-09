from flask import Flask, render_template, request, make_response
import random


app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')



@app.route('/cookie')
def cookie_page():
    response = make_response('<h1>Ten dokument zawiera plik cookie!</h1>')
    response.set_cookie('odpowiedz', '42')
    return response


@app.route('/user/<user_name>')
def user_page(user_name):
    return render_template('user.html', data=user_name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return f'Server fall down for {random.randint(3,256)} time'

if __name__ == '__main__':
    app.run(debug=True)
