from lxml import etree
from matchers.matcher import Matcher
import json

class configParserMatcher(Matcher):
    
    parameters = ['path', 'key']
    
    def __init__(self, name=None, **kwargs):
        if all(k in kwargs for k in self.parameters) == False:
            ## TODO error management
            #print('Key error')
            ...
        super().__init__(name=name, **kwargs)
    
    async def matcher_logic(self, response):
        to_return = json.loads(self.content)
        if self.key in to_return:
            return [to_return[self.key]]
        return False