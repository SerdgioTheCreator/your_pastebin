from flask import Blueprint, render_template

about_blueprint = Blueprint('about', __name__, template_folder='../templates/about/', static_folder='static')


@about_blueprint.route('/about')
def about():
    title = 'about'
    return render_template('about.html', title=title)
