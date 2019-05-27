#coding: utf-8
import csv

from datetime import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from flask import Blueprint, request,jsonify, make_response
from flask_restful import Api, Resource
import jwt
from werkzeug.utils import secure_filename
from app import db
from app.data import get_data_by_key,set_data_by_key
from app.modules.main.models import Whitelist, Blacklist, Patrollist
from app.modules.main.service import TaskScheduler, CommandExecAcl, Command, CommandExecStats

from flask import current_app


api_v1 = Blueprint('api', __name__)
restfu_api = Api(api_v1)


#############################################
#           internal api
#############################################

@api_v1.before_request
def before_request():
    config = current_app.config
    auth = config.get('AUTHORIZATION')
    if auth:
        authorization = request.headers.get('Authorization', '')
        if authorization:
            try:
                auth_public_key = config.get('AUTHORIZATION_RSA_CERTIFICATE')
                cert_obj = load_pem_x509_certificate(auth_public_key, default_backend())
                public_key = cert_obj.public_key()
                payload = jwt.decode(authorization,public_key,audience='cf')
                return
            except Exception,e:
                print(e)
        return make_response(jsonify({"result":"failed"}), 401)


@restfu_api.resource('/whitelist/','/whitelist/<guid>/','/whitelist/<guid>')
class WhitelistApi(Resource):
    def post(self):
        try:
            req_json = request.json
            rule = Whitelist.query.filter_by(rule=req_json[u"rule"],category=req_json[u"category"],type = req_json[u"type"]).first()
            if not rule:
                rule = Whitelist(req_json["rule"],req_json["category"],req_json["type"],None,req_json["description"])
                # Insert the record in our database and commit it
                db.session.add(rule)
                db.session.commit()
            cmd = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
            cmd.add_acl()
            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed"}

    def delete(self,guid):
        try:
            rule = Whitelist.query.filter_by(guid=guid).first()
            if rule:
                cmd = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
                cmd.del_acl()
                db.session.delete(rule)
                db.session.commit()

            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed"}


@restfu_api.resource('/blacklist/','/blacklist/<guid>/','/blacklist/<guid>')
class BlacklistApi(Resource):
    def post(self):
        try:
            req_json = request.json
            rule = Blacklist.query.filter_by(rule=req_json[u"rule"],category=req_json[u"category"],type = req_json[u"type"]).first()
            if not rule:
                rule = Blacklist(req_json["rule"],req_json["category"],req_json["type"],None,req_json["description"])
                # Insert the record in our database and commit it
                db.session.add(rule)
                db.session.commit()
            cmd = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
            cmd.add_acl()
            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed"}

    def delete(self,guid):
        try:
            rule = Blacklist.query.filter_by(guid=guid).first()
            if rule:
                cmd = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
                cmd.del_acl()
                db.session.delete(rule)
                db.session.commit()
            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed"}

@restfu_api.resource('/patrollist/','/patrollist/<guid>/','/patrollist/<guid>')
class PatrollistApi(Resource):
    def post(self):
        try:
            req_json = request.json
            rule = Patrollist.query.filter_by(rule=req_json[u"rule"],category=req_json[u"category"],type = req_json[u"type"]).first()
            if not rule:
                rule = Patrollist(req_json["rule"],req_json["threshold"],req_json["category"],req_json["type"],req_json["auto"],None,req_json["description"])
                # Insert the record in our database and commit it
                db.session.add(rule)
                db.session.commit()
            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed"}

    def delete(self,guid):
        try:
            rule = Patrollist.query.filter_by(guid=guid).first()
            if rule:
                db.session.delete(rule)
                db.session.commit()
            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed"}

