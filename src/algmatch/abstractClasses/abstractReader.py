"""
Abstract class to handle reading in data for difference matching algorithms.
"""

class AbstractReader:
    def __init__(self, data: dict | str) -> None:
        self.data = data

    def _read_data(self) -> None:
        """
        Sets appropriate values for the preference instance based on the data read in.
        """
        raise NotImplementedError("Method not implemented")
    
class FileError(Exception):
    def __init__(self, source, cause):
        super().__init__(f"\nSource: {source}\nCause: {cause}")
