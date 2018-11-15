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
        # 我他妈

        delay[where] = eval(text)['minimum']
    #except TencentCloudSDKException as err:
        #print(err)
    except :
        print(where,'无法测量')
        wherelist = ["ap-guangzhou", "ap-shanghai", "ap-beijing", "ap-chengdu"]
        for i in wherelist:
            delay[i] = -1.0



cred = credential.Credential("AKID60f7TqOta2GG1ZnC7oGTQ7ankRu8etQj", "EE4g4E9qJZfXBalhU3NREn58vT8XgZDb")
httpProfile = HttpProfile()
httpProfile.endpoint = "scf.tencentcloudapi.com"
wherelist = ["ap-guangzhou", "ap-shanghai", "ap-beijing", "ap-chengdu"]


db = pymysql.connect(host="localhost", user="root", password="", db="ip", port=3306)
cur = db.cursor()
#sql = "select ip,site from rootip"
sql = "SELECT ip,site FROM `ipdelay` WHERE `ap-shanghai` = -1 ORDER BY `ap-beijing` ASC "
cur.execute(sql)
result = cur.fetchall()
print(result)

i = 0
while i < len(result):
    Threads = []
    ip = str(IPy.IP(result[i][0]))
    for where in wherelist:
        t = threading.Thread(target=send_resquest, args=(httpProfile, where, ip, 30, 80))
        # send_resquest(httpProfile=httpProfile, where=where, ip="www.pronhub.com")
        Threads.append(t)
    for t in Threads:
        t.start()
    for t in Threads:
        t.join()
    print(ip, result[i][0],result[i][1])
    print(delay)
    #sql = "insert into ipdelay value (%d,%s,%f,%f,%f,%f)"
    sql="UPDATE `ipdelay` SET `ap-guangzhou`='%f',`ap-shanghai`='%f',`ap-beijing`='%f',`ap-chengdu`='%f' WHERE `site` like '%s'"
    try:
        '''
        cur.execute(sql % (
            result[i][0], str('\'' + result[i][1] + '\''), delay['ap-guangzhou'], delay['ap-shanghai'],
            delay['ap-beijing'], delay['ap-chengdu']))
            '''
        cur.execute(sql%(delay['ap-guangzhou'], delay['ap-shanghai'],
            delay['ap-beijing'], delay['ap-chengdu'],str(result[i][1])))
        db.commit()
    except Exception as e:
        print(e)

        db.rollback()
    i = i + 1

db.close()
