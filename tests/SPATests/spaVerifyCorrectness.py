from algmatch.studentProjectAllocation import StudentProjectAllocation

from instanceGenerator import SPAS as InstanceGenerator
from enumerateSMs import ESMS

import os
from tqdm import tqdm


class VerifyCorrectness:
    def __init__(self, total_students, lower_project_bound, upper_project_bound, write_to_file):
        self._total_students = total_students
        self._lower_project_bound = lower_project_bound
        self._upper_project_bound = upper_project_bound
        self._write_to_file = write_to_file

        self.gen = InstanceGenerator(self._total_students, self._lower_project_bound, self._upper_project_bound)

        self._default_filename = 'instance.txt'
        self._results_dir = 'results/'
        self._correct_count = 0
        self._incorrect_count = 0


    def generate_instances(self):
        self.gen.generate_instance_no_ties()
        self.gen.write_instance_no_ties(self._default_filename)

    def verify_instance(self):
        filename = self._default_filename

        enumerator = ESMS(filename)
        student_optimal_solver = StudentProjectAllocation(filename=filename, optimisedSide="student")
        lecturer_optimal_solver = StudentProjectAllocation(filename=filename, optimisedSide="lecturer")

        enumerator.find_all_stable_matchings()
        m_0 = student_optimal_solver.get_stable_matching()
        m_z = lecturer_optimal_solver.get_stable_matching()

        return m_z == enumerator.all_stable_matchings[-1] and m_0 == enumerator.all_stable_matchings[0]
    
    def run(self):
        self.generate_instances()
        if self.verify_instance():
            self._correct_count += 1
        else:
            self._incorrect_count += 1
            if self._write_to_file:
                self.gen.write_instance_no_ties(f"{self._results_dir}incorrect_instance_{self._incorrect_count}.txt")
    
        os.remove(self._default_filename)

    def show_results(self):
        print(f"""
            Total students: {self._total_students}
            Lower project bound: {self._lower_project_bound}
            Upper project bound: {self._upper_project_bound}
            Repetitions: {self._correct_count + self._incorrect_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)


def main():
    TOTAL_STUDENTS = 5
    LOWER_PROJECT_BOUND = 3
    UPPER_PROJECT_BOUND = 3
    REPETITIONS = 10_000
    WRITE_TO_FILE = False

    if WRITE_TO_FILE and not os.path.isdir("results"):
        os.mkdir("results")

    verifier = VerifyCorrectness(TOTAL_STUDENTS, LOWER_PROJECT_BOUND, UPPER_PROJECT_BOUND, WRITE_TO_FILE)
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    verifier.show_results()
    

if __name__ == '__main__':
    main()