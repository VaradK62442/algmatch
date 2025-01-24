"""
Execute the SPA-P algorithm using Gurobi IP, check for blocking pairs and coalition stability, and output results.
Can also specify number of instances to solve. This will save the files by default.
"""

import sys
import os

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerator import SPAPIG
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.SPAPSolver import GurobiSPAP
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.checkStability import StabilityChecker


def save_instance(filename: str, students, lower_bound, upper_bound) -> None:
    S = SPAPIG(students, lower_bound, upper_bound)
    S.generate_instance()
    S.write_instance_to_file(filename)


def write_solution(matching: dict, filename: str) -> None:
    with open(filename, 'w') as f:
        for student in matching:
            f.write(f"{student[1:]} {matching[student][1:]}\n")


def main(iters: int, students=5, lower_bound=1, upper_bound=3, output_flag=1) -> None:

    INSTANCE_FOLDER = "instances/"
    SOLUTIONS_FOLDER = "solutions/"

    if not os.path.exists(INSTANCE_FOLDER):
        os.makedirs(INSTANCE_FOLDER)

    if not os.path.exists(SOLUTIONS_FOLDER):
        os.makedirs(SOLUTIONS_FOLDER)

    for i in range(iters):
        filename = INSTANCE_FOLDER + f"instance_{i}.txt"
        save_instance(filename, students, lower_bound, upper_bound)

        solver = GurobiSPAP(filename=filename, output_flag=output_flag)
        solver.solve()

        checker = StabilityChecker(solver)
        stability = checker.check_stability()

        if stability:
            write_solution(solver.matching, SOLUTIONS_FOLDER + f"solution_{i}.txt")
        else:
            print(f"Instance {i} is not stable.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <iters> [num_students] [lower_bound] [upper_bound] [gurobi_output_flag]")
        sys.exit(1)

    if len(sys.argv) == 2: main(iters=int(sys.argv[1]))
    else:
        main(int(sys.argv[1]), *map(int, sys.argv[2:]))