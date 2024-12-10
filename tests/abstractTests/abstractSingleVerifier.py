from tests.abstractTests.abstractVerifier import AbstractVerifier

class AbstractSingleVerifier(AbstractVerifier):
    def __init__(self):
        self._correct_count = 0
        self._incorrect_count = 0

    def run(self):
        self.generate_instance()
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