from lxml import etree
from matchers.matcher import Matcher

class xpathMatcher(Matcher):
    def __init__(self, xpath_string: str):
        self.xpath_string = xpath_string
    
    def get(self, content: str) -> list[str]:
         tree = etree.fromstring(content, etree.HTMLParser())
         return tree.xpath(self.xpath_string)