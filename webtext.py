'''
blog editor 
包含主函数
'''
import http.server as hs
import socketserver
import time
import os
import sys
import base64
import shutil
import sqlite3
import json
from bs4 import BeautifulSoup
DATE=time.strftime('%Y-%m-%d',time.localtime(time.time()))
PORT = 8000
timec=int(time.time())


def postdata():                                                                 #完成postdata文件复制
    con=sqlite3.connect(os.path.join('outcome','data.db'))
    cur=con.cursor()
    outcome=""
    for i in cur.execute('SELECT * FROM ARTICAL;'):
        outcome+=json.dumps({"id":i[0],"title":i[1],"date":i[2],"intro":i[3],"content":i[4]})+","
    boutcome="var data=["+outcome+"];"
    with open(os.path.join('outcome','postdata.js'),'w+') as f:
        f.write(boutcome)
    shutil.copyfile(os.path.join('outcome','postdata.js'),os.path.join('githubpage','javascripts','postdata.js'))

def handle_image(path,index):
    PATH=os.path.join('githubpage','images')                                      #处理图片文件
    if os.path.isfile(path):
        newname=str(timec)+str(index)+'.jpg'
        shutil.copyfile(path,os.path.join(PATH,newname))
        os.renames(path,os.path.join('images',newname))                           #处理完成后将本地图片文件名与page文件名统一方便更改                                
        return ['s',newname]                           
    else:
        print('图片不存在')
        return ['n']                               


def handlehtml(html,title="",change=0,id=0):                                             #使用*argc 和**argv 可以为传参带来很多方便
    chtml=BeautifulSoup(html,'html.parser')
    img=chtml.find_all('img')                
    for i in range(len(img)):  
        if img[i]['src'].startswith('data'):                                          #处理base64格式图片
            PATH=os.path.join('images','base64image'+str(i)+'.png')
            b64=img[i]['src'].replace('data:image/png;base64,','')
            ba64=base64.b64decode(b64)
            with open(PATH,'wb') as f:
                f.write(ba64)
            re=handle_image(PATH,i)
        else:                                                                          #这里可能会有bug
            re=handle_image(img[i]['src'],i)
            #print("handle image %d complete"%(i))                                     #不能加载服务器文件夹之外的文件 图片文件需要容易复制到images文件夹中
        if re[0]=='s':
            img[i]['src']=os.path.join('images',re[1])        
        elif re[0]=='n':
            pass
            '''mistake_solve''' 
        else:
            pass
    
    try:
        complete_store(str(chtml),title=title,change=change,id=id)
    except:
         complete_store(str(chtml),title=title)
def complete_store(html,title="",change=0,id=0):
    if change==1:
        con=sqlite3.connect(os.path.join('outcome','data.db'))
        cur=con.cursor()
        cur.execute('UPDATE ARTICAL SET CONTENT=:content WHERE ID=:id;',{'content':html,'id':id})
        con.commit()
        con.close()
        postdata()
        with open(os.path.join('outcome','temppostdata.js'),'w+') as f:
            f.write("var data={'content':''}")
    else:
        if title=="":
            for i in sys.argv[2:]:
                title+=i
                title+=" "
        outcome={"id":timec,"title":title,"date":DATE,"intro":"","content":html}
        boutcome=json.dumps(outcome)
        con=sqlite3.connect(os.path.join('outcome','data.db'))
        cur=con.cursor()
        cur.execute("INSERT INTO ARTICAL  VALUES(:id,:title,:date,:intro,:content);",outcome)
        con.commit()
        con.close()
        postdata()
        
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
        data=data.decode()
        try:
            changedata=json.loads(data)
            handlehtml(changedata['content'],id=changedata['id'],change=1)             #changed
        except:
            handlehtml(data)
        raise KeyboardInterrupt

if __name__=='__main__':
    with socketserver.TCPServer(('localhost',PORT), handle) as httpd:                   
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()