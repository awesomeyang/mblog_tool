'''
blog editor 
'''
import http.server as hs
import socketserver
import time
import os
import sys
import shutil
import json
from bs4 import BeautifulSoup
DATE=time.strftime('%Y-%m-%d',time.localtime(time.time()))
PORT = 8000
timec=time.time()
def handle_image(path,index):
    PATH=os.path.join('githubpage','images')                                      #处理图片文件
    if os.path.isfile(path):
        newname=str(int(timec))+str(index)+'.jpg'
        shutil.copyfile(path,os.path.join(PATH,newname))
        os.renames(path,os.path.join('images',newname))                           #处理完成后将本地图片文件名与page文件名统一方便更改                                
        return ['s',newname]                           
    else:
        return ['n']                               


def handlehtml(html,title="",change=0,id=0):                                             #使用*argc 和**argv 可以为传参带来很多方便
    chtml=BeautifulSoup(html,'html.parser')
    img=chtml.find_all('img')                
    for i in range(len(img)):                                                      #这里可能会有bug
        re=handle_image(img[i]['src'],i)
        #print("handle image %d complete"%(i))                                     #不能加载服务器文件夹之外的文件 预计解决方案直接打开html文件 问题无法返回200关闭页面
        if re[0]=='s':
            img[i]['src']=os.path.join('images',re[1])        
        elif re[0]=='n':
            pass
            '''mistake_store''' 
        else:
            pass
    try:
        complete_store(str(chtml),title=title,change=change,id=id)
    except:
         complete_store(str(chtml),title=title)
def complete_store(html,title="",change=0,id=0):
    if change==1:
        with open(os.path.join('outcome','rawpostdata.js'),'wb+') as f:
            data=f.read().decode().split(';')
            for i in data:
                ji=json.loads(i)
                if ji['postintro']['id']==argv['id']:
                    ji['post']['content']==html
            outcome=data.join(';')+';'
            boutcome=outcome.encode('utf-8')
            f.write(boutcome)
    else:
        if title=="":
            for i in sys.argv[2:]:
                title+=i
                title+=" "
        outcome={"postintro":{"id":timec,"title":title,"date":DATE},"post":{"id":timec,"content":html}}
        outcome=json.dumps(outcome)+";"
        boutcome=outcome.encode('utf-8')
        with open(os.path.join('outcome','rawpostdata.js'),'ab+') as f:  
            f.write(boutcome)
        with open(os.path.join('outcome','rawpostdata.js'),'rb+') as f:
            data=f.read().decode().split(';')
            data.pop(-1)
            with open(os.path.join('outcome','postdata.js'),'wb+') as f:
                outcome="var data=function(){ var data="+str(data)+";return data;}"
                boutcome=outcome.encode('utf-8')
                f.write(boutcome)
        shutil.copyfile(os.path.join('outcome','postdata.js'),os.path.join('githubpage','javascripts','postdata.js'))
class handle(hs.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type','text/plain')
        self.end_headers()        
        data=self.rfile.read(int(self.headers['content-length']))
        data.decode()
        try:
            changedata=json.loads(data)
            handlehtml(changedata['post']['content'],id=changedata['post']['id'],change=1)
            with open(os.path.join('outcome','temppostdata.js'),'w+') as f:
                f.truncate()
        except:
            handlehtml(data)
        raise KeyboardInterrupt

if __name__=='__main__':
    with socketserver.TCPServer(('localhost',PORT), handle) as httpd:                   
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()