import httpx
from lxml import etree
from matchers.xpath import xpathMatcher
import regex

WP_PATH_FINDERS = [
    xpathMatcher(name=None, version=True,
        xpath='//link/@href|//script/@src|//img/@src',
        pattern=regex.compile('\/([\w\s\-\/]+?)?\/(?:themes|plugins|uploads|cache)?\/',regex.IGNORECASE)
    ),
]

async def detect_path(args: dict) :#), cached_webpage: dict) -> bool:
    for finder in WP_PATH_FINDERS:
        #print(finder)
        if (await finder.match(args.URL)):
            print(finder.version)
            return finder.version
    #print(finder.version)
    # TODO verify aggressive for path
    #if args.mode == 'aggressive':
    #    for finder in WP_DETECT_FINDERS:
    #        if (finder.match(args.URL, cached_request, path='ThisPageDoesntExistPatrowl', status=404)):
    #            return True
    return False