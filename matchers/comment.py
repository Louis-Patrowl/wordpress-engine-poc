from lxml import etree
from matchers.xpath import xpathMatcher

class commentMatcher(xpathMatcher):
    def __init__(self, **kwargs):
        if not 'xpath' in kwargs:
            kwargs['xpath'] = '//comment()'
        super().__init__(**kwargs)