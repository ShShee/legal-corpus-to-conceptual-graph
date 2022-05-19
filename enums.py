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
    NONE = 0
    RELEVANT_THEME = 1
    RELEVANT_WORD = 2
    IS_ARTICLE = 3

    UNDEFINED = 4
    TRIGGER = 5
    TRIGGER_NOT = 6

    TARGET_EVENT = 7
    TARGET_ACTION = 8
    INTENT = 9

    THEME_EVENT = 10
    THEME_ACTION = 11
    SITUATION = 12


def additionScoring(type):
    return {
        AdditionScores.RELEVANT_THEME: 1,
        AdditionScores.RELEVANT_WORD: 0.3,
        AdditionScores.IS_ARTICLE: 0.05,
        AdditionScores.UNDEFINED: 0.0,
        AdditionScores.TRIGGER: 0.25,
        AdditionScores.TRIGGER_NOT: 0.25,
        AdditionScores.TARGET_EVENT: 0.75,
        AdditionScores.TARGET_ACTION: 0.5,
        AdditionScores.INTENT: 0.75,
        AdditionScores.THEME_ACTION: -0.5,
        AdditionScores.THEME_EVENT: -0.75,
        AdditionScores.SITUATION: -0.75
    }.get(type, 0.0)


class GraphTypes(Enum):
    QUERY = 1
    DATA = 2
    SIMILARITY = 3
