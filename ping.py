import multiprocessing
import socket
import time
from functools import partial

import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt

myList = []


def process_ping(woc, ip):
    ip = socket.gethostbyname(ip)
    processlist = []
    try:
        i = 0
        while i < 10:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            i = i + 1
            s.settimeout(0.5)

            start = time.time()
            s.connect((ip, 80))

            end = time.time()
            s.shutdown(socket.SHUT_RD)
            processlist.append((end - start) * 1000)


    except socket.error as e:

        pass

    return processlist


def draw_hist(myList, fit_alpha, fit_loc, fit_beta, Title, Xlabel, Ylabel, Xmin, Xmax, Ymin, Ymax):
    plt.hist(x=myList, bins=100, density=True)
    plt.xlabel(Xlabel)
    plt.xlim(Xmin, Xmax)
    plt.ylabel(Ylabel)
    plt.ylim(Ymin, Ymax)
    plt.title(Title)
    plt.grid(True)
    x = np.arange(0, 500, 0.01)
    y = stats.gamma.pdf(x, fit_alpha, fit_loc, fit_beta)
    plt.plot(x, y, 'r')
    plt.show()


########线程跑啊
if __name__ == '__main__':
    num = 5000  ##测的次数
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    xs = range(int(num / 10))


    ip = 'www.baidu.com'

    start = time.time()
    tmp = pool.map(partial(process_ping, ip=ip), xs)
    pool.close()
    pool.join()
    end = time.time()

    for i in range(len(tmp)):
        myList = myList + tmp[i]
    print((end - start) * 1000, len(myList))
    fit_alpha, fit_loc, fit_beta = stats.gamma.fit(myList)

    print(fit_alpha, fit_loc, fit_beta)
    draw_hist(myList, fit_alpha, fit_loc, fit_beta, 'distru', 'delay', 'time', 0, 500, 0, 0.2)  # 直方图展示
