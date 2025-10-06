from algmatch.stableRoommatesProblem import StableRoommatesProblem

from tests.SRTests.utils.srInstanceGenerator import SRInstanceGenerator
from tests.SRTests.utils.srEnumerator import SREnumerator


class SRVerifier:
    def __init__(self, no_roommates):
        self._total_roommates = no_roommates
        self.gen = SRInstanceGenerator(no_roommates)
        self.current_instance = {}

    def generate_instance(self):
        self.current_instance = self.gen.generate_instance()

    def verify_instance(self):
        bruteforcer = SREnumerator(dictionary=self.current_instance)
        solver = StableRoommatesProblem(dictionary=self.current_instance)

        bruteforcer.find_stable_matchings()
        matching = solver.get_stable_matching()

        if not solver.sr_alg.is_stable:
            if not bruteforcer.stable_matching_list:
                return True
            return False

        if matching not in bruteforcer.stable_matching_list:
            return False
        return True

    def run(self):
        raise NotImplementedError("No method for processing instances")

    def show_results(self):
        raise NotImplementedError("No method for outputing the results")
