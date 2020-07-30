import os

from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory

from data import DataBase

app = Flask(__name__)
db = DataBase()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@ app.route('/pupils', methods=['GET'])
def get_pupils():
    title = 'Notenverwaltung: Schüler'
    pupils = db.load_pupils()
    pupils = [p.name for p in pupils]
    return render_template('pupils.jinja2', title=title, pupils=pupils)


@ app.route('/pupils/<name>', methods=['GET'])
def get_pupil(name):
    title = f'Notenverwaltung: {name}'
    subject_grades = db.load_subject_grades(name)
    backlink = '/pupils'
    backlink_caption = 'Zurück zur Schülerübersicht'
    return render_template(
        'grades.jinja2',
        title=title,
        subject_grades=subject_grades,
        backlink=backlink,
        backlink_caption=backlink_caption,
    )


@app.route('/add_pupil', methods=['POST'])
def add_pupil():
    name = request.form.get('new_pupil_name')
    pupils = db.load_pupils()
    names = [p.name for p in pupils]
    if name in names:
        raise ValueError(f'"{name}" already exists')
    db.insert_pupil(name)
    return get_pupils()


@app.route('/remove_pupil/<name>', methods=['GET'])
def delete_pupil(name):
    db.remove_pupil(name)
    return get_pupils()
