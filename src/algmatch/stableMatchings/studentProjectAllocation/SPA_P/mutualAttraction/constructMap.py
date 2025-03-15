"""
Construct a map of instances.

n = number of students
l = length of student preference list

Given above parameters, construct a 'map' of instances:
1. generate an instance I of SPA-P using some instance generator
2. calculate MAD(Ma, I) and MAD(Md, I)
3. plot I on the map at (MAD(Ma, I), MAD(Md, I))
4. repeat for all instances
5. repeat for different instance generators
"""


import matplotlib.pyplot as plt
from collections import Counter
from itertools import chain

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.abstract import AbstractInstanceGenerator as SPAPIG_Abstract
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.attributes import SPAPIG_Attributes
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.euclidean import SPAPIG_Euclidean
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.expectations import SPAPIG_ExpectationsEuclidean
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.fame import SPAPIG_FameEuclidean
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.fameExtended import SPAPIG_FameEuclideanExtended
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.random import SPAPIG_Random
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.reverse import SPAPIG_ReverseEuclidean

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.mutualAttraction import *


def generate_instance(instance_generator: SPAPIG_Abstract, n: int, l: int, filename: str, **kwargs) -> None:
    """
    Generate an instance using a specific instance generator.

    :param instance_generator: instance generator type to use
    :param n: number of students
    :param l: length of student preference list
    :param filename: filename to write instance to
    :param kwargs: additional arguments for instance generator
    """
    IG: SPAPIG_Abstract = instance_generator(
        **kwargs,
        num_students=n,
        num_projects=2*n,
        num_lecturers=n,
        lower_bound=l,
        upper_bound=l,
        force_project_capacity=1,
        force_lecturer_capacity=1
    )
    IG.generate_instance()
    IG.write_instance_to_file(filename)


def get_Ma_distance(filename: str) -> int:
    """
    Get the MAD(Ma, I) distance of an instance.

    :param filename: filename of instance
    :return: MAD(Ma, I) distance
    """
    I = construct_mutual_attraction_matrix(filename)

    return mutual_attraction_distance(
        I,
        mutual_agreement_matrix(*I.shape)
    )


def get_Md_distance(filename: str) -> int:
    """
    Get the MAD(Md, I) distance of an instance.

    :param filename: filename of instance
    :return: MAD(Md, I) distance
    """
    I = construct_mutual_attraction_matrix(filename)

    return mutual_attraction_distance(
        I,
        mutual_disagreement_matrix(*I.shape)
    )


def main():
    colours = {
        SPAPIG_Attributes: 'red',
        SPAPIG_Euclidean: 'green',
        SPAPIG_ExpectationsEuclidean: 'blue',
        SPAPIG_FameEuclidean: 'orange',
        SPAPIG_FameEuclideanExtended: 'purple',
        SPAPIG_Random: 'yellow',
        SPAPIG_ReverseEuclidean: 'cyan'
    }
    
    instance_generators = list(colours.keys())

    n, l = 4, 4
    reps = 100 # for each IG
    default_filename = 'instance.csv'
    data = {}

    fig = plt.figure(figsize=(8, 8))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 4], height_ratios=[4, 1], wspace=0, hspace=0)

    ax_scatter = fig.add_subplot(gs[0, 1])
    for IG in instance_generators:
        print(f"Running {IG.__name__}...")
        Ma_distances, Md_distances = [], []
        for _ in range(reps):
            generate_instance(
                IG,
                n,
                l,
                default_filename
            )

            Ma_distances.append(get_Ma_distance(default_filename))
            Md_distances.append(get_Md_distance(default_filename))

        ax_scatter.scatter(Ma_distances, Md_distances, c='black')
        data[IG] = (np.array(Ma_distances), np.array(Md_distances))

    Ma, Md = mutual_agreement_matrix(n, l), mutual_disagreement_matrix(n, l)
    ax_scatter.scatter(mutual_attraction_distance(Ma, Md), mutual_attraction_distance(Md, Ma), c='black', marker='x', label='Ma vs Md')

    ax_scatter.set_xlabel('MAD(Ma, I)')
    ax_scatter.set_ylabel('MAD(Md, I)')
    ax_scatter.set_title('Map of Instances')

    plt.show()
    


if __name__ == "__main__":
    main()