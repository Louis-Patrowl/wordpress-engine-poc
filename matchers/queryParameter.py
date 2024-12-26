from lxml import etree
from matchers.matcher import Matcher
import regex 

class queryParameterMatcher(Matcher):
    
    parameters = ['files']
    
    def __init__(self, **kwargs):
        if all(k in kwargs for k in self.parameters) == False:
            ## TODO error management
            print('Key error')
            ...
        kwargs['pattern'] = regex.compile('\?ver=(?P<v>\d+\.[\.\d]+)')
        self.files = kwargs['files']
        self.xpath = '//link[@href]/@href|//script[@src]/@src'
        super().__init__(**kwargs)
    
    def matcher_logic(self, response) -> list[str]:
        tree = etree.fromstring(response.text, etree.HTMLParser())
        to_return = []
        # TODO manage script[src]
        xpath_match = tree.xpath(self.xpath)
        
        print(xpath_match)
        for i in xpath_match:
            for j in self.files:
                if j in i:
                    to_return.append(i)
        print(to_return)
        return to_return