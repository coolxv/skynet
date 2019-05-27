#coding: utf-8
import httplib
import os
import threading
from time import sleep
import sys
import signal
import zmq
from zmq.backend.cython.utils import ZMQError
from config import  ACL_USER_AGENT_REG_NEG, ACL_USER_AGENT_SUB, ACL_USER_AGENT_REG, ACL_REFERRER_REG_NEG, \
    ACL_REFERRER_SUB, ACL_REFERRER_REG, ACL_URL_REG_NEG, ACL_URL_SUB, ACL_URL_REG, HAPROXY_UNIX_SOCKET_DIR, \
    ID, HAPROXY_FRONTENDS, MQ_ADDR, MQ_REP_MISC_PORT, MQ_PUB_RULE_PORT, \
    MQ_REP_STATS_PORT,SERVER_URL
from haproxyadmin import haproxy
from haproxyadmin.frontend import Frontend


class Command():
    def __init__(self):
        self.hap = haproxy.HAProxy(socket_dir=HAPROXY_UNIX_SOCKET_DIR)

    #user_agent add
    def add_acl_user_agent_reg_neg(self,pattern):
        try:
            return self.hap.add_acl(ACL_USER_AGENT_REG_NEG,pattern)
        except Exception,e:
            print(e)
            return False

    def add_acl_user_agent_sub(self,pattern):
        try:
            return self.hap.add_acl(ACL_USER_AGENT_SUB,pattern)
        except Exception,e:
            print(e)
            return False

    def add_acl_user_agent_reg(self,pattern):
        try:
            return self.hap.add_acl(ACL_USER_AGENT_REG,pattern)
        except Exception,e:
            print(e)
            return False

    #user_agent del
    def del_acl_user_agent_reg_neg(self,pattern):
        try:
            return self.hap.del_acl(ACL_USER_AGENT_REG_NEG,pattern)
        except Exception,e:
            print(e)
            return False

    def del_acl_user_agent_sub(self,pattern):
        try:
            return self.hap.del_acl(ACL_USER_AGENT_SUB,pattern)
        except Exception,e:
            print(e)
            return False

    def del_acl_user_agent_reg(self,pattern):
        try:
            return self.hap.del_acl(ACL_USER_AGENT_REG,pattern)
        except Exception,e:
            print(e)
            return False
    #user_agent clean
    def clean_acl_user_agent_reg_neg(self):
        try:
            return self.hap.clear_acl(ACL_USER_AGENT_REG_NEG)
        except Exception,e:
            print(e)
            return False
    def clean_acl_user_agent_sub(self):
        try:
            return self.hap.clear_acl(ACL_USER_AGENT_SUB)
        except Exception,e:
            print(e)
            return False
    def clean_acl_user_agent_reg(self):
        try:
            return self.hap.clear_acl(ACL_USER_AGENT_REG)
        except Exception,e:
            print(e)
            return False

    #referer add
    def add_acl_referrer_reg_neg(self,pattern):
        try:
            return self.hap.add_acl(ACL_REFERRER_REG_NEG,pattern)
        except Exception,e:
            print(e)
            return False
    def add_acl_referrer_sub(self,pattern):
        try:
            return self.hap.add_acl(ACL_REFERRER_SUB,pattern)
        except Exception,e:
            print(e)
            return False

    def add_acl_referrer_reg(self,pattern):
        try:
            return self.hap.add_acl(ACL_REFERRER_REG,pattern)
        except Exception,e:
            print(e)
            return False
    #referer del
    def del_acl_referrer_reg_neg(self,pattern):
        try:
            return self.hap.del_acl(ACL_REFERRER_REG_NEG,pattern)
        except Exception,e:
            print(e)
            return False
    def del_acl_referrer_sub(self,pattern):
        try:
            return self.hap.del_acl(ACL_REFERRER_SUB,pattern)
        except Exception,e:
            print(e)
            return False

    def del_acl_referrer_reg(self,pattern):
        try:
            return self.hap.del_acl(ACL_REFERRER_REG,pattern)
        except Exception,e:
            print(e)
            return False

    #referer clean
    def clean_acl_referrer_reg_neg(self):
        try:
            return self.hap.clear_acl(ACL_REFERRER_REG_NEG)
        except Exception,e:
            print(e)
            return False
    def clean_acl_referrer_sub(self):
        try:
            return self.hap.clear_acl(ACL_REFERRER_SUB)
        except Exception,e:
            print(e)
            return False
    def clean_acl_referrer_reg(self):
        try:
            return self.hap.clear_acl(ACL_REFERRER_REG)
        except Exception,e:
            print(e)
            return False

    #url add
    def add_acl_url_reg_neg(self,pattern):
        try:
            return self.hap.add_acl(ACL_URL_REG_NEG,pattern)
        except Exception,e:
            print(e)
            return False
    def add_acl_url_sub(self,pattern):
        try:
            return self.hap.add_acl(ACL_URL_SUB,pattern)
        except Exception,e:
            print(e)
            return False
    def add_acl_url_reg(self,pattern):
        try:
            return self.hap.add_acl(ACL_URL_REG,pattern)
        except Exception,e:
            print(e)
            return False
    #url del
    def del_acl_url_reg_neg(self,pattern):
        try:
            return self.hap.del_acl(ACL_URL_REG_NEG,pattern)
        except Exception,e:
            print(e)
            return False
    def del_acl_url_sub(self,pattern):
        try:
            return self.hap.del_acl(ACL_URL_SUB,pattern)
        except Exception,e:
            print(e)
            return False
    def del_acl_url_reg(self,pattern):
        try:
            return self.hap.del_acl(ACL_URL_REG,pattern)
        except Exception,e:
            print(e)
            return False
    #url clean
    def clean_acl_url_reg_neg(self):
        try:
            return self.hap.clear_acl(ACL_URL_REG_NEG)
        except Exception,e:
            print(e)
            return False
    def clean_acl_url_sub(self):
        try:
            return self.hap.clear_acl(ACL_URL_SUB)
        except Exception,e:
            print(e)
            return False
    def clean_acl_url_reg(self):
        try:
            return self.hap.clear_acl(ACL_URL_REG)
        except Exception,e:
            print(e)
            return False
    #status
    def get_runtime(self):
        try:
            return self.hap.uptimesec
        except Exception,e:
            print(e)
            return -1

    def get_fstats(self,frontends,name):
        try:
            metric = 0.0
            if name not in Frontend.FRONTEND_METRICS:
                return metric
            for frontend in frontends:
                f = self.hap.frontend(frontend)
                metric += f.metric(name)
            return metric
        except Exception,e:
            print(e)
            return 0.0
