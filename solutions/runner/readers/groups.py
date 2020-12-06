from solutions.runner.readers.base_reader import BaseGroupReader


class ListGroupReader(BaseGroupReader):
    pass


class DictionaryGroupReader(BaseGroupReader):
    __group_metadata__ = dict, dict.update
