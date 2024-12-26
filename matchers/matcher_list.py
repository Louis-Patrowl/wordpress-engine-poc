from matchers.xpath import xpathMatcher
from matchers.comment import commentMatcher
from matchers.javascriptVar import javascriptVarMatcher
from matchers.header import headerMatcher
from matchers.queryParameter import queryParameterMatcher



matcher_list = {
    'Xpath': xpathMatcher,
    'JavascriptVar': javascriptVarMatcher,
    'HeaderPattern': headerMatcher,
    'QueryParameter': queryParameterMatcher,
    'Comment':commentMatcher
}
