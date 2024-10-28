"""
Abstract class to handle reading in preference lists in files for different matching algorithms.
"""

class AbstractFileReader:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def _read_file(self) -> None:
        """
        Sets appropriate values for the preference instance based on the file read in.
        """
        raise NotImplementedError("Method not implemented")