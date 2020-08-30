def calculate_subject_averages(subject_grades):
    subject_averages = {}
    for subject, grades in subject_grades.items():
        subject_average = calculate_average(grades)
        subject_averages[subject] = subject_average
    return subject_averages


def calculate_overall_average(average_by_subject):
    if len(average_by_subject) == 0:
        return 0
    total = 0
    for grade in average_by_subject.values():
        total += grade
    return round_to(total / len(average_by_subject), 0.1)


def calculate_average(list_of_numbers, granularity=0.5):
    if len(list_of_numbers) < 1:
        return None
    return round_to(sum(list_of_numbers) / len(list_of_numbers), granularity)


def round_to(number, granularity):
    return round(number * 1 / granularity) * granularity


def calculate_deficiency_points(average_by_subject):
    # standardmässig gibt es keine Mangelpunkte
    deficiency_points = 0.0

    # gehe alle Notendurchschnitte durch
    for average in average_by_subject.values():
        # Falls der Notendurchschnitt ungenügend ist (d.h. kleiner als 4.0),
        # gibt es Mangelpunkte. Die Anzahl Mangelpunkte pro Fach ist die
        # Differenz zwischen 4.0 und der erreichten Note.
        # TODO: Berechne die Mangelpunkte für das jeweilige Fach und addiere
        # diese zu deficiency_points. Beispiel: für die Note 3.5 gibt es 0.5
        # Mangelpunkte, für die Note 3.0 gibt es 1.0 Mangelpunkte, und für die
        # Note 4.5 gibt es 0.0 Mangelpunkte.

        # TODO: diese Zeile kann gelöscht werden, sobald der Code fertig ist.
        pass

    # hier wird das Resultat zurückgegeben
    return deficiency_points
