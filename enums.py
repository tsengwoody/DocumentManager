from enum import Enum
class ImageIdEnum:
    DOCUMENT = 0
    SECTION  = 1
    TEXT     = 2
    MATHML   = 3
    BACKPATH = 4
    FORWARD  = 5
    BACKWARD = 6

    @staticmethod
    def typeToEnum(_type):
        if _type == "section":
            return ImageIdEnum.SECTION
        elif _type == "text":
            return ImageIdEnum.TEXT
        elif _type == "mathml":
            return ImageIdEnum.MATHML

class InputType(Enum):
    TREE = 1
    PANEL = 2
    ITEM = 4


class PanelType(Enum):
    SECTION = "section"
    TEXT = "text"
    MATH = "mathml"

class ActionType(Enum):
    DEL = "del"
    ADD = "add"
    UPDATE = "update"
    COUNTING = "update_count"
    NONE = "none"