from matchers.xpath import xpathMatcher
from matchers.comment import commentMatcher
from matchers.javascriptVar import javascriptVarMatcher
from matchers.header import headerMatcher

matcher_list = {
    'Xpath': xpathMatcher,
    'JavascriptVar': javascriptVarMatcher,
    'HeaderPattern': headerMatcher
}
