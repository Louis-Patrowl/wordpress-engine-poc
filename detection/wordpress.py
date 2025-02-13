import httpx
from lxml import etree
from matchers.xpath import xpathMatcher
from matchers.comment import commentMatcher
import regex

# TODO check oembed ?
WP_DETECT_FINDERS = [
    xpathMatcher(version=True,
        xpath='//link/@href|//script/@src',
        pattern=regex.compile('(?:(?:wp-content\/(?:themes|(?:mu-)?plugins|uploads))|wp-includes|wp-json\/oembed)',regex.IGNORECASE)
    ),
    xpathMatcher(version=True,
        xpath='//meta[@name="generator"]/@content',
        pattern=regex.compile("wordpress", regex.IGNORECASE)
    ),
    commentMatcher(version=True,
        pattern=regex.compile('wordpress', regex.IGNORECASE)
    ),
    xpathMatcher(version=True,
        xpath='//script[not(@src)]',
        pattern=regex.compile('\/wp-admin\/admin-ajax\.php', regex.IGNORECASE)
    )
]

async def detect_wordpress(args: dict) :#), cached_webpage: dict) -> bool:
    for finder in WP_DETECT_FINDERS:
        print(finder)
        if (await finder.match(args.URL)):
            return True
    if args.mode == 'passive':
        return False
    for finder in WP_DETECT_FINDERS:
        if (finder.match(args.URL, path='ThisPageDoesntExistPatrowl', status=[404])):
            return True
    return False