from elasticsearch import Elasticsearch


class ElkTask():
    def __init__(self):
        elk_addr = "http://123.56.9.150:9200/"
        self.es = Elasticsearch(elk_addr)
        self.es.cluster.health(request_timeout=10)
    def do_user_agent_reg(self,threshold,reg_string):
        try:
            res = self.es.count(body = {
                "query": {
                    "filtered": {
                        "query":  { "regexp": {
                            "logs.http_user_agent.raw": "%s"%(reg_string)
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
                            "logs.http_user_agent.raw": "*%s*"%(sub_string)
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
                            "logs.referer.raw": "%s"%(reg_string)
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
                            "logs.referer.raw": "*%s*"%(sub_string)
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
            print(res["count"])
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
                                            "logs.hostname.raw": "*%s*"%(sub_string)
                                        }
                                    },
                                    {
                                        "wildcard": {
                                            "logs.path.raw": "*%s*"%(sub_string)
                                        }
                                    },
                                ]
                            }},
                        "filter": { "term":  { "logs.source_type.raw": "RTR" }}
                    }

                }
            })
            print(res["count"])
            return res["count"] >= threshold
        except Exception,e:
            print(e)
            return False
            
elk = ElkTask()
#print elk.do_url_sub(100,"dtcontroller")
print elk.do_url_reg(100,"dt.*dt")
