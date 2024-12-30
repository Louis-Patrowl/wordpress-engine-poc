import httpx
import regex

REGEX_ALL = regex.compile('.*')

class Matcher():

    # TODO set regex type
    def __init__(self, **kwargs):
        self.path  =  kwargs.get('path', '')
        self.pattern =  kwargs.get('pattern', REGEX_ALL)
        self.status_code  =  kwargs.get('status', 200)
    
    def request(self, url: str, requested_dict: dict[str, str], path: str = None, status: int = None) -> httpx.Response:
        if (self.path):
            to_request_path = (path or '') + self.path
        else:
            to_request_path = ''
        if not to_request_path in requested_dict:
            #print(f"{url}{to_request_path}")
            head = httpx.head(f"{url}{to_request_path}")
            if self.status(head, status) == False:
                return head
            response = httpx.get(f"{url}{to_request_path}")
            # TODO error management
            requested_dict[to_request_path] = response
        else:
            response = requested_dict[to_request_path]
        return response

    def status(self, response: httpx.Response, status: int = None) -> bool:
        if response.status_code != (status or self.status_code):
            return False
        return True

    def matcher_logic():
        pass

    def match(self, url: str, requested_dict: dict[str, str], path: str = None, status: int = None) -> bool:
        response = self.request(url, requested_dict, path, status)

        if self.status(response, status) == False:
            return False

        matcher_found = self.matcher_logic(response)
        if len(matcher_found) == 0:
            return False

        for match in matcher_found:
            matched = self.pattern.findall(match)
            if matched:
                self.matched = matched[0]
                return True
        return False
    
