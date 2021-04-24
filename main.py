from flask import Flask, request, render_template
from mongodb_class import User, Manga
from mongoengine import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
connect('db', host='mongodb+srv://Tiris:Et21121982@anibus.rzt5y.mongodb.net/db?retryWrites=true&w=majority')
result_user = None



@app.route('/login', methods=['GET', 'POST'])
def login():
    global result_user
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password, request.form['submit_button'])
        if request.form['submit_button'] == 'Sign_in':
            result_user = list(User.objects(log_user=email))
            if result_user:
                if result_user[0].manager:
                    return ''' <li><a href="http://127.0.0.1:8080/secret">Добавить товар</a></li></br>
                    <li><a href="http://127.0.0.1:8080/secret_two">Удалить товар</a></li>'''
                else:
                    return render_template('main.html')
            else:
                return render_template('login.html')
        elif request.form['submit_button'] == 'Sign_up':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            new_user = User(log_user=email, pass_user=password, first_name=first_name,\
                            last_name=last_name, manager=False).save()
            return render_template('main.html')


@app.route("/menegers")
def promation():
    return render_template('menegers.html')


@app.route("/senen", methods=['GET', 'POST'])
def senen():
    global result_user
    spisok = []
    if request.method == 'GET':
        results = list(Manga.objects(category='senen'))
        i = 1
        if results:
            for result in results:
                photo = result.photo.read()
                f = open(f'static/img/senen/{i}.jpg', 'wb')
                f.write(photo)
                f.close()
                about = result.about[:175] + '...'
                name = result.name
                price = result.price
                spisok.append([f'static/img/senen/{i}.jpg', about, price, name])
                i += 1
            return render_template('shop.html', spisok=spisok)
        else:
            return '<h1>В данной категории ещё нет товаров</h1>'
    elif request.method == 'POST':
        print(request.form['button'])
        for i in spisok:
            if request.form['button'] == i[3]:
                result_user[0].tovar.append([i[3], i[2]])
                print(result_user[0].tovar)


@app.route("/main")
def main():
    return render_template('main.html')


@app.route("/shop/shojo", methods=['GET', 'POST'])
def shojo():
    global result_user
    spisok = []
    if request.method == 'GET':
        results = list(Manga.objects(category='shojo'))
        i = 1
        if results:
            for result in results:
                photo = result.photo.read()
                f = open(f'static/img/shojo/{i}.jpg', 'wb')
                f.write(photo)
                f.close()
                about = result.about[:175] + '...'
                name = result.name
                price = result.price
                spisok.append([f'static/img/shojo/{i}.jpg', about, price, name])
                i += 1
            return render_template('shop.html', spisok=spisok)
        else:
            return '<h1>В данной категории ещё нет товаров</h1>'
    elif request.method == 'POST':
        print(request.form['button'])
        for i in spisok:
            if request.form['button'] == i[3]:
                result_user[0].tovar.append([i[3], i[2]])
                print(result_user[0].tovar)


numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


@app.route("/korzina")
def korzina():
    return render_template('korzina.html', tovar=numbers)


@app.route("/secret", methods=['GET', 'POST'])
def secret():
    if request.method == 'GET':
        return render_template('secret.html')
    elif request.method == 'POST':
        f = request.files['file']
        sfname = 'static/img/a.jpg'
        f.save(sfname)
        new_manga = Manga(name=request.form['name'], price=request.form['price'], category=request.form['category'],\
                          about=request.form['about'], photo='static/img/a.jpg').save()
        return "Товар добавлен"


@app.route("/secret_two", methods=['GET', 'POST'])
def secret_two():
    if request.method == 'GET':
        return render_template('secret_two.html')
    elif request.method == 'POST':
        results = list(Manga.objects(name=request.form['name']))
        results[0].delete()
        return "Товар удалён"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
