import sys
import os
import webbrowser
import time
import json
import sqlite3
import shutil
import handlef
from webtext import postdata
'''
maxwellyang github blog 命令行工具
init 初始化git与个人资料
state 查看个人资料
new  新建blog文章 
    blog文章 
        markdown 
        webtext 'this is title'
change 更改文章内容
    markdown [id]
    [id]
upload 更新blog
list 查看文章列表
help 使用帮助
'''


command=sys.argv
if command[1]=='init':
    print("欢迎使用maxwellblog 命令行工具")
    with open('userdata.json','r',encoding='utf-8') as f:                             
        j=json.loads(f.read())     
    sql=sqlite3.connect(os.path.join('outcome','data.db'))                         #sqlite setting
    s='''CREATE TABLE ARTICAL(
        ID INT PRIMART KET NOT NULL,
        TITLE TEXT NOT NULL,
        DATE TEXT NOT NULL,
        INTRO TEXT ,
        CONTENT TEXT NOT NULL
    );
    '''
    cur=sql.cursor()
    cur.execute(s)
    sql.commit()
    sql.close()
    os.system('git init %s'%(os.path.join('.','githubpage')))                      #git设置
    os.chdir('githubpage')                                                      
    os.system('git config --global push.default current')
    os.system('git add *')
    os.system("git commit -m firstcommit")
    os.system('git remote add github %s'%(j['githuburl']))    
    os.system('git push github --all -f')
                                                                                  #暂时未实现自动生成ssh的功能 姓名自我介绍功能暂时写死
 
    
elif command[1]=='state':
    with open('userdata.json','r',encoding='utf-8') as f:
        j=json.loads(f.read())
        print('username:%s \nintroduction:%s\neducation:%s\naward:%s\n '%(j['username'],j['introduction'],j['education'],j['award']))
elif command[1]=='new':
    if command[2]=='markdown':
        os.system("python handlemd.py new")
    elif command[2]=='webtext':
        webbrowser.open('http://localhost:8000')     
        os.system("python webtext.py --title %s"%(command[4]))                #title格式 'this is a title'
elif command[1]=='change':
    if command[2]=='markdown':
        os.system('python handlemd.py change %s'%(command[3]))                     #用第一个md文件替换内容
    else:
        os.system('python webchange.py %s'%(command[2]))                           #用富文本打开的方式替换文本
        try:
            webbrowser.get('chrome').open('http://localhost:8000')
        except :
            print('更该文章需要使用chrome浏览器')
        else:
            os.system("python webtext.py") 
elif command[1]=='upload':
    try:
        os.chdir('githubpage')
        os.system('git commit -am %d'%(int(time.time())))
        os.system('git push github --all -f')
    except:
        print('init 失败了')                                        
elif command[1]=='list':
    try:
        con=sqlite3.connect(os.path.join('outcome','data.db'))
        cur=con.cursor()
        index=0
        for i in cur.execute('SELECT * FROM ARTICAL;'):
            print("%s    %s"%(i[0],i[1]),end='\n')
            index+=1
        if index==0:
            print('目前没有写过blog哦')
    except:
        print('init 失败了') 
elif command[1]=='delete':
    try:
        if(command[2]=="*"):
             if(input('确认要删除所有博客吗?(y/n)')=='y'):
                 cur.execute('DELETE  FROM ARTICAL')
        else:
            con=sqlite3.connect(os.path.join('outcome','data.db'))
            cur=con.cursor()
            if(input('确认要删除 %s吗？(y/n)'%(''.join(command[2])))=='y'):
                cur.execute('DELETE FROM ARTICAL WHERE ID=:id',{'id':''.join(command[2])})
        con.commit()
        con.close()
        postdata()
    except Exception as e:
        print(e) 
elif command[1]=='preview':
    webbrowser.open(os.path.join('githubpage','index.html'))
elif command[1]=='help':
    data='''
maxwellyang github blog 命令行工具
init 初始化git与个人资料
state 查看个人资料
new  新建blog文章 
     blog文章 
        markdown 
        webtext 'this is title'
change 更改文章内容
    markdown [id]  使用markdown文件更改内容
    [id]           使用webtext更改内容使用chrome浏览器
upload 更新blog
list 查看文章列表
help 使用帮助
'''
    print(data,end="")
else: print("没有这个命令啦",end='\n')


