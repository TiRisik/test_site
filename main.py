from flask import Flask, request, render_template
from mongodb_class import User, Manga
from mongoengine import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
connect('db', host='mongodb+srv://Tiris:Et21121982@anibus.rzt5y.mongodb.net/db?retryWrites=true&w=majority')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password, request.form['submit_button'])
        if request.form['submit_button'] == 'Sign_in':
            result = list(User.objects(log_user=email))
            if result:
                return render_template('main.html')
            else:
                return render_template('login.html')
        elif request.form['submit_button'] == 'Sign_up':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            new_user = User(log_user=email, pass_user=password, first_name=first_name, last_name=last_name).save()
            return render_template('main.html')


@app.route("/menegers")
def promation():
    return render_template('menegers.html')


@app.route("/senen")
def shop():
    return render_template('senen.html')


@app.route("/shojo")
def shojo():
    return render_template('shojo.html')


@app.route("/main")
def main():
    return render_template('main.html')


numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

@app.route("/korzina")
def korzina():
    return render_template('korzina.html', tovar=numbers)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
