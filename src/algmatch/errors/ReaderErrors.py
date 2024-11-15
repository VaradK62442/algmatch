"""
A set of custom errors to make checks during reading of instances cleaner
"""

# Ideally this error should never be called directly
class ReaderError(Exception):
    def __init__(self, participant_type, name, cause, line=False):
        if line:
            source = f"line {name}"
        else:
            source = f"{participant_type} {name}"
        super().__init__(f"\nSource: {source}\nCause: {cause}")

class ParticipantQuantityError(Exception):
    def __init__(self):
        super().__init__("\nSource: line 0\nCause: participant quantities misformatted")

class IDMisformatError(ReaderError):
    def __init__(self, participant_type, name, line=False):
        cause = f"{participant_type} ID misformatted"
        super().__init__(participant_type, name, cause, line)

class CapacityError(ReaderError):
    def __init__(self, participant_type, name, line=False):
        cause = f"{participant_type} capacity is not int"
        super().__init__(participant_type, name, cause, line)

class RepeatIDError(ReaderError):
    def __init__(self, participant_type, name, line=False):
        cause = f"Repeated {participant_type} ID"
        super().__init__(participant_type, name, cause, line)

class PrefListMisformatError(ReaderError):
    def __init__(self, participant_type, name, offender, line=False):
        cause = f"{participant_type} preference list misformatted; {offender} is not int"
        super().__init__(participant_type, name, cause, line)

class OffererError(ReaderError):
    def __init__(self, participant_type, offerer_type, name, line=False):
        cause = f"{participant_type} offerer misformatted; {offerer_type} is not int"
        super().__init__(participant_type, name, cause, line)
