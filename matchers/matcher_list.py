from matchers.xpath import xpathMatcher
from matchers.comment import commentMatcher
from matchers.javascriptVar import javascriptVarMatcher
from matchers.header import headerMatcher
from matchers.queryParameter import queryParameterMatcher
from matchers.bodyPattern import bodyPatternMatcher


matcher_list = {
    'Xpath': xpathMatcher,
    'JavascriptVar': javascriptVarMatcher,
    'HeaderPattern': headerMatcher,
    'QueryParameter': queryParameterMatcher,
    'Comment':commentMatcher,
    'BodyPattern': bodyPatternMatcher
}

named_matcher_list = {
    'Comment': commentMatcher,
    #'ConfigParser':,
    'HeaderPattern': headerMatcher,
    'JavascriptVar': javascriptVarMatcher,
    'QueryParameter':queryParameterMatcher,
    'Readme': bodyPatternMatcher,
    'Xpath': xpathMatcher
}