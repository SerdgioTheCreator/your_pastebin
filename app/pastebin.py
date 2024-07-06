from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from about.about import about_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdgmsergyehto2q3ro12r34ihweg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pastebin.db'

db = SQLAlchemy(app)

app.register_blueprint(about_blueprint)


@app.route('/')
@app.route('/home')
def home():
    title = 'Pastebin'
    return render_template('index.html', title=title)


if __name__ == '__main__':
    app.run(debug=True)
