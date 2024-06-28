from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return 'index.html'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name='Деля'):
    return render_template('hello.html', person=name)
