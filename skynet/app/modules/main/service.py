#coding: utf-8
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from elasticsearch import Elasticsearch
from flask import current_app
from app import db
from app.data import set_data_by_key,get_data_by_key
from app.modules.main.models import Patrollist


class TaskScheduler():
    def __init__(self,**kwargs):
        self.datetime = kwargs["task_datetime"]
        self.type = kwargs["task_type"]
        self.scheduler = BackgroundScheduler()
        self.task_proxy = TaskProxy()


    def __task(self):
        exec_tasks = get_data_by_key("exec_tasks")
        if exec_tasks["exec_status"] == True and exec_tasks["exec_type"] == "once":
            exec_tasks["exec_status"] = False
            exec_tasks["exec_type"] = None
            exec_tasks["exec_time"] = None
            exec_tasks["exec_datetime"] = None
            exec_tasks["exec_patrol"] = None
            set_data_by_key("exec_tasks",exec_tasks)
        ##### ####
        with get_data_by_key("_app").app_context():
            active_rules = Patrollist.query.filter_by(warning=False).all()
            for rule in active_rules:
                result = self.task_proxy.do_task(rule)
                if result == True:
                    try:
                        rule.warning = True
                        rule.wctime = datetime.utcnow()
                        if rule.auto == True:
                            rule.active = True
                            cmd_exec = CommandExecAcl(rule.rule,rule.category,rule.type,Command("_pub_rule_server"))
                            cmd_exec.add_acl()
                        db.session.add(rule)
                        db.session.commit()
                    except Exception,e:
                        print(e)
                        return False

    def __exec_periodicity(self):
        self.scheduler.add_job(self.__task, 'cron', hour=self.datetime.hour,minute=self.datetime.minute)
        self.scheduler.start()

    def __exec_once(self):
        self.scheduler.add_job(self.__task, 'date', run_date=self.datetime)
        self.scheduler.start()

    def exec_task(self):
        if self.type == "once":
            self.__exec_once()
        else:
            self.__exec_periodicity()
    def stop_task(self):
        self.scheduler.shutdown(wait=False)



class TaskProxy():
    def __init__(self):
        self.task = ElkTask()
    def do_task(self,rule):
        return self.task.do_task(rule)



