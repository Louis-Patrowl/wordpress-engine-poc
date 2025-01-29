from lxml import etree
from matchers.matcher import Matcher
import httpx

class headerMatcher(Matcher):
    
    parameters = ['header']
    
    def __init__(self, name=None, **kwargs):
        if all(k in kwargs for k in self.parameters) == False:
            ## TODO error management
            print('Key error')
            ...
        self.header = kwargs['header']
        super().__init__(name=name, **kwargs)
    
    async def matcher_logic(self, response: httpx.Response) -> list[str]:
        to_return = []
        if self.header in response.headers:
            to_return = [response.headers[self.header]]
        return to_return