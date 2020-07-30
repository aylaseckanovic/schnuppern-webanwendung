from collections import namedtuple
import sqlite3


Pupil = namedtuple('pupil', ['id', 'name'])
Subject = namedtuple('subject', ['id', 'name'])
Grade = namedtuple('grade', ['id', 'pupil', 'subject', 'grade'])


class DataBase():

    def load_pupils(self):
        with sqlite3.connect('grades.db') as con:
            c = con.cursor()
            pupils = []
            result = c.execute('SELECT id, name FROM pupil')
            for row in result.fetchall():
                p = Pupil(id=row[0], name=row[1])
                pupils.append(p)
            return pupils

    def remove_pupil(self, name):
        with sqlite3.connect('grades.db') as con:
            c = con.cursor()
            c.execute(f'DELETE FROM pupil WHERE name = "{name}"')

    def load_subject_grades(self, name):
        with sqlite3.connect('grades.db') as con:
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

    def insert_pupil(self, name):
        with sqlite3.connect('grades.db') as con:
            c = con.cursor()
            c.execute(f'INSERT INTO pupil (name) VALUES ("{name}")')