###########################################################################
###########################################################################
class CommandExecAcl():
    def __init__(self,cmd,rule,category,type):
        self.rule = rule
        self.category = category
        self.type = type
        self.cmd = cmd
    def exec_cmd(self,op):
        if op == "add":
            self.__del_acl()
            self.__add_acl()
        elif op == "del":
            self.__del_acl()
        elif op == "clean":
            self.__clean_acl()
        else:
            print("CommandExecAcl:","error operation")


    def __add_acl(self):
        result = False
        if self.category == u"user_agent_rule":
            if self.type == u"sub":
                result = self.cmd.add_acl_user_agent_sub(self.rule)
            elif self.type == u"reg":
                result = self.cmd.add_acl_user_agent_reg(self.rule)
            elif self.type == u"regneg":
                result = self.cmd.add_acl_user_agent_reg_neg(self.rule)
        elif self.category == u"referrer_rule":
            if self.type == u"sub":
                result = self.cmd.add_acl_referrer_sub(self.rule)
            elif self.type == u"reg":
                result = self.cmd.add_acl_referrer_reg(self.rule)
            elif self.type == u"regneg":
                result = self.cmd.add_acl_referrer_reg_neg(self.rule)
        elif self.category == u"url_rule":
            if self.type == u"sub":
                result = self.cmd.add_acl_url_sub(self.rule)
            elif self.type == u"reg":
                result = self.cmd.add_acl_url_reg(self.rule)
            elif  self.type == u"regneg":
                result = self.cmd.add_acl_url_reg_neg(self.rule)
        return result
    def __del_acl(self):
        result = False
        if self.category == u"user_agent_rule":
            if self.type == u"sub":
                result = self.cmd.del_acl_user_agent_sub(self.rule)
            elif self.type == u"reg":
                result = self.cmd.del_acl_user_agent_reg(self.rule)
            elif self.type == u"regneg":
                result = self.cmd.del_acl_user_agent_reg_neg(self.rule)
        elif self.category == u"referrer_rule":
            if self.type == u"sub":
                result = self.cmd.del_acl_referrer_sub(self.rule)
            elif self.type == u"reg":
                result = self.cmd.del_acl_referrer_reg(self.rule)
            elif self.type == u"regneg":
                result = self.cmd.del_acl_referrer_reg_neg(self.rule)
        elif self.category == u"url_rule":
            if self.type == u"sub":
                result = self.cmd.del_acl_url_sub(self.rule)
            elif self.type == u"reg":
                result = self.cmd.del_acl_url_reg(self.rule)
            elif self.type == u"regneg":
                result = self.cmd.del_acl_url_reg_neg(self.rule)
        return result
    def __clean_acl(self):
        result = False
        if self.category == u"user_agent_rule":
            if self.type == u"sub":
                result = self.cmd.clean_acl_user_agent_sub()
            elif self.type == u"reg":
                result = self.cmd.clean_acl_user_agent_reg()
            elif self.type == u"regneg":
                result = self.cmd.clean_acl_user_agent_reg_neg()
        elif self.category == u"referrer_rule":
            if self.type == u"sub":
                result = self.cmd.clean_acl_referrer_sub()
            elif self.type == u"reg":
                result = self.cmd.clean_acl_referrer_reg()
            elif self.type == u"regneg":
                result = self.cmd.clean_acl_referrer_reg_neg()
        elif self.category == u"url_rule":
            if self.type == u"sub":
                result = self.cmd.clean_acl_url_sub()
            elif self.type == u"reg":
                result = self.cmd.clean_acl_url_reg()
            elif self.type == u"regneg":
                result = self.cmd.clean_acl_url_reg_neg()
        return result

