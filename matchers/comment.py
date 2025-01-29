from lxml import etree
from matchers.xpath import xpathMatcher

class commentMatcher(xpathMatcher):
    def __init__(self, name=None, **kwargs):
        if not 'xpath' in kwargs:
            kwargs['xpath'] = '//comment()'
        #print(kwargs)
        super().__init__(name=name, **kwargs)

    async def matcher_logic(self, response):
        to_return = await super().matcher_logic(response)
        return [x.text.strip() for x in to_return]