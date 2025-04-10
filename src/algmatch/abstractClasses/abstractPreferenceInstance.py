"""
Abstract class to store preference lists for both sides in a type of matching problem.
"""

from itertools import product
import os

from algmatch.errors.InstanceSetupErrors import PrefRepError, PrefNotFoundError


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

    def clean_unacceptable_pairs(self, a_side, b_side) -> None:
        """
        Provides a general function for pair cleaning between two sides.
        May be overridden or extended by subclasses if necessary.

        :param a_side: dictionary with information for e.g. men, residents
        :param b_side: dictionary with information for e.g. women, hospitals
        """
        for a, b in product(a_side, b_side):
            a_in_b_list = a in b_side[b]["list"]
            b_in_a_list = b in a_side[a]["list"]

            if not a_in_b_list or not b_in_a_list:
                if b_in_a_list:
                    a_side[a]["list"].remove(b)
                if a_in_b_list:
                    b_side[b]["list"].remove(a)

    def set_up_rankings(self) -> None:
        raise NotImplementedError("Method not implemented")

    def check_preferences_single_group(self, group, name_singular, targets) -> None:
        """
        Utility. Checks that each list contains only valid targets without repetition.

        :param group:  set of entities (e.g. men, projects, lecturers)
        :param name_singular: singular of group name
        :param targets: group of valid targets of preference
        :raises PrefRepError: target duplication
        :raises PrefNotFoundError: target is not is not of the right kind
        """
        for g, prefs in group.items():
            if len(set(prefs["list"])) != len(prefs["list"]):
                raise PrefRepError(name_singular, g)

            for t in prefs["list"]:
                if t not in targets:
                    raise PrefNotFoundError(name_singular, g, t)

    def tieless_lists_to_rank(self, group) -> None:
        """
        Utility. Takes a group with clean lists and constructs their rank dictionaries.

        :param group: set of entities (e.g. men, projects, lecturers)
        """
        for prefs in group.values():
            prefs["rank"] = {target: idx for idx, target in enumerate(prefs["list"])}
