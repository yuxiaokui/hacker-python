#coding:utf-8
import threading
import queue
import dns.resolver
import time
import itertools as its
import logging
import pymongo


client = pymongo.MongoClient(host='xxx', port=27017)
db = client.scanner

logging.basicConfig(filename='xk.log', filemode='w', level=logging.DEBUG)
queuelist = queue.Queue(10000)

target =  ['baidu.com','qq.com','163.com']

black_ip = []



print("泛域名IP处理中...")
for i in target:
    d = "xi4okv_fuckdomain." + i 
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["8.8.8.8","114.114.114.114","9.9.9.9"]
        resolver.lifetime = resolver.timeout = 5
        answers = resolver.query(d)
        for i in answers:
            ip = i.address
            black_ip.append(ip)
    except Exception as e:
        pass
print("泛域名IP处理完成！开始子域名Fuzz...")


class Produce(threading.Thread):
    def __init__(self):
        super(Produce,self).__init__()
        self.subdomains = []
        self.elements = []
        self._load_subname("subnames.txt", self.subdomains)
        self._load_subname("elements.txt", self.elements)


    def _load_subname(self,filename,parm):
        with open(filename) as f:
            for line in f:
                sub = line.strip()
                parm.append(sub)

    def run(self):

        for subname in self.subdomains:  #字典破解
            if not queuelist.full():
                queuelist.put(subname)
                time.sleep(0.01)
            else:
                print ("Queue is full!")
                time.sleep(10)

        self.elements += list("1234567890abcdefghijklmnopqrstuvwxyz.-") #迭代破解
        for i in range(1,4):
            r = its.product(self.elements,repeat=i)
            for k in r:
                subname = "".join(k)
                if not queuelist.full():
                    queuelist.put(subname)
                    time.sleep(0.05)
                else:
                    print ("Queue is full!")
                    time.sleep(10)


class Consume(threading.Thread):
    def __init__(self):
        super(Consume,self).__init__()
        self.target = target

    def fuck(self,domain):
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ["8.8.8.8","114.114.114.114","9.9.9.9"]
            resolver.lifetime = resolver.timeout = 3
            answers = resolver.query(domain)
            ip = answers[0].address
            if ip not in black_ip:
                print(domain)
                try:
                    db.domains.insert_one({"domain":domain,"ip":ip,'time':time.time()})
                except Exception as e:
                    print(e)
                logging.warning(domain+":"+ip)
        except Exception as e:
            pass

    def run(self):
        while True:
            if not queuelist.empty():
                domain = queuelist.get()
                for i in self.target:
                    self.fuck(domain + "." + i)


if __name__ == "__main__":
    
    for server_num in range(0, 1):
        server = Produce()
        server.start()


    for customer_num in range(0, 100):
        customer = Consume()
        customer.start()
        
        
