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
    NONE = 0.11
    RELEVANT_THEME = 1
    RELEVANT_WORD = 0.3
    IS_ARTICLE = 0.05

    TRIGGER = 0.2
    TRIGGER_NOT = 0.4
    TARGET = 0.5
    DESTINATION = 0.6
    # TARGET_FOR = 0.0
    # TARGET_FROM = 0.0
    # TARGET_BY = 0.0
    THEME = 0.7
    SOURCE = 0.71
    INCLUDE = 0.72
    SKIP = 0.73

class GraphTypes(Enum):
    QUERY = 1
    DATA = 2
    SIMILARITY = 3
