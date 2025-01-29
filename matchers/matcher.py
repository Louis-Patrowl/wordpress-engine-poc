import regex
from test_time import testtime
import functools
from async_lru import alru_cache
import aiohttp

REGEX_ALL = regex.compile('.*')

class Matcher():

    @staticmethod
    @alru_cache()
    async def cached_get_request(url):
        async with aiohttp.ClientSession() as client:
            resp = await client.get(url)
            return resp, await resp.text()

    @staticmethod
    @alru_cache()
    async def cached_head_request(url):
        async with aiohttp.ClientSession() as client:
            resp = await client.head(url)
            return resp
    #@functools.cache
    #def cached_get_request(url):
    #    return httpx.get(url)
    #
    #@functools.cache
    #def cached_head_request(url):
    #    return httpx.head(url)


    # TODO set regex type
    def __init__(self, name=None, **kwargs):
        self.path  =  kwargs.get('path', '')
        self.pattern =  kwargs.get('pattern', REGEX_ALL)
        self.status_code  =  kwargs.get('status', [200])
        self.name = name
        self.detected = False
        self.version = None
        self.content = ""
        self.check_version = kwargs.get('version', False)


    async def request(self, url: str, path: str = None, status: int = None):
        if (self.path):
            to_request_path = (path or '') + self.path
        else:
            to_request_path = ''
        head = await Matcher.cached_head_request(f"{url}{to_request_path}")
        if self.status(head, status) == False:
            return head, ""
        response, content = await Matcher.cached_get_request(f"{url}{to_request_path}")
        return response, content

    def status(self, response, status: int = None) -> bool:
        if response.status not in (status or self.status_code):
            return False
        return True

    async def matcher_logic():
        pass

    async def match(self, url: str, path: str = None, status: int = None) -> bool:
        #tmptime = testtime("request")
        response, self.content = await self.request(url, path, status)
        #tmptime.end()
        if self.status(response, status) == False:
            return False

        matcher_found = await self.matcher_logic(response)
        if len(matcher_found) == 0:
            return False
        for match in matcher_found:
            if not match:
                continue
            matched = self.pattern.findall(match)
            if matched:
                if self.check_version:
                    self.version = matched[0]
                self.detected = True
                return True
        return False
    
