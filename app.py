import os

from flask import Flask
from flask import render_template
from flask import send_from_directory

from data import pupils_grades

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@ app.route('/pupils', methods=['GET'])
def get_pupils():
    title = 'Notenverwaltung: Schüler'
    pupils = pupils_grades.keys()
    return render_template('pupils.jinja2', title=title, pupils=pupils)


@ app.route('/pupils/<name>', methods=['GET'])
def get_pupil(name):
    title = f'Notenverwaltung: {name}'
    subject_grades = pupils_grades[name]
    backlink = '/pupils'
    backlink_caption = 'Zurück zur Schülerübersicht'
    return render_template(
        'grades.jinja2',
        title=title,
        subject_grades=subject_grades,
        backlink=backlink,
        backlink_caption=backlink_caption,
    )
