"""
Abstract class to store preference lists for both sides in matching problems that have ties in the preference lists.
"""

from algmatch.abstractClasses.abstractPreferenceInstance import (
    AbstractPreferenceInstance,
)


class AbstractPreferenceInstanceWithTies(AbstractPreferenceInstance):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(filename, dictionary)

    def any_repetitions(self, prefs):
        seen_count = 0
        seen_set = set()
        for tie in prefs:
            seen_count += len(tie)
            seen_set |= tie
        if len(seen_set) != seen_count:
            return True
        return False
