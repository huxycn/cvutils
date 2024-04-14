import csv

from collections import OrderedDict

from .base import BaseFileHandler


def to_number(s):
    try:
        if s.isdigit():
            return int(s)
        else:
            return float(s)
    except ValueError:
        pass
    return s
 

def set_default(obj):
    pass


class CsvHandler(BaseFileHandler):

    def load_from_fileobj(self, file, **kwargs):
        if 'delimiter' not in kwargs:
            kwargs['delimiter'] = ' '
        headers = kwargs.pop('headers', False)
        if headers:
            return [OrderedDict({k: to_number(v) for k, v in d.items()}) for d in csv.DictReader(file, **kwargs)]
        else:
            return [[to_number(s) for s in row] for row in csv.reader(file, **kwargs)]
    
    def dump_to_fileobj(self, obj, file):
        csv.writer(file).writerows(obj)

    def dump_to_str(self, obj):
        return '\n'.join(obj)
