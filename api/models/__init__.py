""" Default import all .py files in current directory """
from glob import iglob
from re import search

__all__ = []

""" Find all DB model modules and their paths """
for path in iglob('./**/*.py', recursive=True):
    model_pattern = '.*/models/\w+\.py'
    if search(model_pattern, path) is not None:
        """ Get model modules """
        FILE_INDEX = -1 # Files are the last part of a path
        module = path.split('/')[FILE_INDEX].rstrip('.py')
        if module != '__init__':
            __all__.append(module)
