import json
import threading

import IPy
import pymysql
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.scf.v20180416 import scf_client, models

# 全局变量
delay = {}
wherelist = ["ap-guangzhou", "ap-shanghai", "ap-beijing", "ap-chengdu"]
for i in wherelist:
    delay[i] = -1.0


def send_resquest(httpProfile, where, ip, num, port):
    try:

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = scf_client.ScfClient(cred, where, clientProfile)

        req = models.InvokeRequest()
        req.FunctionName = 'dotcpping'
        # req.InvocationType='Event'

        req.LogType = 'Tail'
        req.ClientContext = '{"ip":' + '\"' + ip + '\"' + ',"num":' + str(num) + ',"port":' + str(port) + '}'
        resp = client.Invoke(req)  # 发送了请求，我觉得还是要异步，同步就算有结果也会超时，下一步工作，同步只能ping 10次

        text = json.loads(resp.to_json_string())['Result']['Log'].split('\n')[0]
        print(where, " old ", delay[where], ' now  ', eval(text)['minimum'])
        print(eval(text)['conn_times'])
        # 我他妈


        delay[where] = eval(text)['minimum']
    #except TencentCloudSDKException as err:
        #print(err)
    except :
        print(where,'无法测量')
        wherelist = ["ap-guangzhou", "ap-shanghai", "ap-beijing", "ap-chengdu"]
        for i in wherelist:
            delay[i] = -1.0


def distance(dela):
    db = pymysql.connect(host="localhost", user="root", password="", db="ip", port=3306)
    cur = db.cursor()
    sql='select * from ipdelay'
    cur.execute(sql)
    result=cur.fetchall()
    max=1000000000000000000000
    maxindex=-1
    for i in range(0,len(result)):
        if result[i][3]==-1:
            continue
        sum=(result[i][2]-dela["ap-guangzhou"])**2+(result[i][3]-dela["ap-shanghai"])**2+(result[i][4]-dela["ap-beijing"])**2+(result[i][5]-dela["ap-chengdu"])**2
        if sum<max:
            max=sum
            maxindex=i


    sql="select * from rootip where site like %s"
    cur.execute(sql%(str('\''+result[maxindex][1]+'\'')))
    print(cur.fetchall())
    return cur.fetchall()

cred = credential.Credential("AKID60f7TqOta2GG1ZnC7oGTQ7ankRu8etQj", "EE4g4E9qJZfXBalhU3NREn58vT8XgZDb")
httpProfile = HttpProfile()
httpProfile.endpoint = "scf.tencentcloudapi.com"
ip='www.baidu.com'
Threads=[]
for where in wherelist:
    t = threading.Thread(target=send_resquest, args=(httpProfile, where, ip, 30, 80))
    # send_resquest(httpProfile=httpProfile, where=where, ip="www.pronhub.com")
    Threads.append(t)
for t in Threads:
    t.start()
for t in Threads:
    t.join()
print(delay)
do=1
for i in wherelist:
    if delay[i]==-1 or delay[i]==0:
        do=0
if do==1:
    print(distance(delay))
else:
    print("测不了")
