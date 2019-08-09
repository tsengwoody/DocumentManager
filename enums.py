
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