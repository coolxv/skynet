#coding: utf-8
import zmq
from app.data import get_data_by_key, set_data_by_key
from app.modules.main.models import Whitelist, Blacklist, Patrollist


class PubRuleServer(object):
    def __init__(self,local_addr,local_port):
        self.local_addr = local_addr
        self.local_port = local_port
        #
        self.context = zmq.Context()
        self.publish = self.context.socket(zmq.PUB)
        self.publish.bind("tcp://%s:%s"%(local_addr,local_port))

    def send_cmd(self,cmd):
        self.publish.send_json(cmd)

class RepStatsServer(object):
    def __init__(self,local_addr,local_port):
        self.local_addr = local_addr
        self.local_port = local_port
        #
        self.context = zmq.Context()
        self.route = self.context.socket(zmq.ROUTER)
        self.route.bind("tcp://%s:%s"%(local_addr,local_port))

    def send_cmd(self,cmd):
        result = []
        plugin_tmp = []
        plugins = get_data_by_key("plugins")
        poller = zmq.Poller()
        poller.register(self.route, zmq.POLLIN)
        err_count = 0
        for plugin in plugins:
            self.route.send_string(plugin,zmq.SNDMORE)
            self.route.send_json(cmd)
            try:
                socks = dict(poller.poll(3000))
                if self.route in socks:
                    who = self.route.recv()
                    message = self.route.recv_json()
                    if message["op"] == "real-stats-rep" and who == plugin:
                        result.append(message["data"])
                    plugin_tmp.append(plugin)
                else:
                    err_count += 1
            except KeyboardInterrupt:
                continue
        if err_count > 0:
            set_data_by_key("plugins",plugin_tmp)
        return result





####################################

class RepMiscServer(object):
    def __init__(self,local_addr,local_port,callback):
        self.local_addr = local_addr
        self.local_port = local_port
        self.callback = callback
        #
        self.context = zmq.Context()
        self.route = self.context.socket(zmq.ROUTER)
        self.route.bind("tcp://%s:%s"%(local_addr,local_port))

    def loop_main(self):
        poller = zmq.Poller()
        poller.register(self.route, zmq.POLLIN)
        while True:
            try:
                socks = dict(poller.poll())
            except KeyboardInterrupt:
                continue
            if self.route in socks:
                #
                try:
                    who = self.route.recv()
                    message = self.route.recv_json()
                    print(message)
                    self.callback(self,who,message)
                except Exception,e:
                    print e


def req_msg_proc(client,who,message):
    if "register-req" == message["op"]:
        plugins = get_data_by_key("plugins")
        if message["data"]["id"] not in plugins:
            plugins.append(message["data"]["id"])
            set_data_by_key("plugins",plugins)
        client.route.send_string(who,zmq.SNDMORE)
        client.route.send_json({"op":"register-rep","data":{}})
    elif "batch-rule-req" == message["op"]:
        client.route.send_string(who,zmq.SNDMORE)
        #
        whitelist_rules = Whitelist.query.all()
        for rule in whitelist_rules:
            client.route.send_json({"op":"batch-rule-rep","data":{"rule":rule.rule,"category":rule.category,"type":rule.type,"op":"add"}}, zmq.SNDMORE)
        blacklist_rules = Blacklist.query.all()
        for rule in blacklist_rules:
            client.route.send_json({"op":"batch-rule-rep","data":{"rule":rule.rule,"category":rule.category,"type":rule.type,"op":"add"}}, zmq.SNDMORE)
        warnings_rules_auto = Patrollist.query.filter_by(warning=True,auto=True).all()
        for rule in warnings_rules_auto:
            client.route.send_json({"op":"batch-rule-rep","data":{"rule":rule.rule,"category":rule.category,"type":rule.type,"op":"add"}}, zmq.SNDMORE)
        warnings_rules = Patrollist.query.filter_by(warning=True,auto=False,active=True).all()
        for rule in warnings_rules:
            client.route.send_json({"op":"batch-rule-rep","data":{"rule":rule.rule,"category":rule.category,"type":rule.type,"op":"add"}}, zmq.SNDMORE)
        #end
        client.route.send_json({"op":"batch-rule-end","data":{}})