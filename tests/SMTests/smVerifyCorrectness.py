from time import perf_counter_ns
from tqdm import tqdm

from algmatch.stableMarriageProblem import StableMarriageProblem

from instanceGenerator import SMInstanceGenerator as InstanceGenerator
from minmaxSMs import MMSMS


class VerifyCorrectness:
    def __init__(self, total_men, total_women, lower_bound, upper_bound):
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
        self.generate_instances()
        if self.verify_instance():
            self._correct_count += 1
        else:
            self._incorrect_count += 1


    def show_results(self):
        print(f"""
            Total men: {self._total_men}
            Total women: {self._total_women}
            Preference list length lower bound: {self._lower_bound}
            Preference list length upper bound: {self._upper_bound}
            Repetitions: {self._correct_count + self._incorrect_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)

def main():
    n=5
    TOTAL_MEN = n
    TOTAL_WOMEN = n
    LOWER_LIST_BOUND = n
    UPPER_LIST_BOUND = n
    REPETITIONS = 40_000

    start = perf_counter_ns()

    verifier = VerifyCorrectness(TOTAL_MEN, TOTAL_WOMEN, LOWER_LIST_BOUND, UPPER_LIST_BOUND)
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    end = perf_counter_ns()
    print(f"\nFinal Runtime: {(end-start)/1000**3}s")

    verifier.show_results()
    

if __name__ == '__main__':
    main()