from lxml import etree
from matchers.matcher import Matcher
import json
import regex

class javascriptVarMatcher(Matcher):
    
    def __init__(self, **kwargs):
        print(kwargs)
        self.version_key = kwargs.get('version_key', None)
        self.xpath = kwargs.get('xpath', '//script[not(@src)]')
        if self.version_key:
            self.pattern_config = kwargs['pattern']
            kwargs['pattern'] = regex.compile('.*')
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

    def config_matcher(self,response):
        to_return = []
        variable = self.pattern_config.findall(response.text)
        if variable:
            json_variable = json.loads('{' + variable[0] + '}')
            if self.version_key in json_variable:
                to_return = [json_variable[self.version_key]]
        return to_return

    def matcher_logic(self, response):
        if self.version_key == None:
            return self.xpath_matcher(response)
        else:
            return self.config_matcher(response)