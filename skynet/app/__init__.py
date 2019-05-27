#coding: utf-8
import threading
from flask import Flask, render_template, current_app
from app.data import set_data_by_key, get_data_by_key
from app.extensions import db, mail, bootstrap, moment,login_manager
from app.modules.auth.models import User
from app.modules.main.mq import req_msg_proc, PubRuleServer, RepStatsServer, RepMiscServer
from config import config
from app import modules


DEFAULT_MODULES = (
    (modules.main, ""),
    (modules.auth, "/auth"),
    (modules.api_v1, "/api/v1"),
)


def create_app(config_name, modules=None):
    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(__name__)
    # config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    configure_extensions(app)

    # register module
    configure_modules(app, modules)

    #error page
    app.error_handler_spec[None][404] = page_not_found
    app.error_handler_spec[None][500] = internal_server_error
    #init data
    app.before_first_request(init_data)
    #
    set_data_by_key("_app",app)
    return app

def configure_extensions(app):
    # configure extensions
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"Please log in to access this page. "
    login_manager.init_app(app)


def configure_modules(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix, static_folder='static',template_folder='templates')

def page_not_found(error):
    return render_template('404.html'), 404



def internal_server_error(error):
    return render_template('500.html'), 500

#数据初始化总入口
def init_data():
    create_user()
    init_mq()
#初始化数据库
def create_user():
    app = current_app
    config = app.config
    email = config.get('USER_EMAIL')
    username = config.get('USER_NAME')
    password = config.get('USER_PASSWORD')
    confirmed = True
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email,username=username,password=password,confirmed=confirmed)
        else:
            user.password = password
            user.confirmed = True
        db.session.add(user)
        db.session.commit()
    except Exception:
        pass


def sub_msg_main():
    with get_data_by_key("_app").app_context():
        config = current_app.config
        addr = config.get('MQ_ADDR')
        port = config.get('MQ_REP_MISC_PORT')
        server = RepMiscServer(addr,port,req_msg_proc)
        server.loop_main()

def init_mq():

    config = current_app.config
    #
    addr = config.get('MQ_ADDR')
    port = config.get('MQ_PUB_RULE_PORT')
    server = PubRuleServer(addr,port)
    set_data_by_key("_pub_rule_server",server)
    #
    addr = config.get('MQ_ADDR')
    port = config.get('MQ_REP_STATS_PORT')
    server = RepStatsServer(addr,port)
    set_data_by_key("_rep_stats_server",server)
    #
    t1 = threading.Thread(target=sub_msg_main)
    t1.start()
    set_data_by_key("_rep_misc_server",t1)
    return

