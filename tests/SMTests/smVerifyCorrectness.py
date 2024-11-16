import os
from tqdm import tqdm

from algmatch.stableMarriageProblem import StableMarriageProblem

from instanceGenerator import SMInstanceGenerator as InstanceGenerator
from enumerateSMs import ESMS


class VerifyCorrectness:
    def __init__(self, total_men, total_women, lower_bound, upper_bound, write_to_file):
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
        self._write_to_file = write_to_file

        self.gen = InstanceGenerator(self._total_men, self._total_women, self._lower_bound, self._upper_bound)

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
        man_optimal_solver = StableMarriageProblem(filename=filename, optimisedSide="men")
        woman_optimal_solver = StableMarriageProblem(filename=filename, optimisedSide="women")

        enumerator.find_all_stable_matchings()
        m_0 = man_optimal_solver.get_stable_matching()
        m_z = woman_optimal_solver.get_stable_matching()

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
            Total men: {self._total_men}
            Total women: {self._total_women}
            Preferene list length lower bound: {self._lower_bound}
            Preferene list length upper bound: {self._upper_bound}
            Repetitions: {self._correct_count + self._incorrect_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)

def main():
    n=9
    TOTAL_MEN = n
    TOTAL_WOMEN = n
    LOWER_LIST_BOUND = n
    UPPER_LIST_BOUND = n
    REPETITIONS = 1
    WRITE_TO_FILE = False

    if WRITE_TO_FILE and not os.path.isdir("results"):
        os.mkdir("results")

    verifier = VerifyCorrectness(TOTAL_MEN, TOTAL_WOMEN, LOWER_LIST_BOUND, UPPER_LIST_BOUND, WRITE_TO_FILE)
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    verifier.show_results()
    

if __name__ == '__main__':
    main()