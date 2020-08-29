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


def calculate_average(list_of_numbers):
    return round_to(sum(list_of_numbers) / len(list_of_numbers), 0.5)


def round_to(number, granularity):
    return round(number * 1 / granularity) * granularity
