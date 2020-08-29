import os

from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory

from calculations import calculate_average
from calculations import calculate_deficiency_points
from calculations import calculate_overall_average
from calculations import calculate_subject_averages
from data import DataBase

app = Flask(__name__)
db = DataBase('grades.db')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def index():
    title = 'Notenverwaltung'
    pages = {
        'Schüler': '/pupils',
        'Fächer': '/subjects',
        'Notenüberblick': '/overview',
    }
    return render_template('index.jinja2', title=title, pages=pages)


@app.route('/pupils', methods=['GET'])
def get_pupils():
    title = 'Notenverwaltung: Schüler'
    pupils = db.load_pupils()
    pupils = [p.name for p in pupils]
    return render_template('pupils.jinja2', title=title, pupils=pupils)


@app.route('/pupils/<name>', methods=['GET'])
def get_pupil(name):
    title = f'Notenverwaltung: {name}'
    subject_grades = db.load_subject_grades(name)
    backlink = '/pupils'
    backlink_caption = 'Zurück zur Schülerübersicht'
    average_by_subject = calculate_subject_averages(subject_grades)
    average_overall = calculate_overall_average(average_by_subject)
    subjects = db.load_subjects()
    deficiency_points = calculate_deficiency_points(average_by_subject)
    return render_template(
        'grades.jinja2',
        title=title,
        pupil_name=name,
        subject_grades=subject_grades,
        average_by_subject=average_by_subject,
        average_overall=average_overall,
        deficiency_points=deficiency_points,
        backlink=backlink,
        backlink_caption=backlink_caption,
        subjects=subjects,
    )


@app.route('/remove_pupil/<name>', methods=['GET'])
def delete_pupil(name):
    db.remove_pupil(name)
    return get_pupils()


@app.route('/add_pupil', methods=['POST'])
def add_pupil():
    new_pupil_name = request.form.get('new_pupil_name')
    pupils = db.load_pupils()
    names = [p.name for p in pupils]
    if new_pupil_name in names:
        raise ValueError(f'pupil "{new_pupil_name}" already exists')
    db.insert_pupil(new_pupil_name)
    return get_pupils()


@app.route('/subjects', methods=['GET'])
def get_subjects():
    title = 'Notenverwaltung: Fächer'
    subjects = db.load_subjects()
    subjects = [s.name for s in subjects]
    return render_template('subjects.jinja2', title=title, subjects=subjects)


@app.route('/add_subject', methods=['POST'])
def add_subject():
    new_subject_name = request.form.get('new_subject_name')
    subjects = db.load_subjects()
    subject_names = [s.name for s in subjects]
    if new_subject_name in subject_names:
        raise ValueError(f'subject "{new_subject_name}" already exists')
    db.insert_subject(new_subject_name)
    return get_subjects()


@app.route('/remove_subject/<name>', methods=['GET'])
def delete_subject(name):
    db.remove_subject(name)
    return get_subjects()


@app.route('/<pupil>/add_grade', methods=['POST'])
def add_grade(pupil):
    grade_value = request.form.get('grade')
    subject_id = request.form.get('subject')
    pupil_id = db.load_pupil_id(pupil)
    db.insert_grade(subject_id, pupil_id, grade_value)
    return get_pupil(pupil)


@app.route('/overview', methods=['GET'])
def overview():
    subjects = db.load_subjects()
    subject_names = [s.name for s in subjects]

    entries = []
    pupils = db.load_pupils()
    for pupil in pupils:
        averages = []
        subject_grades = db.load_subject_grades(pupil.name)
        average_by_subject = calculate_subject_averages(subject_grades)
        for subject in subject_names:
            if subject in average_by_subject:
                averages.append(average_by_subject[subject])
            else:
                averages.append(0)
        average_overall = calculate_overall_average(average_by_subject)
        entries.append([pupil.name] + averages + [average_overall])

    sort_by = request.args.get('sort')
    if sort_by == 'Schüler':
        print('order by name')
        entries.sort(key=lambda e: e[0])
    elif sort_by == 'Durchschnitt':
        entries.sort(key=lambda e: e[len(e) - 1], reverse=True)
        print('order by average')
    elif sort_by:
        if sort_by in subject_names:
            pos = subject_names.index(sort_by)
            entries.sort(key=lambda e: e[pos + 1], reverse=True)

    summary = ['⌀']
    summary_cols = subject_names + ['Durchschnitt']
    for subject in summary_cols:
        averages = []
        offset = 1 + summary_cols.index(subject)
        for entry in entries:
            if entry[offset]:
                averages.append(entry[offset])
        summary.append(calculate_average(averages, granularity=0.01))

    return render_template(
        'overview.jinja2',
        title='Notenüberblick',
        table_header=['Schüler'] + subject_names + ['Durchschnitt'],
        table_body=entries,
        table_footer=summary,
    )
