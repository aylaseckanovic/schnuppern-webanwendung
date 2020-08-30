#!/usr/bin/env python3

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

xs = np.linspace(-2.0, +2.0, 20)
ys = norm.pdf(xs)

for pupil, pupil_id in pupil_ids.items():
    baseline = random.choice([3.5, 4.0, 4.5, 5.0, 5.5])
    for subject, subject_id in subject_ids.items():
        deviations = random.choices(xs, weights=ys, k=random.randint(2, 8))
        for deviation in deviations:
            grade = round((baseline + deviation) * 10) / 10
            grade = max(1, min(6, grade))
            c.execute('INSERT INTO grade (pupil_id, subject_id, grade) '
                      f'VALUES ({pupil_id}, {subject_id}, {grade})')

connection.commit()
