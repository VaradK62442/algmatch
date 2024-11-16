"""
Class to represent a preference entity.
e.g. in a student's preference list, a project is an entity.
"""

class EntityPreferenceInstance:
    def __init__(self, values: str | tuple[str]) -> None:
        """
        Initialises an EntityPreferenceInstance object.

        :param values: The values of the entity. If entity is a tied preference, this is a list of strings.
        """ 
        if isinstance(values, tuple):
            self.values = tuple(EntityPreferenceInstance(v) for v in values)
        else:
            self.values = values
        self.isTie = isinstance(values, tuple)

    def __str__(self) -> str:
        return f"{self.values}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if isinstance(other, EntityPreferenceInstance):
            return self.values == other.values
        
        elif isinstance(other, str) or isinstance(other, tuple):
            return self.values == other
        
        return False
    
    def __ne__(self, other) -> bool:
        return not self == other
    
    def __hash__(self) -> int:
        return hash(self.values)

    def __contains__(self, item) -> bool:
        return item in self.values