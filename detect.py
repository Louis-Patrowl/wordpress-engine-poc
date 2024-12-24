import httpx
from lxml import etree
from matchers.finder import Finder
from matchers.xpath import xpathMatcher
import regex

# TODO check oembed ?
WP_DETECT_FINDERS = [
    Finder(
        xpathMatcher('//link/@href|//script/@src'), 
        regex.compile('(?:(?:wp-content\/(?:themes|(?:mu-)?plugins|uploads))|wp-includes|wp-json\/oembed)',regex.IGNORECASE)
    ),
    Finder(
        xpathMatcher('//meta[@name="generator"]/@content'),
        regex.compile("wordpress", regex.IGNORECASE)
    
    ),

]

def is_wordpress_passive(url: str) -> bool:
    httpx.get(url, )

def is_wordpress_aggressive():
    ...

def detect_wordpress(args: dict) :#), cached_webpage: dict) -> bool:
    print(WP_DETECT_FINDERS[1].match(args.URL, {}))
    #for finder in WP_DETECT_FINDERS:
    #    if (finder.match(args.URL, {})):
    #        return True
    return False



    #if args.mode == 'passive':
    #    return is_wp