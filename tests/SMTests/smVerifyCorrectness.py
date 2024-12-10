from time import perf_counter_ns
from tqdm import tqdm

from tests.abstractTests.abstractSingleVerifier import AbstractSingleVerifier as ASV
from tests.SMTests.smAbstractVerifier import SMAbstractVerifier as SMAV

class VerifyCorrectness(SMAV, ASV):
    def __init__(self, total_men, total_women,
                 lower_bound, upper_bound):
        
        SMAV.__init__(self, total_men, total_women,
                      lower_bound, upper_bound)
        ASV.__init__(self)

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