class CommandExecStats():
    def __init__(self,cmd,frontends):
        self.frontends = frontends
        self.cmd = cmd
    def exec_cmd(self,name):
        return self.cmd.get_fstats(self.frontends,name)
###########################################################################
###########################################################################
class SubRuleClient(object):
    def __init__(self,remote_addr,remote_port,callback,callback_data):
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.callback = callback
        self.callback_data = callback_data
        #
        self.context = zmq.Context()
        self.subscribe = self.context.socket(zmq.SUB)
        self.subscribe.connect("tcp://%s:%s"%(remote_addr,remote_port))
        self.subscribe.setsockopt(zmq.SUBSCRIBE, b"")


    def process_real_rule(self):
        poller = zmq.Poller()
        poller.register(self.subscribe, zmq.POLLIN)
        while True:
            try:
                socks = dict(poller.poll())
            # except KeyboardInterrupt:
            #     continue
                if self.subscribe in socks:
                    message = self.subscribe.recv_json()
                    if message["op"] == "real-rule-req":
                        self.callback(self.callback_data,message["data"])
            except Exception,e:
                print("process_real_rule",e)

class ReqMiscClient(object):
    def __init__(self,id,remote_addr,remote_port,callback,callback_data):
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.callback = callback
        self.callback_data = callback_data
        #
        self.context = zmq.Context()
        self.dealer = self.context.socket(zmq.DEALER)
        self.id = id
        self.dealer.setsockopt(zmq.IDENTITY,self.id)
        self.dealer.connect("tcp://%s:%s"%(remote_addr,remote_port))
    #once batch rule
    def process_batch_rule(self):
        err_count = 0
        #
        poller = zmq.Poller()
        poller.register(self.dealer, zmq.POLLIN)
        #
        self.dealer.send_json({"op":"batch-rule-req","data":{}})
        while True:
            if err_count > 3:
                raise ZMQError
            try:
                socks = dict(poller.poll(5000))
                if self.dealer in socks:
                    message = self.dealer.recv_json()
                    if message["op"] == "batch-rule-end":
                        break
                    elif message["op"] == "batch-rule-rep":
                        self.callback(self.dealer,self.callback_data,message["data"])
                else:
                    err_count += 1
            # except KeyboardInterrupt:
            #     continue
            except Exception,e:
                err_count += 1
                print("process_batch_rule:",e)

    #once register identity
    def process_register(self):
        err_count = 0
        #
        poller = zmq.Poller()
        poller.register(self.dealer, zmq.POLLIN)
        while True:
            if err_count > 3:
                raise ZMQError
            try:
                self.dealer.send_json({"op":"register-req","data":{"id":ID}})
                socks = dict(poller.poll(5000))
                if self.dealer in socks:
                    message = self.dealer.recv_json()
                    if message["op"] == "register-rep":
                        break
                err_count += 1
            # except KeyboardInterrupt:
            #     continue
            except Exception,e:
                err_count += 1
                print("process_register:",e)


