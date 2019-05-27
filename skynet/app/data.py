#coding: utf-8

# import threading
#
# lock = threading.Lock()


#需要考虑并发情况
__global_data = {
    "_app":None,
    "_rep_stats_server":None,
    "_pub_rule_server":None,
    "_rep_misc_server":None,
    ##########################
    "plugins":[],
    "exec_tasks":{
        "exec_status":False,
        "exec_type":None,
        "exec_time":None,
        "exec_datetime":None
    }

}

def get_data_by_key(key):
    try:
        # if lock.acquire():
        return __global_data[key]
    except Exception,e:
        print(e)
        return None
def set_data_by_key(key,value):
    try:
        __global_data[key] = value
        # lock.release()
    except Exception,e:
        print(e)
