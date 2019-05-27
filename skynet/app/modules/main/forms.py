#coding: utf-8
from flask_wtf import Form
from wtforms import StringField,IntegerField,SelectField, DateTimeField


class RuleForm(Form):
    category = StringField('category')
    rule = StringField('rule')
    threshold = IntegerField('threshold')
    type = SelectField('type')
    behavior = SelectField('behavior')
    description = SelectField('description')

class ExecTaskForm(Form):
    time = DateTimeField(u'time' ,format='%H:%M')
    datetime = DateTimeField(u'datetime' ,format='%Y-%m-%d %H:%M')
    type = SelectField('type')