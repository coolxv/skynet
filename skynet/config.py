#coding: utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG=False
    TESTING=False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = 'public'
    RECAPTCHA_PRIVATE_KEY = 'private'
    #sqlalchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #wtf
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'a random string'
    #mq#custom
    MQ_ADDR = "0.0.0.0"
    MQ_PUB_RULE_PORT = "5555"
    MQ_REP_MISC_PORT = "5556"
    MQ_REP_STATS_PORT = "5557"

    #elk
    ELK_ADDR = 'http://123.56.9.150:9200/'
    #user#custom
    USER_NAME = u"skynet"
    USER_PASSWORD = u"skynet"
    USER_EMAIL = u"skynet@dtdream.com"
    #mail#custom
    MAIL_SERVER = 'smtp.dtdream.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USERNAME = "skynet@dtdream.com" #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = "skynet" #os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <zhangdx@dtdream.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    #api sec#custom
    AUTHORIZATION = False
    AUTHORIZATION_RSA_CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIICUjCCAbugAwIBAgIJAInhlwF3ouu7MA0GCSqGSIb3DQEBCwUAMEIxCzAJBgNV
BAYTAlhYMRUwEwYDVQQHDAxEZWZhdWx0IENpdHkxHDAaBgNVBAoME0RlZmF1bHQg
Q29tcGFueSBMdGQwHhcNMTUxMTEzMDYxNjI3WhcNMTgxMTEyMDYxNjI3WjBCMQsw
CQYDVQQGEwJYWDEVMBMGA1UEBwwMRGVmYXVsdCBDaXR5MRwwGgYDVQQKDBNEZWZh
dWx0IENvbXBhbnkgTHRkMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHFr+K
ICms+tuT1OXJwhCUmR2dKVy7psa8xzElSyzqx7oJyfJ1JZyOzToj9T5SfTIq396a
gbHJWVfYphNahvZ/7uMXqHxf+ZH9BL1gk9Y6kCnbM5R60gfwjyW1/dQPjOzn9N39
4zd2FJoFHwdq9Qs0wBugspULZVNRxq7veq/fzwIDAQABo1AwTjAdBgNVHQ4EFgQU
rwLtreYvDJsRiv/J9SPNfX6DbSkwHwYDVR0jBBgwFoAUrwLtreYvDJsRiv/J9SPN
fX6DbSkwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOBgQBsIxFi42j7dl6L
cvFwuZWWcllPT6gFXXPDEp/LZHG37hn/lzYd3YYgJdOGt7onAn0ZGVH1gsSa7ZbB
5+wgWQgHeIdsSR7LNTVThuGl6ouej7TRuo12RhTbSUo3nDeq7pCnXSYjK7aIVG0c
hfJYXf0emMHxQtIYwudr+OGLtFG+zw==
-----END CERTIFICATE-----"""
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data','data-dev.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'data', 'migrations')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data','data-test.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'data', 'migrations')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data','data.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'data', 'migrations')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}