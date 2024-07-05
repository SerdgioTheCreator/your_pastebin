from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdgmsergyehto2q3ro12r34ihweg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pastebin.db'

db = SQLAlchemy(app)

from app.pastebin import routes


if __name__ == '__main__':
    app.run(debug=True)
