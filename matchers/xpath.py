from lxml import etree
from matchers.matcher import Matcher

class xpathMatcher(Matcher):
    
    parameters = ['xpath']
    
    def __init__(self, **kwargs):
        if all(k in kwargs for k in self.parameters) == False:
            ## TODO error management
            print('Key error')
            ...
        self.xpath = kwargs['xpath']
        super().__init__(**kwargs)
    
    def matcher_logic(self, response) -> list[str]:
         tree = etree.fromstring(response.text, etree.HTMLParser())
         
         # TODO manage script[src]
         return tree.xpath(self.xpath)