class ReqStatsClient(object):
    def __init__(self,id,remote_addr,remote_port,callback,callback_data):
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.callback = callback
        self.callback_data = callback_data
        #
        self.context = zmq.Context()
        self.dealer = self.context.socket(zmq.DEALER)
        self.id = id
        self.dealer.setsockopt(zmq.IDENTITY,self.id)
        self.dealer.setsockopt(zmq.SNDTIMEO,2000)
        self.dealer.connect("tcp://%s:%s"%(remote_addr,remote_port))
        self.poller = zmq.Poller()
    #
    def process_real_stats(self):
        self.poller.register(self.dealer, zmq.POLLIN)
        while True:
            try:
                socks = dict(self.poller.poll())
                if self.dealer in socks:
                    message = self.dealer.recv_json()
                    if message["op"] == "real-stats-req":
                        self.callback(self.dealer,self.callback_data,message["data"])
            # except KeyboardInterrupt:
            #     continue
            except Exception,e:
                print("process_real_stats:",e)


#######################################################
#######################################################
####real
def sub_real_rule_msg_main():
    client = SubRuleClient(MQ_ADDR,MQ_PUB_RULE_PORT,sub_real_rule_msg_proc,Command())
    client.process_real_rule()

def sub_real_rule_msg_proc(cmd,data):
    try:
        cmd = CommandExecAcl(cmd,data["rule"],data["category"],data["type"])
        cmd.exec_cmd(data["op"])
    except Exception,e:
        print("sub_real_rule_msg_proc:",e)
####batch
def req_batch_rule_msg_proc(dealer,cmd,data):
    try:
        cmd = CommandExecAcl(cmd,data["rule"],data["category"],data["type"])
        cmd.exec_cmd(data["op"])
    except Exception,e:
        print("req_batch_rule_msg_proc:",e)

####stats
def req_real_stats_msg_main():
    stats_client = ReqStatsClient(ID,MQ_ADDR,MQ_REP_STATS_PORT,req_real_stats_msg_proc,Command())
    stats_client.process_real_stats()

def req_real_stats_msg_proc(dealer,cmd,data):
    try:
        cmd = CommandExecStats(cmd,HAPROXY_FRONTENDS)
        result = cmd.exec_cmd(data["name"])
        dealer.send_json({"op":"real-stats-rep","data":{"result":result}})
    except Exception,e:
        print("req_real_stats_msg_proc:",e)

##############################################################
##############################################################
def try_http():
    conn = httplib.HTTPConnection(SERVER_URL)
    conn.request("HEAD","/")
    res = conn.getresponse()
    if(int(res.status) >= 400):
        return False
    else:
        return True

#
def clean_all_acl(cmd):
    try:
        cmd.clean_acl_user_agent_sub()
        cmd.clean_acl_user_agent_reg()
        cmd.clean_acl_user_agent_reg_neg()
        cmd.clean_acl_referrer_sub()
        cmd.clean_acl_referrer_reg()
        #cmd.clean_acl_referrer_reg_neg()
        cmd.clean_acl_url_sub()
        cmd.clean_acl_url_reg()
        #cmd.clean_acl_url_reg_neg()
    except Exception,e:
        print("clean_all_acl:",e)
    return

def main_loop():
    #初始化haproxyadmin
    cmd = Command()
    runtime = 0
    client = ReqMiscClient(ID,MQ_ADDR,MQ_REP_MISC_PORT,req_batch_rule_msg_proc,cmd)
    while True:
        runtime_tmp = cmd.get_runtime()
        if (runtime > runtime_tmp or runtime == 0 or not try_http()) and -1 != runtime_tmp:
            client.process_register()
            clean_all_acl(cmd)
            client.process_batch_rule()
        runtime = runtime_tmp
        sleep(5)
def main():
    try:
        #尝试连接 skynet core，使其初始化MQ
        if try_http():
            #real rule thread
            t1 = threading.Thread(target=sub_real_rule_msg_main)
            t1.setDaemon(True)
            t1.start()
            #real stats thread
            t2 = threading.Thread(target=req_real_stats_msg_main)
            t2.setDaemon(True)
            t2.start()
            #heartbeat
            main_loop()
    except Exception,e:
        print("main:",e)

def restart_program():
    sleep(5)
    print("I restart")
    python = sys.executable
    os.execl(python, python, * sys.argv)

def sig_handler(signum, frame):
    print('I received: ', signum)
    exit(0)

############################################################
############################################################
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sig_handler)
    main()
    restart_program()