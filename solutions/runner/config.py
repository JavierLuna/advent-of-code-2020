import os

INPUTS_FOLDER = os.getenv("INPUTS_FOLDER")

if not INPUTS_FOLDER:
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    INPUTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(dir_path)), "inputs")