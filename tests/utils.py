import os
import jsonpickle


def load_dd_obj(filename):
    current_dir = os.path.abspath(os.path.split(__file__)[0])
    full_filename = os.path.join(current_dir, 'fixtures', filename)
    with open(full_filename, 'r') as dd_file:
        dd_obj = jsonpickle.loads(dd_file.read())
    return dd_obj
