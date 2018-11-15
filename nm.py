# coding:utf-8
import socket
import threading
import time
def get_ip_status(ip, port):

    print(port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(0.5)
    try:
        server.connect((ip, port))
        print('{0} port {1} is open'.format(ip, port))
        return True
    except Exception as err:

        #print('{0} port {1} is not open'.format(ip, port))
        return False
    finally:
        server.close()
        return False


def quicknmap(host):

    host=socket.gethostbyname(host)
    for j in range(0,82):
        threads = []

        for port in range(0, 800):
            t = threading.Thread(target=get_ip_status, args=(host, port+j*800))

            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()



quicknmap('localhost')