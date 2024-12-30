from lxml import etree
from matchers.matcher import Matcher
import httpx

class bodyPatternMatcher(Matcher):
    def __init__(self, **kwargs):
        if type(kwargs['path']) == str:
            kwargs['path'] = [kwargs['path']]
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
                print(f'Found {path}/{i}')
                return True
        return False