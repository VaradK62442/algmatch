"""
Abstract class to store preference lists for both sides in a type of matching problem.
"""

import os


class AbstractPreferenceInstance:
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        assert filename is not None or dictionary is not None, (
            "Either filename or dictionary must be provided"
        )
        assert not (filename is not None and dictionary is not None), (
            "Only one of filename or dictionary must be provided"
        )

        if filename is not None:
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._load_from_file(filename)

        if dictionary is not None:
            self._load_from_dictionary(dictionary)

    def _general_setup_procedure(self):
        self.check_preference_lists()
        self.clean_unacceptable_pairs()
        self.set_up_rankings()

    def _load_from_file(self, filename: str) -> None:
        raise NotImplementedError("Method not implemented")

    def _load_from_dictionary(self, dictionary: dict) -> None:
        raise NotImplementedError("Method not implemented")

    def check_preference_lists(self) -> None:
        raise NotImplementedError("Method not implemented")

    def clean_unacceptable_pairs(self) -> None:
        raise NotImplementedError("Method not implemented")

    def set_up_rankings(self) -> None:
        raise NotImplementedError("Method not implemented")
