from time import perf_counter_ns
from tqdm import tqdm

from tests.abstractTestClasses.abstractSingleVerifier import AbstractSingleVerifier as ASV
from tests.SPATests.spasVerifier import SPASAbstractVerifier as SPASAV

class SPASSingleVerifier(SPASAV, ASV):
    def __init__(self, total_students,
                 lower_project_bound, upper_project_bound):
        
        SPASAV.__init__(self, total_students,
                      lower_project_bound, upper_project_bound)
        ASV.__init__(self)

    def show_results(self):
        print(f"""
            Total students: {self._total_students}
            Lower project bound: {self._lower_project_bound}
            Upper project bound: {self._upper_project_bound}
            Repetitions: {self._total_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)

def main():
    TOTAL_STUDENTS = 5
    LOWER_PROJECT_BOUND = 3
    UPPER_PROJECT_BOUND = 3
    REPETITIONS = 40_000

    start = perf_counter_ns()

    verifier = SPASSingleVerifier(TOTAL_STUDENTS, LOWER_PROJECT_BOUND, UPPER_PROJECT_BOUND)
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    end = perf_counter_ns()
    print(f"\nFinal Runtime: {(end-start)/1000**3}s")

    verifier.show_results()
    

if __name__ == '__main__':
    main()