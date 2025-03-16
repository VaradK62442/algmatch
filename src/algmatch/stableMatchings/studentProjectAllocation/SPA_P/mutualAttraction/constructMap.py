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
from tqdm import tqdm

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
    reps = 100_000 # for each IG
    default_filename = 'instance.csv'
    data = {}
    min_Ma, min_Md = float('inf'), float('inf')

    fig = plt.figure(figsize=(8, 8))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 4], height_ratios=[4, 1], wspace=0, hspace=0)

    ax_scatter = fig.add_subplot(gs[0, 1])
    print("Generating instances...")
    for IG in tqdm(instance_generators):
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

            if Ma_distances[-1] < min_Ma:
                min_Ma = Ma_distances[-1]

            if Md_distances[-1] < min_Md:
                min_Md = Md_distances[-1]

        ax_scatter.scatter(Ma_distances, Md_distances, c='black')
        data[IG] = (np.array(Ma_distances), np.array(Md_distances))

    MAD_Ma_Md = MAD_distance_between_Ma_Md(n, l)

    ax_scatter.scatter(
        MAD_Ma_Md, MAD_Ma_Md,
        c='black', marker='x', label='Ma vs Md'
    )

    ax_scatter.set_xlabel('MAD(Ma, I)')
    ax_scatter.set_ylabel('MAD(Md, I)')
    ax_scatter.set_title(f'Map of all Instances')
    ax_scatter.legend()

    ax_bar_Ma = fig.add_subplot(gs[1, 1], sharex=ax_scatter)
    ax_bar_Md = fig.add_subplot(gs[0, 0], sharey=ax_scatter)

    lower_bound = min(min_Ma, min_Md)

    print("Generating histograms...")
    for IG, colour in tqdm(colours.items()):
        Ma_distances, Md_distances = data[IG]
        bottom_Ma, bottom_Md = np.zeros(MAD_Ma_Md - lower_bound), np.zeros(MAD_Ma_Md - lower_bound)

        ax_bar_Ma.cla()
        ax_bar_Md.cla()

        ax_bar_Ma.hist(Ma_distances, bottom=bottom_Ma, bins=range(lower_bound, MAD_Ma_Md+1), color=colour, alpha=0.5)
        ax_bar_Md.hist(Md_distances, bottom=bottom_Md, bins=range(lower_bound, MAD_Ma_Md+1), color=colour, alpha=0.5, orientation='horizontal')
        bottom_Ma += np.array([Counter(Ma_distances)[i] for i in range(lower_bound, MAD_Ma_Md)])
        bottom_Md += np.array([Counter(Md_distances)[i] for i in range(lower_bound, MAD_Ma_Md)])

        ax_bar_Ma.set_title(f'MAD(Ma, I) Histogram')
        ax_bar_Ma.set_ylabel('Frequency')

        ax_bar_Md.set_title(f'MAD(Md, I) Histogram')
        ax_bar_Md.set_xlabel('Frequency')

        plt.savefig(f"maps/map_{IG.__name__}.png")    


if __name__ == "__main__":
    main()