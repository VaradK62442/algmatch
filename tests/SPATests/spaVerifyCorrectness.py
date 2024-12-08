from tqdm import tqdm

from algmatch.studentProjectAllocation import StudentProjectAllocation

from instanceGenerator import SPAInstanceGenerator as InstanceGenerator
from enumerateSMs import ESMS

class VerifyCorrectness:
    def __init__(self, total_students, lower_project_bound, upper_project_bound):
        self._total_students = total_students
        self._lower_project_bound = lower_project_bound
        self._upper_project_bound = upper_project_bound

        self.gen = InstanceGenerator(self._total_students, self._lower_project_bound, self._upper_project_bound)
        self.current_instance = {}

        self._correct_count = 0
        self._incorrect_count = 0


    def generate_instances(self):
        self.current_instance = self.gen.generate_instance_no_ties()

    def verify_instance(self):

        enumerator = ESMS(dictionary=self.current_instance)
        student_optimal_solver = StudentProjectAllocation(dictionary=self.current_instance, optimisedSide="student")
        lecturer_optimal_solver = StudentProjectAllocation(dictionary=self.current_instance, optimisedSide="lecturer")

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
    REPETITIONS = 1000

    verifier = VerifyCorrectness(TOTAL_STUDENTS, LOWER_PROJECT_BOUND, UPPER_PROJECT_BOUND)
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    verifier.show_results()
    

if __name__ == '__main__':
    main()