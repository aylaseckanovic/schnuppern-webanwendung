#!/usr/bin/env python

import random
import sqlite3

import numpy as np
from scipy.stats import norm

connection = sqlite3.connect('grades.db')

pupils = [
    'Alois',
    'Bettina',
    'Carlo',
    'Daniela',
    'Ernst',
    'Franziska',
    'Gustav',
    'Helene',
    'Igor',
    'Jana',
    'Kilian',
    'Lena',
    'Michael',
    'Nora',
    'Oliver',
    'Paula',
    'Quentin',
    'Rita',
    'Silvio',
    'Thea',
    'Ulrich',
    'Verena',
    'Walter',
    'Xenia',
    'Yannick',
    'Zoe']

subjects = [
    'Mathematik',
    'Deutsch',
    'Englisch',
    'Französisch',
    'Sport',
    'Musik']

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

xs = np.linspace(-3.5, +1.5, 500)
ys = norm.pdf(xs)

for pupil, pupil_id in pupil_ids.items():
    baseline = 4.5 + random.choices(xs, weights=ys, k=1)[0]
    for subject, subject_id in subject_ids.items():
        deviations = random.choices(xs, weights=ys, k=random.randint(1, 10))
        for deviation in deviations:
            grade = round((baseline + deviation) * 10) / 10
            c.execute('INSERT INTO grade (pupil_id, subject_id, grade) '
                      f'VALUES ({pupil_id}, {subject_id}, {grade})')

connection.commit()
