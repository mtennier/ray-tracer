class FileSections:
    # Constants for reading the file.
    SECTION = 0 
    # Regex for extracting important parts of the file
    SECTION_REGEX = '[a-zA-z]+'
    NAME_REGEX = '[a-zA-z0-9_]+'
    INT_REGEX = '-?[0-9]+'
    NUM_REGEX = '-?[0-9]*[.]*[0-9]+'
    # Different sections of the file.
    NEAR = 'NEAR'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    BOTTOM = 'BOTTOM'
    TOP = 'TOP'
    RES = 'RES'
    SPHERE = 'SPHERE'
    LIGHT = 'LIGHT'
    BACK = 'BACK'
    AMBIENT = 'AMBIENT'
    OUTPUT = 'OUTPUT'


class RayConstants:
    # Constants for the Ray Tracing class
    MAX_DEPTH = 3
    COLS = 0
    ROWS = 1

class ColorConstants:
    # Constants for writing colors to file.
    MAX_COLOR_VAL = 255

class NumberConstants:
    # Constants for numerical error.
    ZERO_OFFSET = 0.0001
    RAY_START_OFFSET = 0.000001