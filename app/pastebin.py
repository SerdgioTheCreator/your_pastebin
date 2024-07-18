import os
from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', default='secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pastebin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<user {id}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SignupForm(FlaskForm):
    email = EmailField(
        validators=[InputRequired(), Length(min=4, max=30)],
        render_kw={'placeholder': 'Email address'}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=30)],
        render_kw={'placeholder': 'Password'}
    )
    submit = SubmitField('Signup')


class LoginForm(FlaskForm):
    email = EmailField(
        validators=[InputRequired(), Length(min=4, max=30)],
        render_kw={'placeholder': 'Email address'}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=30)],
        render_kw={'placeholder': 'Password'}
    )
    submit = SubmitField('Login')


class PasteForm(FlaskForm):
    text = TextAreaField(
        validators=[InputRequired(), Length(min=1, max=5000)],
        render_kw={'placeholder': 'Type your Paste!'}
    )
    submit = SubmitField('Paste')


@app.route('/')
@app.route('/index')
def index():
    form = PasteForm()
    return render_template('index.html', title='Pastebin', form=form)


@app.route('/about')
def about():
    title = 'about'
    return render_template('about/about.html', title=title)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('users/signup.html', title='Регистрация', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('login'))

    return render_template('users/login.html', title='Авторизация', form=form)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('/login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
