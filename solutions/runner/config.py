import os

dir_path = os.path.dirname(os.path.realpath(__file__))

ROOT_FOLDER = os.path.dirname(os.path.dirname(dir_path))
INPUTS_FOLDER = os.path.join(ROOT_FOLDER, "inputs")
SOLUTIONS_FOLDER = os.path.join(ROOT_FOLDER, "solutions")