class ElkTask():
    def __init__(self):
        config = current_app.config
        elk_addr = config.get('ELK_ADDR')
        self.es = Elasticsearch(elk_addr)
        self.es.cluster.health(request_timeout=10)
    def do_user_agent_reg(self,threshold,reg_string):
        try:
            res = self.es.count(body = {
                "query": {
                    "filtered": {
                        "query":  { "regexp": {
                            "logs.http_user_agent": "%s"%(reg_string)
                        }
                        },
                        "filter": { "term":  { "logs.source_type.raw": "RTR" }}
                    }

                }
            })
            return res["count"] >= threshold
        except Exception,e:
            print(e)
            return False

    def do_user_agent_sub(self,threshold,sub_string):
        try:
            res = self.es.count(body = {
                "query": {
                    "filtered": {
                        "query":  { "wildcard": {
                            "logs.http_user_agent": "*%s*"%(sub_string)
                        }
                        },
                        "filter": { "term":  { "logs.source_type.raw": "RTR" }}
                    }

                }
            })
            return res["count"] >= threshold
        except Exception,e:
            print(e)
            return False
    def do_referrer_reg(self,threshold,reg_string):
        try:
            res = self.es.count(body = {
                "query": {
                    "filtered": {
                        "query":  { "regexp": {
                            "logs.referer": "%s"%(reg_string)
                        }
                        },
                        "filter": { "term":  { "logs.source_type.raw": "RTR" }}
                    }

                }
            })
            return res["count"] >= threshold
        except Exception,e:
            print(e)
            return False

    def do_referrer_sub(self,threshold,sub_string):
        try:
            res = self.es.count(body = {
                "query": {
                    "filtered": {
                        "query":  { "wildcard": {
                            "logs.referer": "*%s*"%(sub_string)
                        }
                        },
                        "filter": { "term":  { "logs.source_type.raw": "RTR" }}
                    }

                }
            })
            return res["count"] >= threshold
        except Exception,e:
            print(e)
            return False
    def do_url_reg(self,threshold,reg_string):
        try:
            res = self.es.count(body = {
                "query": {
                    "filtered": {
                        "query":{
                            "bool":{
                                "should":[
                                    {
                                        "regexp": {
                                            "logs.hostname": "%s"%(reg_string)
                                        }
                                    },
                                    {
                                        "regexp": {
                                            "logs.path": "%s"%(reg_string)
                                        }
                                    },
                                ]
                            }},
                        "filter": { "term":  { "logs.source_type.raw": "RTR" }}
                    }

                }
            })
            return res["count"] >= threshold
        except Exception,e:
            print(e)
            return False

    def do_url_sub(self,threshold,sub_string):
        try:
            res = self.es.count(body = {
                "query": {
                    "filtered": {
                        "query":{
                            "bool":{
                                "should":[
                                    {
                                        "wildcard": {
                                            "logs.hostname": "*%s*"%(sub_string)
                                        }
                                    },
                                    {
                                        "wildcard": {
                                            "logs.path": "*%s*"%(sub_string)
                                        }
                                    },
                                ]
                            }},
                        "filter": { "term":  { "logs.source_type.raw": "RTR" }}
                    }

                }
            })
            return res["count"] >= threshold
        except Exception,e:
            print(e)
            return False

    def do_task(self,rule):
        result = False
        if rule.category == "url_rule":
            if rule.type == "sub":
                result = self.do_url_sub(rule.threshold,rule.rule)
            elif rule.type == "reg":
                result = self.do_url_reg(rule.threshold,rule.rule)
        elif rule.category == "user_agent_rule" or rule.category == "whitelist_rule":
            if rule.type == "sub":
                result = self.do_user_agent_sub(rule.threshold,rule.rule)
            elif rule.type == "reg":
                result = self.do_user_agent_reg(rule.threshold,rule.rule)
        elif rule.category == "referrer_rule":
            if rule.type == "sub":
                result = self.do_referrer_sub(rule.threshold,rule.rule)
            elif rule.type == "reg":
                result = self.do_referrer_reg(rule.threshold,rule.rule)
        return result

###########################################################
###########################################################

class Command():
    def __init__(self,server_type):
        self.cmd = get_data_by_key(server_type)

    def send_cmd(self,cmd):
        return self.cmd.send_cmd(cmd)

class CommandExecAcl():
    def __init__(self,rule,category,type,cmd_actuator):
        self.cmd = {"rule":rule,"category":category,"type":type}
        self.cmd_actuator = cmd_actuator

    def add_acl(self):
        result = False
        self.cmd["op"] = "add"
        add_cmd = {"op":"real-rule-req","data":self.cmd}
        try:
            self.cmd_actuator.send_cmd(add_cmd)
        except Exception,e:
            result = False
            print(e)
        return result
    def del_acl(self):
        result = False
        self.cmd["op"] = "del"
        del_cmd = {"op":"real-rule-req","data":self.cmd}
        try:
            self.cmd_actuator.send_cmd(del_cmd)
        except Exception,e:
            result = False
            print(e)
        return result
    def clean_acl(self):
        result = False
        self.cmd["op"] = "clean"
        clean_cmd = {"op":"real-rule-req","data":self.cmd}
        try:
            self.cmd_actuator.send_cmd(clean_cmd)
        except Exception,e:
            result = False
            print(e)
        return result

class CommandExecStats():
    def __init__(self,name,cmd_actuator):
        self.cmd = {"name":name}
        self.cmd_actuator = cmd_actuator

    def get_stats(self):
        metric = 0.0
        stats_cmd = {"op":"real-stats-req","data":self.cmd}
        try:
            results = self.cmd_actuator.send_cmd(stats_cmd)
            for r in results:
                metric += r["result"]
        except Exception,e:
            print(e)
        return metric






