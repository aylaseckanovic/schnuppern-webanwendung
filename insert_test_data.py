#!/usr/bin/env python3

import random
import sqlite3

connection = sqlite3.connect('grades.db')

pupils = ['Alois', 'Bettina', 'Cyrille', 'Daniel', 'Ernst', 'Franziska']
subjects = ['Mathematik', 'Deutsch', 'Englisch', 'Sport', 'Musik']
c = connection.cursor()

pupil_ids = {}
for pupil in pupils:
    c.execute(f'INSERT INTO pupil (name) VALUES ("{pupil}")')
    new_id = c.execute('SELECT last_insert_rowid()')
    pupil_ids[pupil] = new_id.lastrowid

subject_ids = {}
for subject in subjects:
    c.execute(f'INSERT INTO subject (name) VALUES ("{subject}")')
    new_id = c.execute('SELECT last_insert_rowid()')
    subject_ids[subject] = new_id.lastrowid

for pupil, pupil_id in pupil_ids.items():
    for subject, subject_id in subject_ids.items():
        for i in range(0, random.randint(1, 10)):
            grade = random.randint(10, 60) / 10
            c.execute('INSERT INTO grade (pupil_id, subject_id, grade) '
                      f'VALUES ({pupil_id}, {subject_id}, {grade})')

connection.commit()
