import json
from abc import ABC, abstractmethod, abstractstaticmethod
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml


class WriteFile(ABC):
    _file_extension = ''

    def __init__(self, file_name='result'):
        self.file_name = file_name

    @property
    def file_path(self):
        return self.file_name + '.' + self._file_extension

    @abstractmethod
    def write(self, data):
        pass


class WriteJSON(WriteFile):
    _file_extension = 'json'

    def write(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=3)


class WriteXML(WriteFile):
    _file_extension = 'xml'

    @staticmethod
    def dict_to_xml(data):
        parsed = parseString(dicttoxml(data, attr_type=False))
        return parsed.toprettyxml()

    def write(self, data):
        with open(self.file_path, "w") as file:
            file.write(self.dict_to_xml(data))
