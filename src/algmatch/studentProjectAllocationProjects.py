"""
Class to provide interface for the SPA-P stable matching algorithm.
Also provides class for running several iterations, as well as configuring different variables.
"""

import os
import math
import argparse

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerator import SPAPIG
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.SPAPSolver import GurobiSPAP
from algmatch.stableMatchings.studentProjectAllocation.SPA_P.checkStability import StabilityChecker


class StudentProjectAllocationProjectsSingle:
    def __init__(
            self, 
            filename: str | None = None, 
            output: str | None = None,
            output_flag: 0 | 1 = 1
    ) -> None:
        """
        Initialise the SPA-P algorithm.

        :param filename: str, optional, default=None, the path to the file to read in the preferences from.      
        :param output: str, optional, default=None, the path to the file to write the output to. Will print to console if None.

        :param output_flag: 0 or 1, optional, default=1, the flag to determine whether to output the Gurobi solver output.
        """
        assert filename is not None, "Filename must be provided"

        self.filename = os.path.join(os.getcwd(), filename)
        self.output_file = os.path.join(os.getcwd(), output) if output is not None else None
        self.solver = GurobiSPAP(filename=filename, output_flag=output_flag)


    def get_stable_matching(self) -> dict | str:
        """
        Get the stable matching for the Student Project Allocation algorithm.
        Also writes the output to file or console, as specified.

        :return: dict, the stable matching.
        """
        self.solver.solve()

        result = "\n".join([f"{s[1:]} {p[1:]}" for s, p in self.solver.matching.items()])
        print(result, file=None if self.output_file is None else open(self.output_file, 'w'))

        checker = StabilityChecker(self.solver)
        
        return self.solver.matching if checker.check_stability() else "Matching is not stable."
    

class StudentProjectAllocationProjectsMultiple:
    def __init__(
            self,
            iters: int = 1,
            students: int = 5,
            lower_bound: int = 1,
            upper_bound: int = 3,
            project_ratio: float = 0.5,
            lecturer_ratio: float = 0.2,
            instance_folder: str = "instances/",
            solutions_folder: str = "solutions/",
            output_flag: 0 | 1 = 1
    ):
        """
        Run several iterations of the SPA-P algorithm.

        :param iters: int, optional, default=1, the number of iterations to run the SPA-P algorithm for.
        :param students: int, optional, default=5, the number of students.
        :param lower_bound: int, optional, default=1, the lower bound of projects a student can rank.
        :param upper_bound: int, optional, default=3, the upper bound of projects a student can rank.
        :param project_ratio: float, optional, default=0.5, the ratio of projects to students.
        :param lecturer_ratio: float, optional, default=0.2, the ratio of lecturers to students.
        :param instance_folder: str, optional, default="instances/", the folder to save the instances to.
        :param solutions_folder: str, optional, default="solutions/", the folder to save the solutions to.
        :param output_flag: 0 or 1, optional, default=1, the flag to determine whether to output the Gurobi solver output.
        """
        
        assert lower_bound <= upper_bound, "Lower bound must be less than or equal to upper bound."
        assert upper_bound <= int(math.ceil(students * project_ratio)), "Upper bound must be less than or equal to number of students * project ratio."

        self.iters = iters
        self.num_students = students
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.project_ratio = project_ratio
        self.lecturer_ratio = lecturer_ratio

        self.instance_folder = os.path.join(os.getcwd(), instance_folder)
        self.solutions_folder = os.path.join(os.getcwd(), solutions_folder)

        if not os.path.exists(self.instance_folder):
            os.makedirs(self.instance_folder)

        if not os.path.exists(self.solutions_folder):
            os.makedirs(self.solutions_folder)

        self.output_flag = output_flag


    def _save_instance(self, filename: str) -> None:
        S = SPAPIG(self.num_students, self.lower_bound, self.upper_bound)
        S.generate_instance()
        S.write_instance_to_file(filename)


    def _write_solution(self, matching: dict, filename: str) -> None:
        with open(filename, 'w') as f:
            for student in matching:
                f.write(f"{student[1:]} {matching[student][1:]}\n")

    
    def run(self) -> None:
        """
        Runs solver for number of iterations specified.
        """
        print(f"Running {self.iters} iterations of SPA-P algorithm.")

        for i in range(self.iters):
            filename = self.instance_folder + f"instance_{i}.txt"
            self._save_instance(filename)

            solver = GurobiSPAP(filename=filename, output_flag=self.output_flag)
            solver.solve()
            checker = StabilityChecker(solver)
            is_stable = checker.check_stability()

            if is_stable:
                self._write_solution(solver.matching, self.solutions_folder + f"solution_{i}.txt")
            else:
                print(f"Instance {i} is not stable.")


def main():

    def help_msg(name=None):
        msg="""
        Usage: python3 main.py [--single | --multiple] [options]

        Run the SPA-P algorithm for a single instance:
            python3 main.py --single --filename FILENAME --output OUTPUT --output_flag OUTPUT_FLAG

        Run the SPA-P algorithm for multiple instances:
            python3 main.py --multiple --iters ITERS --students STUDENTS --lower_bound LOWER_BOUND --upper_bound UPPER_BOUND --project_ratio PROJECT_RATIO --lecturer_ratio LECTURER_RATIO --instance_folder INSTANCE_FOLDER --solutions_folder SOLUTIONS_FOLDER --output_flag OUTPUT_FLAG
        """
        return msg
    
    parser = argparse.ArgumentParser(description="Run the SPA-P algorithm.", usage=help_msg())

    parser.add_argument("--single", action="store_true", help="Run the SPA-P algorithm for a single instance.")
    
    parser.add_argument("--filename", type=str, help="The filename of the instance to run the SPA-P algorithm on.")
    parser.add_argument("--output", type=str, help="The filename to write the output to.")

    parser.add_argument("--multiple", action="store_true", help="Run the SPA-P algorithm for multiple instances.")

    parser.add_argument("--iters", type=int, default=1, help="The number of iterations to run the SPA-P algorithm for.")
    parser.add_argument("--students", type=int, default=5, help="The number of students.")
    parser.add_argument("--lower_bound", type=int, default=1, help="The lower bound of projects a student can rank.")
    parser.add_argument("--upper_bound", type=int, default=3, help="The upper bound of projects a student can rank.")
    parser.add_argument("--project_ratio", type=float, default=0.5, help="The ratio of projects to students.")
    parser.add_argument("--lecturer_ratio", type=float, default=0.2, help="The ratio of lecturers to students.")
    parser.add_argument("--instance_folder", type=str, default="instances/", help="The folder to save the instances to.")
    parser.add_argument("--solutions_folder", type=str, default="solutions/", help="The folder to save the solutions to.")
    parser.add_argument("--output_flag", type=int, default=1, help="The flag to determine whether to output the Gurobi solver output.")

    args = parser.parse_args()

    if not any([args.single, args.multiple]) or all([args.single, args.multiple]):
        parser.print_help()
        return

    if args.single:
        spa = StudentProjectAllocationProjectsSingle(
            filename=args.filename,
            output=args.output,
            output_flag=args.output_flag
        )
        spa.get_stable_matching()

    elif args.multiple:
        spa = StudentProjectAllocationProjectsMultiple(
            iters=args.iters,
            students=args.students,
            lower_bound=args.lower_bound,
            upper_bound=args.upper_bound,
            project_ratio=args.project_ratio,
            lecturer_ratio=args.lecturer_ratio,
            instance_folder=args.instance_folder,
            solutions_folder=args.solutions_folder,
            output_flag=args.output_flag
        )
        spa.run()


if __name__ == "__main__":
    main()