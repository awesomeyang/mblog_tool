'''
blog editor 
'''
import http.server as hs
import socketserver
import time
import os
import sys
import shutil
from bs4 import BeautifulSoup
DATE=time.strftime('%Y-%m-%d',time.localtime(time.time()))
PORT = 8000
timec=time.time()
def handle_image(path,index):
    PATH=os.path.join(os.getcwd(),'image')
    if os.path.isfile(path):
        newname=str(int(timec))+str(index)+'.jpg'
        shutil.copyfile(path,os.path.join(PATH,newname))                                
        return ['s',newname]                           
    else:
        return 'n'                               


def handlehtml(html):
    chtml=BeautifulSoup(html,'html.parser')
    img=chtml.find_all('img')
    print(len(img))                  
    for i in range(len(img)):
        print(img[i]['src'])                                                       #这里可能会有bug
        re=handle_image(img[i]['src'],i)
        print("handle image %d complete"%(i))
        if re[0]=='s':
            img[i]['src']=os.path.join('image',re[1])        
        elif re=='m':
            pass
            '''mistake_store''' 
        else:
            pass
    complete_store(str(chtml))

def complete_store(html):
    title=""
    for i in sys.argv[2:]:
        title+=i
        title+=" "
    outcome='''{"postintro":{"id":%d,"title":"%s","date":"%s"},"post":{"id":%d,"content":"%s"}};'''%(timec,title,DATE,timec,html)
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
class handle(hs.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type','text/plain')
        self.end_headers()        
        data=self.rfile.read(int(self.headers['content-length']))
        data.decode()
        handlehtml(data)
        
        raise KeyboardInterrupt
        

if __name__=='__main__':
    with socketserver.TCPServer(('localhost',PORT), handle) as httpd:
        print('serving....',end='\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()