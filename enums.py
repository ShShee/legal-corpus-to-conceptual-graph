from enum import Enum

class VariableTypes(Enum):
    ONLY_VERBS = 1
    ONLY_NOUNS = 2
    BOTH = 3


class DataPathTypes(Enum):
    LAWS = 1
    ARTICLES = 2
    RULES = 3
    LOOKUPS = 4