#coding: utf-8
from StringIO import StringIO
from flask import render_template, Blueprint,redirect,url_for, make_response, request
from flask.ext.login import login_required
from app.data import get_data_by_key
from app.modules.main.constants import RULE_TYPE,  RULE_DESCRIPTION, RULE_ACTIVE, RULE_AUTO
from app.modules.main.models import Whitelist, Blacklist, Patrollist

main = Blueprint('main', __name__)




@main.route('/')
@main.route('/dashboard.html')
@login_required
def index():
    count = {}
    count["plugins_num"] = len(get_data_by_key("plugins"))
    count["whitelist_rules"] = len(Whitelist.query.all())
    count["blacklist_rules"] = len(Blacklist.query.all())
    count["patrollist_rules"] = len(Patrollist.query.all())
    count["warning_rules"] = len(Patrollist.query.filter_by(warning=True).all())
    return render_template('main/dashboard.html',count=count)

@main.route('/whitelist.html')
@login_required
def whitelist():
    user_agent_rules = Whitelist.query.filter_by(category=u'user_agent_rule').all()
    return render_template('main/whitelist.html',user_agent_rules=user_agent_rules,type=RULE_TYPE)


@main.route('/blacklist.html')
@login_required
def blacklist():
    user_agent_rules = Blacklist.query.filter_by(category=u'user_agent_rule').all()
    refferer_rules = Blacklist.query.filter_by(category=u'referrer_rule').all()
    url_rules = Blacklist.query.filter_by(category=u'url_rule').all()
    return render_template('main/blacklist.html',user_agent_rules=user_agent_rules,refferer_rules=refferer_rules,url_rules=url_rules, type=RULE_TYPE,description=RULE_DESCRIPTION)

@main.route('/patrollist.html')
@login_required
def patrol():
    user_agent_rules = Patrollist.query.filter_by(category=u'user_agent_rule').all()
    refferer_rules = Patrollist.query.filter_by(category=u'referrer_rule').all()
    url_rules = Patrollist.query.filter_by(category=u'url_rule').all()
    exec_tasks = get_data_by_key("exec_tasks")
    return render_template('main/patrollist.html',user_agent_rules=user_agent_rules,refferer_rules=refferer_rules,url_rules=url_rules, type=RULE_TYPE,auto=RULE_AUTO,description=RULE_DESCRIPTION,exec_status=exec_tasks["exec_status"])


@main.route('/warning.html')
@login_required
def warning():
    nonauto_warnings = Patrollist.query.filter_by(warning=True,auto=False).all()
    auto_warnings = Patrollist.query.filter_by(warning=True,auto=True).all()
    return render_template('main/warning.html',nonauto_warnings=nonauto_warnings,auto_warnings=auto_warnings,description=RULE_DESCRIPTION,active=RULE_ACTIVE)



@main.route('/download')
@main.route('/download/')
@login_required
def download():
    type = request.args["type"]
    csv_data = StringIO()
    if type == "whitelist":
        user_agent_rules = Whitelist.query.filter_by(category=u'user_agent_rule').all()
        for user_agent_rule in user_agent_rules:
            csv_data.write(type+","+user_agent_rule.category+","+user_agent_rule.type+","+","+u"\"%s\""%user_agent_rule.description+","+u"\"%s\""%user_agent_rule.rule+"\r\n")
    elif type == "blacklist":
        user_agent_rules = Blacklist.query.filter_by(category=u'user_agent_rule').all()
        for user_agent_rule in user_agent_rules:
            csv_data.write(type+","+user_agent_rule.category+","+user_agent_rule.type+","+","+u"\"%s\""%user_agent_rule.description+","+u"\"%s\""%user_agent_rule.rule+"\r\n")
        refferer_rules = Blacklist.query.filter_by(category=u'referrer_rule').all()
        for refferer_rule in refferer_rules:
            csv_data.write(type+","+refferer_rule.category+","+refferer_rule.type+","+","+u"\"%s\""%refferer_rule.description+","+u"\"%s\""%refferer_rule.rule+"\r\n")
        url_rules = Blacklist.query.filter_by(category=u'url_rule').all()
        for url_rule in url_rules:
            csv_data.write(type+","+url_rule.category+","+url_rule.type+","+","+u"\"%s\""%url_rule.description+","+u"\"%s\""%url_rule.rule+"\r\n")
    elif type == "patrol":
        user_agent_rules = Patrollist.query.filter_by(category=u'user_agent_rule').all()
        for user_agent_rule in user_agent_rules:
            csv_data.write(type+","+user_agent_rule.category+","+user_agent_rule.type+","+str(user_agent_rule.threshold)+","+u"\"%s\""%user_agent_rule.description+","+u"\"%s\""%user_agent_rule.rule+"\r\n")
        refferer_rules = Patrollist.query.filter_by(category=u'referrer_rule').all()
        for refferer_rule in refferer_rules:
            csv_data.write(type+","+refferer_rule.category+","+refferer_rule.type+","+str(refferer_rule.threshold)+","+u"\"%s\""%refferer_rule.description+","+u"\"%s\""%refferer_rule.rule+"\r\n")
        url_rules = Patrollist.query.filter_by(category=u'url_rule').all()
        for url_rule in url_rules:
            csv_data.write(type+","+url_rule.category+","+url_rule.type+","+str(url_rule.threshold)+","+u"\"%s\""%url_rule.description+","+u"\"%s\""%url_rule.rule+"\r\n")

    response = make_response(csv_data.getvalue())

    response.headers["Content-Disposition"] = "attachment; filename=%s.csv"%type
    return response

@main.route('/<name>')
@login_required
def wildcard(name=''):
    if name not in ["dashboard.html","whitelist.html","blacklist.html","patrollist.html","warning.html"]:
        return redirect(url_for("main.index"))

