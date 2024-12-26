from lxml import etree
from matchers.matcher import Matcher
import json

class configParserMatcher(Matcher):
    
    parameters = ['path', 'key']
    
    def __init__(self, **kwargs):
        if all(k in kwargs for k in self.parameters) == False:
            ## TODO error management
            print('Key error')
            ...
        self.path = kwargs['path']
        self.key = kwargs['key']
    
    def get(self, request) -> list[str]:
        json_object =json.load(request.text)
        # TODO error management
        return json_object[self.key]