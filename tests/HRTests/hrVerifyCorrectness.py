from tqdm import tqdm

from algmatch.hospitalResidentsProblem import HospitalResidentsProblem

from tests.HRTests.utils.instanceGenerator import HRInstanceGenerator as InstanceGenerator
from tests.HRTests.utils.minmaxSMs import MMSMS


class VerifyCorrectness:
    def __init__(self, total_residents, total_hospitals, lower_bound, upper_bound):
        """
        It takes argument as follows (set in init):
            number of men
            number of women
            lower bound of the preference list length
            upper bound of the preference list length
        """

        self._total_residents = total_residents
        self._total_hospitals = total_hospitals
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

        self.gen = InstanceGenerator(self._total_residents, self._total_hospitals, self._lower_bound, self._upper_bound)
        self.current_instance = {}

        self._correct_count = 0
        self._incorrect_count = 0


    def generate_instances(self):
        self.current_instance = self.gen.generate_instance_no_ties()

    def verify_instance(self):

        minmaxer = MMSMS(dictionary=self.current_instance)
        resident_optimal_solver = HospitalResidentsProblem(dictionary=self.current_instance, optimisedSide="residents")
        hospital_optimal_solver = HospitalResidentsProblem(dictionary=self.current_instance, optimisedSide="hospitals")

        minmaxer.find_minmax_matchings()
        m_0 = resident_optimal_solver.get_stable_matching()
        m_z = hospital_optimal_solver.get_stable_matching()

        return m_z == minmaxer.minmax_matchings[-1] and m_0 == minmaxer.minmax_matchings[0]

    def run(self):
        self.generate_instances()
        if self.verify_instance():
            self._correct_count += 1
        else:
            self._incorrect_count += 1

    def show_results(self):
        print(f"""
            Total residents: {self._total_residents}
            Total hospitals: {self._total_hospitals}
            Preferene list length lower bound: {self._lower_bound}
            Preferene list length upper bound: {self._upper_bound}
            Repetitions: {self._correct_count + self._incorrect_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)

def main():
    TOTAL_RESIDENTS = 12
    TOTAL_HOSPITALS = 5
    LOWER_LIST_BOUND = 0
    UPPER_LIST_BOUND = 3
    REPETITIONS = 100_000

    verifier = VerifyCorrectness(TOTAL_RESIDENTS, TOTAL_HOSPITALS, LOWER_LIST_BOUND, UPPER_LIST_BOUND)
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    verifier.show_results()
    

if __name__ == '__main__':
    main()