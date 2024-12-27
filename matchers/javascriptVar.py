from lxml import etree
from matchers.matcher import Matcher
import json

class javascriptVarMatcher(Matcher):
    
    def __init__(self, **kwargs):
        self.version_key = kwargs.get('version_key', None)
        self.xpath = kwargs.get('xpath', None)
        super().__init__(**kwargs)
    
    def xpath_matcher(self, response):
        to_return = []
        tree = etree.fromstring(response.text, etree.HTMLParser())
         
         # TODO manage script[src]
        matched_xpath = tree.xpath(self.xpath)
        if matched_xpath:
            to_return = [x.text for x in matched_xpath]
        #    print(to_return[0])
        return to_return

    def config_matcher():
        ...

    def matcher_logic(self, response):
        if self.xpath:
            return self.xpath_matcher(response)