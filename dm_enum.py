from enum import Enum
 
class InputType(Enum):
    TREE = 1
    PANEL = 2
    ITEM = 4


class PanelType(Enum):
    SECTION = "section"
    TEXT = "text"
    MATH = "mathml"