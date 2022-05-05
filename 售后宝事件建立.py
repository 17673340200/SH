import json
import time
import requests
#导入授权认证
import entoken
class Event_shb():
        # 获取授权
        def Have_token(self):
            try:
                Acces = entoken.token().token_have()
            except:
                Acces="ERR"
            return Acces
        def API_Creat_File(self):
            Acces=Event_shb().Have_token()
            i = 0
            while (Acces == "ERR"):
                time.sleep(10)
                i += 1
                print("重新获取授权{}次".format(i))
                Acces = Event_shb().Have_token()

            url="https://oapi.shb.ltd/service/file/upload_file?accessToken={}".format(Acces)
            #注意，文件必须上传multipartfile的类型，否则会无法创建附件
            files = {'file': open("1.jpg", 'rb')}
            res = requests.post(url=url, files=files).json()
            # 将获取的信息定为josn格式
            res = json.loads(res)
            # 返回创建后的id；
            return res['data']['fileId']

        def API_Creat_event(self):
            Acces=Event_shb().Have_token()
            i=0
            fileid=Event_shb().API_Creat_File()
            while(Acces == "ERR"):
                time.sleep(10)
                i+=1
                print("重新获取授权{}次".format(i))
                Acces = Event_shb().Have_token()
            url="https://oapi.shb.ltd/service/event/create_event?accessToken={}".format(Acces)
            # body 填入信息
            body = {
        "attribute": {
            "field_4loCHZxTB67KBOnV": "事件自定义字段选项1",
            "field_3cDNtpr33LznP8DL": "事件自定义字段选项2",
            "field_YnBanupRFl5xX6v8": "事件自定义字段选项3",
            "field_4EAUubfl748bHUT2": [f"{fileid}"],

            },
        "cusNo": "CUS11101",
        "cusName": "上海金桥信息股份有限公司",
        "address": "北京市朝阳区利泽西园315号楼2层",
        "lmName": "zhangzhi",
        "lmPhone": "17673340200",
        "templateId": "fe5958ed-9b01-11e9-8123-7cd30abca02e",
        "templateName": "客户报修",
        "productIds": ["28b0f79d3c67-11e8-9206-00163e304a25"],
        "autoDispatch": True
    }
            # 获取请求的信息
            res = requests.post(url=url, json=body).json()
            # 将获取的信息定为josn格式
            res = json.loads(res)
            print(res)
            print(f"创建成功！事件号为{res['data']}")
if __name__ == '__main__':
    #测试创建文件是否成功
    #Event_shb().API_Creat_File()

    Event_shb().API_Creat_event()