from lxml import etree
from matchers.matcher import Matcher

class xpathMatcherMulti(Matcher):
    
    parameters = ['xpath']
    
    def __init__(self, **kwargs):
        if all(k in kwargs for k in self.parameters) == False:
            ## TODO error management
            print('Key error')
            ...
        self.xpath = kwargs['xpath']
        super().__init__(**kwargs)
    
    async def matcher_logic(self, response) -> list[str]:
         tree = etree.fromstring(self.content, etree.HTMLParser())
         # TODO manage script[src]
         return tree.xpath(self.xpath)
    
    async def match(self, url: str, path: str = None, status: int = None) -> bool:
            #tmptime = testtime("request")
            response, self.content = await self.request(url, path, status)
            #tmptime.end()
            if self.status(response, status) == False:
                return False
            matcher_found = await self.matcher_logic(response)
            if len(matcher_found) == 0:
                return False
            self.version = []
            for match in matcher_found:
                matched = self.pattern.findall(match)
                if matched and matched[0] not in self.version:
                     self.version.append(matched[0])
            if len(self.version) == 0:
                self.detected = False
            else:
                self.detected = True
            return self.detected

