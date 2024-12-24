from matchers.matcher import Matcher
import httpx
import regex

class Finder():
    # TODO set regex type
    def __init__(self, matcher: Matcher, regex = regex.Pattern, path: str = '/'):
        self.matcher = matcher
        self.regex = regex
        self.path = path
    
    def match(self, url: str, requested_dict = dict[str, str]):
        if not self.path in requested_dict:
            response = httpx.get(f"{url}{self.path}")
            # TODO error management
            requested_dict[self.path] = response.text
        matcher_found = self.matcher.get(requested_dict[self.path])
        print(matcher_found)
        if len(matcher_found) == 0:
            return False
        for match in matcher_found:
            if self.regex.findall(match):
                return True
        return False