@restfu_api.resource('/exectasks','/exectasks/')
class ExecTaskApi(Resource):
    def post(self):
        try:
            exec_tasks = get_data_by_key("exec_tasks")
            if exec_tasks["exec_status"] == False:
                req_json = request.json
                exec_tasks["exec_status"] = True
                exec_tasks["exec_type"] = req_json["type"]
                exec_tasks["exec_time"] = datetime.strptime(req_json["time"], '%H:%M') if req_json["time"] else None
                exec_tasks["exec_datetime"] = datetime.strptime(req_json["datetime"], '%Y-%m-%d %H:%M') if req_json["datetime"] else None

                if exec_tasks["exec_type"] == "once" and exec_tasks["exec_datetime"] != None:
                    exec_tasks["exec_patrol"] = TaskScheduler(task_type=exec_tasks["exec_type"],task_datetime=exec_tasks["exec_datetime"])
                elif exec_tasks["exec_type"] == "periodicity" and exec_tasks["exec_time"] != None:
                    exec_tasks["exec_patrol"] = TaskScheduler(task_type=exec_tasks["exec_type"],task_datetime=exec_tasks["exec_time"])
                else:
                    return {"result":"failed"}
                exec_tasks["exec_patrol"].exec_task()
                set_data_by_key("exec_tasks",exec_tasks)

            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed"}
    def delete(self):
        try:
            exec_tasks = get_data_by_key("exec_tasks")
            if exec_tasks["exec_status"] == True:
                exec_tasks["exec_patrol"].stop_task()
                exec_tasks["exec_status"] = False
                exec_tasks["exec_type"] = None
                exec_tasks["exec_time"] = None
                exec_tasks["exec_datetime"] = None
                exec_tasks["exec_patrol"] = None
                set_data_by_key("exec_tasks",exec_tasks)
            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed"}


@restfu_api.resource('/warning/','/warning/<guid>/','/warning/<guid>')
class WarningApi(Resource):
    def put(self,guid):
        try:
            rule = Patrollist.query.filter_by(guid=guid).first()
            if rule:
                cmd = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
                cmd.add_acl()
                rule.active = True
                db.session.add(rule)
                db.session.commit()
            return {"result":"successful"}
        except Exception,e :
            return {"result":"failed"}
    def delete(self,guid):
        try:
            rule = Patrollist.query.filter_by(guid=guid).first()
            if rule:
                cmd = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
                cmd.del_acl()
                rule.warning = False
                rule.wctime = None
                rule.active = False
                db.session.add(rule)
                db.session.commit()
            return {"result":"successful"}
        except Exception,e :
            return {"result":"failed"}

@restfu_api.resource('/upload/<type>','/upload/<type>/')
class UploadApi(Resource):
    def post(self,type):
        try:
            if type == "whitelist":
                file = request.files['import_whitelist']
                if file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == "whitelist":
                            rule = Whitelist.query.filter_by(rule=row[5],category=row[1],type = row[2]).first()
                            if not rule:
                                rule = Whitelist(rule=row[5],category=row[1],type = row[2],source="import",description=row[4])
                                # Insert the record in our database and commit it
                                db.session.add(rule)
                                db.session.commit()
                            cmd = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
                            cmd.add_acl()
            elif type == "blacklist":
                file = request.files['import_blacklist']
                if file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == "blacklist":
                            rule = Blacklist.query.filter_by(rule=row[5],category=row[1],type = row[2]).first()
                            if not rule:
                                rule = Blacklist(rule=row[5],category=row[1],type = row[2],source="import",description=row[4])
                                # Insert the record in our database and commit it
                                db.session.add(rule)
                                db.session.commit()
                            cmd = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
                            cmd.add_acl()
            elif type == "patrol":
                file = request.files['import_patrol']
                if file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == "patrol":
                            rule = Patrollist.query.filter_by(rule=row[5],category=row[1],type = row[2]).first()
                            if not rule:
                                rule = Patrollist(rule=row[5],threshold=int(row[3]),category=row[1],type = row[2],source="import",description=row[4])
                                # Insert the record in our database and commit it
                                db.session.add(rule)
                                db.session.commit()
            else:
                return {"result":"failed","reason":"no type"}

            return {"result":"successful"}
        except Exception,e :
            print(e)
            return {"result":"failed","reason":"server exception"}
#############################################
#           ext api
#############################################


@restfu_api.resource('/ext/stats/frontend/<name>','/ext/stats/frontend/<name>/')
class ExtFrontendStats(Resource):
    def get(self,name):
        try:
            cmd = CommandExecStats(name,Command("_rep_stats_server"))
            metric =cmd.get_stats()
            return metric
        except Exception,e:
            print(e)
            return 0.0


