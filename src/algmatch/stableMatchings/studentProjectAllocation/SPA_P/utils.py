"""
Set of utility functions for SPA-P.
"""

import numpy as np
from pprint import pprint

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.fileReader import FileReader


def instance_to_numpy(instance_filename: str):
    """
    Function to take an instance of SPA-P defined in a file,
    and turn it into a numpy array with the following structure:

    Shape = (num_students + num_lecturers, num_projects)
    Each row corresponds to a student or lecturer, and each column corresponds to a project.

    Each entry is 0 if the student / lecturer does not have the corresponding project on their preference list.
    Otherwise, the entry is the rank of the project on their preference list, normalied such that rows sum to 1.
        Most preferred project has highest value, least preferred project has lowest value.
    """
    r = FileReader(instance_filename)

    num_students = len(r.students)
    num_lecturers = len(r.lecturers)
    num_projects = len(r.projects)

    # create numpy array
    instance = np.zeros((num_students + num_lecturers, num_projects))

    # TODO: vectorise these loops

    # fill in student preferences
    for student in r.students:
        pref_list_len = len(r.students[student][0])
        sum_to_pref_list_len = (pref_list_len ** 2 + pref_list_len) // 2
        for i, project in enumerate(r.students[student][0]):
            instance[int(student[1:])-1, int(project[1:])-1] = (pref_list_len - i) / (sum_to_pref_list_len)

    # fill in lecturer preferences
    for lecturer in r.lecturers:
        pref_list_len = len(r.lecturers[lecturer][1])
        sum_to_pref_list_len = (pref_list_len ** 2 + pref_list_len) // 2
        for i, project in enumerate(r.lecturers[lecturer][1]):
            instance[num_students + int(lecturer[1:])-1, int(project[1:])-1] = (pref_list_len - i) / (sum_to_pref_list_len)

    return instance


def main():
    res = instance_to_numpy("test.txt")
    pprint(res)


if __name__ == "__main__":
    main()