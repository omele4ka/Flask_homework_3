# Задание №4
# Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
# содержать следующие поля:
# ○ Имя пользователя (обязательное поле)
# ○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
# ○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
# ○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
# После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
# и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
# заполнено или данные не прошли валидацию, то должно выводиться соответствующее
# сообщение об ошибке.
# Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
# базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
# об ошибке

from flask import Flask, render_template, url_for, request, redirect
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

from form_04 import RegistrationForm
from model_04 import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_registration.db'
app.config['SECRET_KEY'] =b'59b87c59045c81924047efde7229d74a6ba9e5b343fb7d7be935636f97d38c38'
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
db.init_app(app)


def add_user_to_db(user_name, user_email, user_password):
    user_name = request.form['name']
    user_email = request.form['email']
    user_password = request.form['password']
    hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
    new_user = User(user_name = user_name, user_email = user_email, user_password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    errors = []
    if request.method == 'POST' and form.validate():
        user_name = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
        new_user = User(name = user_name, email = user_email, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        if User.query.filter(User.name == user_name).count() > 0:
            errors.append(f'Username {user_name} is alredy exists!')
        if User.query.filter(User.email == user_email).count() > 0:
            errors.append(f'Email {user_email} is already exists!')
        return redirect(url_for('registration'))
    return render_template('registration.html', form=form, errors=errors)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database created successfully!')

if __name__ == '__main__':
    app.run(debug=True)