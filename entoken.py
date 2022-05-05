import hashlib
import json
import MySQLdb
import requests

# from shouhoubao import timestamp

import time
timestamp=int(round(time.time()*1000))

class token():

    #获取token
    def get_token(self):
        url="https://oapi.shb.ltd/service/auth/get_access_token"
        appkey="shbdzpnu3mnm3hghyc"
        appSecret="0e29c834e5f26ef257d50e13c1314a5e23e04f98d5f72ad0"
        vcode_value=str(str(appSecret)+"_"+str(timestamp))
        m=hashlib.md5()
        b=vcode_value.encode(encoding="utf-8")
        m.update(b)
        vcode_value=m.hexdigest()
        body={
        "appKey":"shbdzpnu3mnm3hghyc",
        "timestamp":timestamp,
        "verifyCode":vcode_value,
    }
        res=requests.post(url=url,json=body).json()
        res=json.loads(res)
        print(res)
        acces_token=res['data']['access_token']
        acces_token=str(acces_token)
        lasttimestamps =res['data']['expire_time']
        if(acces_token!=None):
            token.inter_table(acces_token=acces_token,timestamp=timestamp,lasttimestamps=lasttimestamps)
        else:
            print("获取失败")
        return acces_token
    #判断token是否过期，没过期则从数据库中获取
    def token_have(self):
        sql1 = '''
                     SELECT lasttimestamps FROM miyao  WHERE id = 1;
             '''
        sql2 = '''
             SELECT makey FROM  miyao WHERE id = 1;
             '''
        lasttime = token.select_table(sql1)
        lasttime=int(lasttime)
        if (lasttime > timestamp):
            acces_token=token.select_table(sql2)
        else:
            acces_token=token.get_token(self)
        return acces_token
#创建数据库，把授权token存到数据库中
    def create_table(self):
        conn = MySQLdb.connect("localhost",user='admin',passwd='admin',db='shbdb',charset='utf8')
        c = conn.cursor()
        # 数据库调用语句
        sql = '''
                                     CREATE TABLE  miyao
                                     (id INT NOT NULL,
                                     makey VARCHAR(100) NOT NULL ,
                                     timestamps VARCHAR(100) NOT NULL,
                                     lasttimestamps VARCHAR(100) NOT NULL
                                     );'''
        c.execute(sql)
        conn.commit()  # 提交数据库操作
        conn.close()
    # 把获取的秘钥填入数据库中
    def inter_table(acces_token,timestamp,lasttimestamps):
        acces_token=str(acces_token)
        timestamp=timestamp
        lasttimestamps=lasttimestamps
        conn = MySQLdb.connect("localhost",user='admin',passwd='admin',db='shbdb',charset='utf8')
        c = conn.cursor()
        # 数据库调用语句
        # sql = '''
        #             insert into miyao(id,key,timestamps,lasttimestamps)
        #             values (1,"%s","%s","%s")
        #                    '''
        sql='''
                 UPDATE miyao SET  makey='%s',timestamps='%s',lasttimestamps='%s' WHERE id =1;
         '''
        c.execute(sql %(acces_token,timestamp,lasttimestamps))
        conn.commit()  # 提交数据库操作
        conn.close()
    #数据库读取
    def select_table(sql):
        conn=MySQLdb.connect("localhost",user='admin',passwd='admin',db='shbdb',charset='utf8')
        c=conn.cursor()
        # sql='''
        #         SELECT lasttimestamps FROM miyao WHERE id is 1;
        # '''
        c.execute(sql)
        c=c.fetchone()
        c=c[0]
        conn.close()
        return c
#测试逻辑是否正常
if __name__ == '__main__':
    s=token().get_token()
    d=token().token_have()
    print(d)
    print(s)