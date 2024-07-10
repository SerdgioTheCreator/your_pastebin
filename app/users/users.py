from flask import Blueprint, render_template

users_blueprint = Blueprint('users', __name__, template_folder='../templates/users/', static_folder='static')


@users_blueprint.route('/signup')
def about():
    title = 'Регистрация'
    return render_template('signup.html', title=title)


@users_blueprint.route('/login')
def login():
    title = 'Авторизация'
    return render_template('login.html', title=title)
