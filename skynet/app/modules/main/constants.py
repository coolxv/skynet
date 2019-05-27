#coding: utf-8


#display
RULE_TYPE = {
    "sub": u'子字符串',
    "subneg": u'子字符串',
    "reg": u'正则表达式',
    "regneg": u'正则表达式',
}

RULE_ACTIVE = {
    0: u'未下发',
    1: u'已下发',
}
RULE_AUTO = {
    0: u'否',
    1: u'是',
}
RULE_DESCRIPTION = {
    "other": u'其他',
    "crawler": u'爬虫',
    "worm": u'蠕虫',
    "searcher": u'搜索引擎',
    "ad": u'广告',
}
#ACL number
ACL_USER_AGENT_REG_NEG = 10001
ACL_USER_AGENT_SUB = 10002
ACL_USER_AGENT_REG = 10003

ACL_REFERRER_REG_NEG = 10004
ACL_REFERRER_SUB = 10005
ACL_REFERRER_REG = 10006

ACL_URL_REG_NEG = 10007
ACL_URL_SUB = 10008
ACL_URL_REG = 10009
