from flask import Flask, request, render_template
from mongodb_class import User, Manga
from mongoengine import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
connect('db', host='mongodb+srv://Tiris:Et21121982@anibus.rzt5y.mongodb.net/db?retryWrites=true&w=majority')
result_user = None


# Аккаунт менеджера: who@mail.ru, 1234567
# Аккаунт пользователя: val@mail.ru, qwerty
# Ну или можете самии создать. Тогда в корзину всё добавлять придётся


@app.route('/login', methods=['GET', 'POST'])
def login():
    global result_user
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if request.form['submit_button'] == 'Sign_in':
            result_user = list(User.objects(log_user=email))
            if result_user:
                print(password, result_user[0].pass_user)
                if password == result_user[0].pass_user:
                    if result_user[0].manager:
                        return ''' <li><a href="http://127.0.0.1:8080/secret">Добавить товар</a></li></br>
                        <li><a href="http://127.0.0.1:8080/secret_two">Удалить товар</a></li>'''
                    else:
                        return render_template('main.html')
                else:
                    return render_template('login.html')
            else:
                return render_template('login.html')
        elif request.form['submit_button'] == 'Sign_up':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            new_user = User(log_user=email, pass_user=password, first_name=first_name, \
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
                spisok.append([f'static/img/senen/{i}.jpg', about, price, name, f'http://127.0.0.1:8080/senen/{i}'])
                i += 1
            return render_template('shop.html', spisok=spisok)
        else:
            return '<h1>В данной категории ещё нет товаров</h1>'
    elif request.method == 'POST':
        return f'''<a href={request.form['button']}>Подтвердите переход к товару</a>'''


@app.route("/senen/<int:i>", methods=['GET', 'POST'])
def senen_manga(i):
    global result_user
    results = list(Manga.objects(category='senen'))
    about = results[i - 1].about
    name = results[i - 1].name
    price = results[i - 1].price
    spisok = [f'static/img/senen/{i}.jpg', about, price, name]
    if request.method == 'GET':
        return render_template('manga.html', spisok=spisok)
    elif request.method == 'POST':
        result_user[0].korzina.append([spisok[3], str(spisok[2]), request.form['integer']])
        result_user[0].save()
        return 'Товар добавлен в корзину'


@app.route("/main")
def main():
    return render_template('main.html')


@app.route("/shojo", methods=['GET', 'POST'])
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
        return f'''<a href={request.form['button']}>Подтвердите переход к товару</a>'''


@app.route("/korzina")
def korzina():
    global result_user
    return render_template('korzina.html', tovar=result_user[0].korzina)


@app.route("/secret", methods=['GET', 'POST'])
def secret():
    if request.method == 'GET':
        return render_template('secret.html')
    elif request.method == 'POST':
        f = request.files['file']
        sfname = 'static/img/a.jpg'
        f.save(sfname)
        new_manga = Manga(name=request.form['name'], price=request.form['price'], category=request.form['category'], \
                          about=request.form['about'], photo='static/img/a.jpg').save()
        return "Товар добавлен"


@app.route("/popular", methods=['GET', 'POST'])
def popular():
    global result_user
    spisok = []
    if request.method == 'GET':
        results = list(Manga.objects(category='popular'))
        i = 1
        if results:
            for result in results:
                photo = result.photo.read()
                f = open(f'static/img/popular/{i}.jpg', 'wb')
                f.write(photo)
                f.close()
                about = result.about[:175] + '...'
                name = result.name
                price = result.price
                spisok.append([f'static/img/popular/{i}.jpg', about, price, name])
                i += 1
            return render_template('shop.html', spisok=spisok)
        else:
            return '<h1>В данной категории ещё нет товаров</h1>'
    elif request.method == 'POST':
        return f'''<a href={request.form['button']}>Подтвердите переход к товару</a>'''


@app.route("/secret_two", methods=['GET', 'POST'])
def secret_two():
    if request.method == 'GET':
        return render_template('secret_two.html')
    elif request.method == 'POST':
        results = list(Manga.objects(name=request.form['name']))
        results[0].delete()
        return "Товар удалён"


@app.route("/horror", methods=['GET', 'POST'])
def horror():
    global result_user
    spisok = []
    if request.method == 'GET':
        results = list(Manga.objects(category='horror'))
        i = 1
        if results:
            for result in results:
                photo = result.photo.read()
                f = open(f'static/img/horror/{i}.jpg', 'wb')
                f.write(photo)
                f.close()
                about = result.about[:175] + '...'
                name = result.name
                price = result.price
                spisok.append([f'static/img/horror/{i}.jpg', about, price, name])
                i += 1
            return render_template('shop.html', spisok=spisok)
        else:
            return '<h1>В данной категории ещё нет товаров</h1>'
    elif request.method == 'POST':
        return f'''<a href={request.form['button']}>Подтвердите переход к товару</a>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
