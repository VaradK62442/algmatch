"""
For any two instances of SPA-P, one can find the Mutual Attraction Distance
by first finding the Mutual Attraction Matrix of the two instances,
then using the defined Mutual Attraction Distance (MAD) formula.

This file contains a set of functions to perform this analysis, along with other related functions.
"""


import numpy as np
from itertools import permutations

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.fileReader import FileReader


def construct_mutual_attraction_matrix(filename: str) -> np.ndarray:
    """
    Given a SPA-P instance, construct the Mutual Attraction Matrix.

    The element at position (i, j) of the matrix MA is
    the position in l_k's preference list of the project p_x
    that is in position j of s_i's preference list,
    where l_k is the lecturer that offers p_x.

    :param filename: file name of a SPA-P instance
    :return: Mutual Attraction Matrix
    """
    instance = FileReader(filename)

    students = instance.students
    projects = instance.projects
    lecturers = instance.lecturers

    n = len(students)
    assert n >= 1, "Instance must have at least one student."
    l = len(students['s1'][0])

    MA = np.zeros((n, l))

    for s_i in students:
        MA[int(s_i[1:])-1] = np.array([
            lecturers[projects[p_x][1]][1].index(p_x) + 1
            for p_x in students[s_i][0]
        ])

    return MA


def mutual_attraction_distance(I: np.ndarray, J: np.ndarray) -> int:
    """
    Returns the Mutual Attraction Distance between two instances I, J of SPA-P.

    :param I: Mutual Attraction Matrix of instance I
    :param J: Mutual Attraction Matrix of instance J
    :return: Mutual Attraction Distance between I and J
    """

    assert I.shape == J.shape, "Instances must have the same shape (i.e. same number of students and length of student preference list)."

    perms = list(permutations(range(I.shape[0])))
    
    min_dist = float('inf')
    for p in perms:
        dist = 0
        for i, sigma_i in enumerate(p):
            dist += np.sum(np.abs(I[i] - J[sigma_i]))

        if dist < min_dist:
            min_dist = dist

    return int(min_dist)


def mutual_agreement_matrix(n, l) -> np.ndarray:
    """
    Return a Mutual Agreement matrix of shape (n, l).

    Mutual Agreement matrix = [
        [1, 2, 3, ..., l],
        [1, 2, 3, ..., l],
        [1, 2, 3, ..., l],
    ]
    
    :param n: number of students
    :param l: length of student preference list
    :return: Mutual Agreement matrix
    """
    return np.tile(np.arange(1, l+1), (n, 1))


def mutual_disagreement_matrix(n, l) -> np.ndarray:
    """
    Return a Mutual Disagreement matrix of shape (n, l).

    Mutual Disagreement matrix = [
        [l, l-1, l-2, ..., 1],
        [l, l-1, l-2, ..., 1],
        [l, l-1, l-2, ..., 1],
    ]
    
    :param n: number of students
    :param l: length of student preference list
    :return: Mutual Disagreement matrix
    """
    return np.tile(np.arange(l, 0, -1), (n, 1))


def MAD_distance_between_Ma_Md(n, l) -> int:
    """
    Returns the Mutual Attraction Distance between the Mutual Agreement and Mutual Disagreement matrices.

    :param n: number of students
    :param l: length of student preference list
    :return: Mutual Attraction Distance between the Mutual Agreement and Mutual Disagreement matrices
    """
    if l % 2 == 1:
        return n * (l ** 2 - 1) // 2
    else:
        return n * l ** 2 // 2


def main():
    MA_0 = construct_mutual_attraction_matrix("instances/instance_0.csv")
    MA_1 = construct_mutual_attraction_matrix("instances/instance_1.csv")

    print(f"MAD between MA_0 and MA_1: {mutual_attraction_distance(MA_0, MA_1)}")

    Ma = mutual_agreement_matrix(*MA_0.shape)
    Md = mutual_disagreement_matrix(*MA_0.shape)

    calculated_MAD = mutual_attraction_distance(Ma, Md)
    formula_MAD = MAD_distance_between_Ma_Md(*MA_0.shape)

    print(f"Calculated MAD between Ma and Md: {calculated_MAD}")
    print(f"Formula MAD between Ma and Md: {formula_MAD}")

    assert calculated_MAD == formula_MAD, f"Mismatch in MAD calculation: {calculated_MAD} != {formula_MAD}"


if __name__ == "__main__":
    main()