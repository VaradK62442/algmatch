"""
A set of custom errors to make checks during pre-processing of intances cleaner
"""

# Ideally this error should never be called directly
class InstanceSetupError(Exception):
    def __init__(self, participant_type, name, cause):
        source = f"{participant_type} {name}"
        super().__init__(f"\nSource: {source}\nCause: {cause}")

class PrefRepError(InstanceSetupError):
    def __init__(self, participant_type, name):
        cause = "repetition in preference list."
        super().__init__(participant_type, name, cause)

class PrefNotFoundError(InstanceSetupError):
    def __init__(self, participant_type, name, offender):
        cause = f"{offender} not instantiated."
        super().__init__(participant_type, name, cause)