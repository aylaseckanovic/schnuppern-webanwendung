from collections import namedtuple
import sqlite3


Pupil = namedtuple('pupil', ['id', 'name'])
Subject = namedtuple('subject', ['id', 'name'])
Grade = namedtuple('grade', ['id', 'pupil', 'subject', 'grade'])


class DataBase:

    def __init__(self, db_path):
        self.db_path = db_path

    def load_pupils(self):
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            pupils = []
            result = c.execute('SELECT id, name FROM pupil')
            for row in result.fetchall():
                p = Pupil(id=row[0], name=row[1])
                pupils.append(p)
            return pupils

    def load_pupil_id(self, name):
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            result = c.execute(
                f'SELECT pupil.id FROM pupil WHERE name = "{name}"')
            for row in result.fetchall():
                return int(row[0])

    def insert_pupil(self, name):
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            c.execute(f'INSERT INTO pupil (name) VALUES ("{name}")')

    def remove_pupil(self, name):
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            c.execute(f'DELETE FROM pupil WHERE name = "{name}"')

    def load_subject_grades(self, name):
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            subject_grades = {}
            result = c.execute(
                'SELECT grade.grade, subject.name ' +
                'FROM grade ' +
                'JOIN subject ON (grade.subject_id = subject.id) ' +
                'JOIN pupil ON (grade.pupil_id = pupil.id) ' +
                f'WHERE pupil.name="{name}" ' +
                'ORDER BY subject.name ASC')
            for row in result.fetchall():
                subject = row[1]
                if subject not in subject_grades:
                    subject_grades[subject] = []
                subject_grades[subject].append(row[0])  
        return subject_grades

    def load_subjects(self):
        subjects = []
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            result = c.execute('SELECT subject.id, subject.name FROM subject')
            for row in result.fetchall():
                subject = Subject(id=row[0], name=row[1])
                subjects.append(subject)
        return subjects

    def insert_subject(self, name):
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            c.execute(f'INSERT INTO subject (name) VALUES ("{name}")')

    def remove_subject(self, name):
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            c.execute(f'DELETE FROM subject WHERE name = "{name}"')

    def insert_grade(self, subject_id, pupil_id, grade):
        with sqlite3.connect(self.db_path) as con:
            c = con.cursor()
            c.execute(
                'INSERT INTO grade (subject_id, pupil_id, grade) ' +
                f'VALUES ({subject_id}, {pupil_id}, {grade})')
