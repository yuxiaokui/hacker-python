import socket
from multiprocessing import Pool
ports = [21,22,23,25,53,80,110,139,143,389,443,445,465,873,993,995,1080,1311,1723,1433,1521,3000,3001,3002,3306,3389,3690,4000,5432,5900,6379,7001,8000,8001,8080,8081,8888,9200,9300,9080,9090,9999,11211,27017]

def portcheck(target):
    ip, port = target.split(":")
    try:
        cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cs.settimeout(float(2.5))
        address=(ip, int(port))
        status = cs.connect_ex((address))
        if status == 0:
            print ip + ":" + port + ",",
    except Exception ,e:
        pass
        #print "error:%s" %e
    finally:
        cs.close()


if __name__ == '__main__':
    targets = []
    with open("ip.txt") as f:
        print "Port Scaning ..."
        for ip in f.readlines():
            for port in ports:
                targets.append(ip.strip() + ":" + str(port))
        print targets

        pool = Pool(20)
        results = pool.map(portcheck, targets)
        pool.close()
        pool.join()
        print "\nScan end"
