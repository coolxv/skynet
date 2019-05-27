#coding: utf-8
from datetime import datetime
from app import db
from app.modules.main import constants as CONST
from uuid import  uuid1


class Whitelist(db.Model):
    __tablename__ = 'whitelist_rule'
    id = db.Column(db.Integer, primary_key=True)
    #资源guid
    guid = db.Column(db.String(32),  unique=True,nullable=False)
    #规则
    rule = db.Column(db.UnicodeText, nullable=False)
    #规则匹配类型:Str or Reg
    type = db.Column(db.UnicodeText, nullable=False)
    #规则分类:user_agent or referrer or url
    category = db.Column(db.UnicodeText, nullable=False)
    #来源：
    source = db.Column(db.UnicodeText, nullable=True)
    #规则的描述
    description = db.Column(db.UnicodeText, nullable=True)
    #规则创建的时间
    ctime = db.Column(db.DateTime, nullable=False,default= datetime.now)


    def __init__(self, rule=None,category=None,type=None,source=None,description=None):
        self.rule = rule
        self.type = type
        self.category = category
        self.description = description
        self.source = source
        self.guid = uuid1().get_hex()



    def __repr__(self):
        return '<White rule %r>' % (self.rule)


class Blacklist(db.Model):
    __tablename__ = 'blacklist_rule'
    id = db.Column(db.Integer, primary_key=True)
    #资源guid
    guid = db.Column(db.String(32),  unique=True,nullable=False)
    #规则
    rule = db.Column(db.UnicodeText, nullable=False)
    #规则匹配类型:Str or Reg
    type = db.Column(db.UnicodeText, nullable=False)
    #规则分类:user_agent or referrer or url
    category = db.Column(db.UnicodeText, nullable=False)
    #来源：
    source = db.Column(db.UnicodeText, nullable=True)
    #规则的描述
    description = db.Column(db.UnicodeText, nullable=True)
    #规则创建的时间
    ctime = db.Column(db.DateTime, nullable=False,default= datetime.now)


    def __init__(self, rule=None,category=None,type=None,source=None,description=None):
        self.rule = rule
        self.type = type
        self.category = category
        self.description = description
        self.source = source
        self.guid = uuid1().get_hex()



    def __repr__(self):
        return '<Black rule %r>' % (self.rule)

class Patrollist(db.Model):
    __tablename__ = 'patrollist_rule'
    id = db.Column(db.Integer, primary_key=True)
    #资源guid
    guid = db.Column(db.String(32),  unique=True,nullable=False)
    #规则
    rule = db.Column(db.UnicodeText, nullable=False)
    #阈值
    threshold = db.Column(db.Integer, nullable=False)
    #规则匹配类型:Str or Reg
    type = db.Column(db.UnicodeText, nullable=False)
    #规则分类:user_agent or referrer or url
    category = db.Column(db.UnicodeText, nullable=False)
    #来源：
    source = db.Column(db.UnicodeText, nullable=True)
    #规则的描述
    description = db.Column(db.UnicodeText, nullable=True)
    #预警状态
    warning = db.Column(db.Boolean,nullable=False,default=False)
    #自动阻拦和手动阻拦
    auto = db.Column(db.Boolean,nullable=False,default=False)
    #下发状态
    active = db.Column(db.Boolean,nullable=False,default=False)
    #规则创建的时间
    ctime = db.Column(db.DateTime, nullable=False,default= datetime.now)
    #产生预警的时间
    wctime = db.Column(db.DateTime, nullable=True)
    #规则下发的时间
    actime = db.Column(db.DateTime, nullable=True)

    def __init__(self, rule=None,threshold=10000,category=None,type=None,auto=False,source=None,description=None):
        self.rule = rule
        self.threshold = threshold
        self.type = type
        self.category = category
        self.description = description
        self.auto = auto
        self.source = source
        self.guid = uuid1().get_hex()

    def __repr__(self):
        return '<Patrol rule %r>' % (self.rule)


