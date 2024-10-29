"""
Abstract class to handle reading in preference lists in dictionaries for different matching algorithms.
"""

class AbstractDictionaryReader:
    def __init__(self, dictionary: dict) -> None:
        self.dictionary = dictionary

    def _read_dictionary(self) -> None:
        """
        Sets appropriate values for the preference instance based on the dictionary read in.
        """
        raise NotImplementedError("Method not implemented")