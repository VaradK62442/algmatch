from multiprocessing import Manager, Process
from time import perf_counter_ns, sleep
from tqdm import tqdm

from tests.abstractTestClasses.abstractMultiVerifier import AbstractMultiVerifier as AMV
from tests.SPATests.spasVerifier import SPASAbstractVerifier as SPASAV

class SPASMultiVerifier(SPASAV, AMV):
    def __init__(self, total_students,
                 lower_project_bound, upper_project_bound,
                 reps, result_dict):
        
        SPASAV.__init__(self, total_students,
                      lower_project_bound, upper_project_bound)
        AMV.__init__(self, reps, result_dict)

    def show_results(self):
        print(f"""
            Total students: {self._total_students}
            Lower project bound: {self._lower_project_bound}
            Upper project bound: {self._upper_project_bound}
            Repetitions: {self.result_dict['total']}

            Correct: {self.result_dict['correct']}
            Incorrect: {self.result_dict['incorrect']}
              """)

def main():
    TOTAL_STUDENTS = 5
    LOWER_PROJECT_BOUND = 3
    UPPER_PROJECT_BOUND = 3
    REPETITIONS = 10_000 # per thread
    THREADS = 4

    start = perf_counter_ns()

    with Manager() as manager:
        result_dict = manager.dict()
        verifier = SPASMultiVerifier(TOTAL_STUDENTS,
                                     LOWER_PROJECT_BOUND, UPPER_PROJECT_BOUND,
                                     REPETITIONS, result_dict)
        v_threads = []
        for _ in range(THREADS):
            thread = Process(target=verifier.run)
            v_threads.append(thread)

        for v_t in v_threads:
            v_t.start()

        with tqdm(total=REPETITIONS*THREADS) as pbar:
            while any(thread.is_alive() for thread in v_threads):
                sleep(0.25)
                pbar.n = verifier.result_dict['total']
                pbar.last_print_n = pbar.n
                pbar.update(0)

        for v_t in v_threads:
            v_t.join()
        
        end = perf_counter_ns()
        print(f"\nFinal Runtime: {(end-start)/1000**3}s")

        verifier.show_results()
    

if __name__ == '__main__':
    main()