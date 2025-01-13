from lxml import etree
from matchers.matcher import Matcher
import httpx
import regex

class bodyPatternMatcher(Matcher):
    def __init__(self, **kwargs):
        if type(kwargs['path']) == str:
            kwargs['path'] = [kwargs['path']]
        if 'readme.txt' in kwargs['path']:
            kwargs['pattern'] = regex.compile('\\b(?:stable tag|version):\\s*(?!trunk)([0-9a-z.-]+)|^=+\s+(?:v(?:ersion)?\\s*)?([0-9.-]+)[^=]*=+$', regex.IGNORECASE)
        super().__init__(**kwargs)

    def matcher_logic(self, response):
        return [response.text]

    def request(self, url: str, requested_dict: dict[str, str], path: str = None, status: int = None) -> httpx.Response:
        if not path in requested_dict:
            #print(f"{url}{to_request_path}")
            
            head = httpx.head(f"{url}{path}")
            if self.status(head, status) == False:
                return head
            response = httpx.get(f"{url}{path}")
            # TODO error management
            requested_dict[path] = response
        else:
            response = requested_dict[path]
        return response

    def match(self, url: str, requested_dict: dict[str, str], path: str = None, status: int = None) -> bool:
        for i in self.path:
            response = self.request(url, requested_dict, f"{path}/{i}")
            if self.status(response, status) == True:
                self.detected = True
                matched = self.pattern.findall(response.text)
                print(self.pattern)
                print(matched)
                if matched:
                    if type(matched[0]) == tuple:
                        self.matched = matched[0][0]
                    else:
                        self.matched = matched[0]
                return True
        return False