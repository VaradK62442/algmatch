class AbstractInstanceGenerator:
    def generate_instance_no_ties():
        """
        Generates an instance of a particular problem WITHOUT ties in preference lists.
        """
        raise NotImplementedError("Method not implemented")

    def generate_instance_with_ties():
        """
        Generates an instance of a particular problem WITH ties in preference lists.
        """
        raise NotImplementedError("Method not implemented")