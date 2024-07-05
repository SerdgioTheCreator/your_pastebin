from flask import render_template
from app import app


@app.route('/')
@app.route('/home')
def home():
    title = 'Pastebin'
    return render_template('index.html', title=title)
