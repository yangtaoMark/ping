import json
import threading
import time

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.scf.v20180416 import scf_client, models

# 全局变量
delay = {}
wherelist = ["ap-guangzhou", "ap-shanghai", "ap-chengdu", "ap-beijing"]


def send_resquest(httpProfile, where, ip, num):
    try:

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = scf_client.ScfClient(cred, where, clientProfile)

        req = models.InvokeRequest()

        req.FunctionName = 'ping'
        # req.InvocationType='Event'

        req.LogType = 'Tail'
        req.ClientContext = '{"ip":' + '\"' + ip + '\",\"num\":' + str(num) + '}'
        resp = client.Invoke(req)
        data, success = eval(json.loads(resp.to_json_string())['Result']['RetMsg'])

        print(data,success)

        # 我他妈


    except TencentCloudSDKException as err:
        print(err)


cred = credential.Credential("AKID60f7TqOta2GG1ZnC7oGTQ7ankRu8etQj", "EE4g4E9qJZfXBalhU3NREn58vT8XgZDb")
httpProfile = HttpProfile()
httpProfile.endpoint = "scf.tencentcloudapi.com"
ip = 'www.baidu.com'
num = 5000
Threads = []
start=time.time()
for where in wherelist:
    t = threading.Thread(target=send_resquest, args=(httpProfile, where, ip, num))

    Threads.append(t)
for t in Threads:
    t.start()
for t in Threads:
    t.join()
end=time.time()
print((end-start)*1000,'s')