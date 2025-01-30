from matchers.xpath import xpathMatcher
from matchers.comment import commentMatcher
from matchers.javascriptVar import javascriptVarMatcher
from matchers.header import headerMatcher
from matchers.queryParameter import queryParameterMatcher
from matchers.bodyPattern import bodyPatternMatcher
from matchers.configParser import configParserMatcher



## TO REMOVE
matcher_list = {
    'Xpath': xpathMatcher,
    'JavascriptVar': javascriptVarMatcher,
    'HeaderPattern': headerMatcher,
    'QueryParameter': queryParameterMatcher,
    'Comment':commentMatcher,
    'BodyPattern': bodyPatternMatcher,
    'ConfigParser': configParserMatcher
}

## Keep only this one

named_matcher_list = {
    'Comment': commentMatcher,
    #'ConfigParser':,
    'HeaderPattern': headerMatcher,
    'JavascriptVar': javascriptVarMatcher,
    'QueryParameter':queryParameterMatcher,
    'Readme': bodyPatternMatcher,
    'Xpath': xpathMatcher
}

active_finders = ['Readme']

#named_matcher_list = {
#    "AnalyticsComment" : commentMatcher,
#    "BodyTag" : xpathMatcher,
#    "ChangeLog" : bodyPatternMatcher,
#    "Changelog" : bodyPatternMatcher,
#    "Comment" : commentMatcher,
#    "CommentDebugInfo" : commentMatcher,
#    "CommentInJavascript" : xpathMatcher,
#    "ComposerFile" : configParserMatcher,
#    "ConfigComment" : bodyPatternMatcher,
#    "ConfigFile" : configParserMatcher,
#    "ConfigParser" : configParserMatcher,
#    "ConstantFile" : configParserMatcher,
#    "CssFile" : bodyPatternMatcher,
#    "DependenciesFile" : configParserMatcher,
#    "DisabledComment" : commentMatcher,
#    "DivDataVersion" : xpathMatcher,
#    "DocumentationFile" : bodyPatternMatcher,
#    "ExplorerIE8Comment" : commentMatcher,
#    "GlueFile" : configParserMatcher,
#    "GraphMetaTagsComment" : commentMatcher,
#    "HeaderPattern" : headerMatcher,
#    "HiddenInput" : ,
#    "HistoryLog" : ,
#    "Ie6Comment" : ,
#    "Ie7Comment" : ,
#    "InlineJavascriptVar" : ,
#    "InvalidTrackerComment" : ,
#    "JavascriptComment" : ,
#    "JavascriptFile" : ,
#    "JavascriptVar" : ,
#    "JavascriptVarFromEnhancedEcommerce" : ,
#    "LanguageTranslationFile" : ,
#    "LinkInHomepage" : ,
#    "LocaleTranslationFile" : ,
#    "MetaGenerator" : ,
#    "MetaTag" : ,
#    "MonsterInsightsComment" : ,
#    "OldComment" : ,
#    "QueryParameter" : ,
#    "Readme" : ,
#    "ReleaseLog" : ,
#    "ScriptComment" : ,
#    "SpanTag" : ,
#    "StyleBackgroundUrl" : ,
#    "StyleComment" : ,
#    "StyleVar" : ,
#    "TranslationFile" : ,
#    "TranslationFile2" : ,
#    "TranslationFile3" : ,
#    "TwitterCardComment" : ,
#    "UrlInHomePage" : ,
#    "VersionFile" : ,
#    "VersionInFilename" : ,
#    "VersionLog" : ,
#    "WikiIE8Comment" : ,
#    "Xpath" : ,
#    "YoastComment" : 
#}