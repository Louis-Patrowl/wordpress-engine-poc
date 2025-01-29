from lxml import etree
from matchers.matcher import Matcher
import regex 

class queryParameterMatcher(Matcher):
    
    parameters = ['files']
    
    def __init__(self, name=None, **kwargs):
        if all(k in kwargs for k in self.parameters) == False:
            ## TODO error management
            print('Key error')
            ...
        kwargs['pattern'] = regex.compile('\?ver=(?P<v>\d+\.[\.\d]+)')
        self.files = kwargs['files']
        if 'xpath' in kwargs:
            self.xpath = kwargs['xpath']
        else:
            self.xpath = '//link[@href]/@href|//script[@src]/@src'
        super().__init__(name=name, **kwargs)
    
    async def matcher_logic(self, response) -> list[str]:
        tree = etree.fromstring(self.content, etree.HTMLParser())
        to_return = []
        # TODO manage script[src]
        xpath_match = tree.xpath(self.xpath)
        for i in xpath_match:
            for j in self.files:
                #print(i, j)
                if f"{self.name or ''}" in i and j in i:
                    #print(f"{self.name or ''}/{j}", i)
                    to_return.append(i)
        #print(to_return)
        return to_return