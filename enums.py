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

class AdditionScores(Enum):
    RELEVANT_THEME = 0.25
    RELEVANT_WORD = 0.1
    IS_ARTICLE = 0.05