from cn_rest.utils import Choices


class DoubtStateChoices(Choices):
    DRAFT = 1
    IN_PROCESS = 2
    ESCALATED = 3
    SOLVED = 4
