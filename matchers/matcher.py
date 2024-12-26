import httpx
import regex

REGEX_ALL = regex.compile('.*')

class Matcher():

    # TODO set regex type
    def __init__(self, **kwargs):
        self.basepath  =  kwargs.get('basepath', '/')
        self.path  =  kwargs.get('path', '')
        self.pattern =  kwargs.get('pattern', REGEX_ALL)
        self.status_code  =  kwargs.get('status', 200)
    
    def request(self, url: str, requested_dict: dict[str, str], path: str = None) -> httpx.Response:
        to_request_path = self.basepath + self.path + (path or '')
        if not to_request_path in requested_dict:
            print(f"{url}{to_request_path}")
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
        response = self.request(url, requested_dict, path)

        if self.status(response, status) == False:
            return False

        matcher_found = self.matcher_logic(response)
        if len(matcher_found) == 0:
            return False

        print(matcher_found)
        for match in matcher_found:
            matched = self.pattern.findall(match)
            print(self.pattern)
            print(matched)
            if matched:
                self.matched = matched[0]
                return True
        return False
    
