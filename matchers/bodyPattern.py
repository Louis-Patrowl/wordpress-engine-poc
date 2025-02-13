from lxml import etree
from matchers.matcher import Matcher
import httpx
import regex
import asyncio

class bodyPatternMatcher(Matcher):
    def __init__(self,  **kwargs):
        if type(kwargs['path']) == str:
            kwargs['path'] = [kwargs['path']]
        if 'readme.txt' in kwargs['path']:
            kwargs['pattern'] = regex.compile('\\b(?:stable tag|version):\\s*(?!trunk)([0-9a-z.-]+)|^=+\s+(?:v(?:ersion)?\\s*)?([0-9.-]+)[^=]*=+$', regex.IGNORECASE)
        kwargs['status'] = [200, 403]
        super().__init__(**kwargs)

    async def matcher_logic(self, response):
        return [self.content]

    async def request(self, url: str, path: str = None, status: int = None) -> httpx.Response:
        head = await Matcher.cached_head_request(f"{url}{path}")
        if self.status(head, status) == False:
            return head, ""
        response, content = await Matcher.cached_get_request(f"{url}{path}")
        return response, content


    async def match(self, url: str, path: str = None, status: int = None) -> bool:
        for i in self.path:
            response,self.content = await self.request(url, f"{path}/{i}")
            if self.status(response, status) == True:
                self.detected = True
                matched = self.pattern.findall(self.content)
                #print(self.pattern)
                #print(matched)
                if matched:
                    if type(matched[0]) == tuple:
                        self.version = matched[0][0]
                    else:
                        self.version = matched[0]
        return self.detected