from multiprocessing import Lock, Manager, Process
from time import perf_counter_ns, sleep
from tqdm import tqdm

from algmatch.stableMarriageProblem import StableMarriageProblem

from instanceGenerator import SMInstanceGenerator as InstanceGenerator
from minmaxSMs import MMSMS


class MultiVerifyCorrectness:
    def __init__(self, total_men, total_women,
                 lower_bound, upper_bound,
                 reps, result_dict):
        """
        It takes argument as follows (set in init):
            number of men
            number of women
            lower bound of the preference list length
            upper bound of the preference list length
        """

        self._total_men = total_men
        self._total_women = total_women
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

        self._reps = reps
        self.result_dict = result_dict
        self.lock = Lock()

        self.gen = InstanceGenerator(self._total_men, self._total_women, self._lower_bound, self._upper_bound)
        self.current_instance = {}

        self._correct_count = 0
        self._incorrect_count = 0


    def generate_instances(self):
        self.current_instance = self.gen.generate_instance_no_ties()

    def verify_instance(self):

        minmaxer = MMSMS(dictionary=self.current_instance)
        man_optimal_solver = StableMarriageProblem(dictionary=self.current_instance, optimisedSide="men")
        woman_optimal_solver = StableMarriageProblem(dictionary=self.current_instance, optimisedSide="women")

        minmaxer.find_minmax_matchings()
        m_0 = man_optimal_solver.get_stable_matching()
        m_z = woman_optimal_solver.get_stable_matching()

        return m_z == minmaxer.minmax_matchings[-1] and m_0 == minmaxer.minmax_matchings[0]
    

    def run(self):
        local_correct = 0
        local_incorrect = 0
        local_total = 0

        while local_total < self._reps:
            self.generate_instances()
            if self.verify_instance():
                local_correct += 1
                local_total += 1
                with self.lock:
                    self.result_dict['correct'] += 1
                    self.result_dict['total'] += 1
            else:
                local_incorrect += 1
                local_total += 1
                with self.lock:
                    self.result_dict['incorrect'] += 1
                    self.result_dict['total'] += 1
        
    def show_results(self):
        print(f"""
            Total men: {self._total_men}
            Total women: {self._total_women}
            Preference list length lower bound: {self._lower_bound}
            Preference list length upper bound: {self._upper_bound}
            Repetitions: {self.result_dict['correct'] + self.result_dict['incorrect']}

            Correct: {self.result_dict['correct']}
            Incorrect: {self.result_dict['incorrect']}
              """)

def main():
    n=5
    TOTAL_MEN = n
    TOTAL_WOMEN = n
    LOWER_LIST_BOUND = n
    UPPER_LIST_BOUND = n
    REPETITIONS = 2_500 # per thread
    THREADS = 16

    start = perf_counter_ns()
    with Manager() as manager:
        result_dict = manager.dict()
        result_dict['correct'] = 0
        result_dict['incorrect'] = 0
        result_dict['total'] = 0

        verifier = MultiVerifyCorrectness(TOTAL_MEN, TOTAL_WOMEN,
                                          LOWER_LIST_BOUND, UPPER_LIST_BOUND,
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
                pbar.n = result_dict['total']
                pbar.last_print_n = pbar.n
                pbar.update(0)

        for v_t in v_threads:
            v_t.join()
        
        end = perf_counter_ns()
        print(f"\nFinal Runtime: {(end-start)/1000**3}s")

        verifier.show_results()

if __name__ == '__main__':
    main()