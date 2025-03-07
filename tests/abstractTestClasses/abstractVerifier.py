class AbstractVerifier:
    def __init__(self, problem, sides, gen, gen_args, brute_force):
        self.Problem = problem
        self.sides = sides
        self.BruteForce = brute_force
        self.gen = gen(*gen_args)
        self.current_instance = {}

    def generate_instance(self):
        self.current_instance = self.gen.generate_instance()

    def verify_instance(self):
        # optimal and pessimal from man/resident/student side

        bruteforcer = self.BruteForce(dictionary=self.current_instance)
        optimal_solver = self.Problem(
            dictionary=self.current_instance, optimised_side=self.sides[0]
        )
        pessimal_solver = self.Problem(
            dictionary=self.current_instance, optimised_side=self.sides[1]
        )

        bruteforcer.find_minmax_matchings()
        m_0 = optimal_solver.get_stable_matching()
        m_z = pessimal_solver.get_stable_matching()

        if m_z != bruteforcer.stable_matching_list[-1]:
            return False
        if m_0 != bruteforcer.stable_matching_list[0]:
            return False
        return True

    def run(self):
        raise NotImplementedError("No method for processing instances")

    def show_results(self):
        raise NotImplementedError("No method for outputing the results")
