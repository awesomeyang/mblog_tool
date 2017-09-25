import sys
import os
import webbrowser
import time
import json
import shutil
import handlemd
'''
maxwellyang github blog 命令行工具
init 初始化git与个人资料
state 查看个人资料
new  新建blog文章 
    post blog文章 
        markdown 
        webtext 'this is title'
    book 读书简笔 格式 图片加文字
change 更改文章内容
    markdown [id]
    [id]
upload 更新blog
list 查看文章列表
help 使用帮助
'''
'''
数据传递格式
{
    postintro:{
        id:546,
        title:'',
        date:'',
        #intro：'' 简介功能暂未实现
    }
    post:{
        id:546,
        content:''
    }
}
postdata.js
可用js文件返回数据
rawpostdata.js
原始数据文件
格式{};{};{}
pako压缩功能暂未开发
'''

command=sys.argv
if command[1]=='init':
    print("欢迎使用maxwellblog 命令行工具")
    with open('userdata.json','r',encoding='utf-8') as f:                             #git设置
        j=json.loads(f.read())                                       
    os.system('git init %s'%(os.path.join('.','githubpage')))
    os.chdir('githubpage')                                                       #githubpage 中有.git 文件所以不能push
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
    if command[2]=='post':
        if command[3]=='markdown':
            os.system("python handlemd.py")
        elif command[3]=='webtext':
            webbrowser.open('http://localhost:8000')     
            os.system("python webtext.py --title %s"%(command[4]))                #title格式 'this is a title'
    elif command[1]=='book':
        pass
elif command[1]=='change':
    if command[2]=='markdown':
        os.system('python handlemd.py change %s'%(command[3]))                     #用第一个md文件替换内容
    else:
        os.system('python webchange.py %s'%(command[2]))                           #用富文本打开的方式替换文本
        webbrowser.open('http://localhost:8000')     
        os.system("python webtext.py") 
elif command[1]=='upload':
    os.chdir('githubpage')
    os.system('git commit -am %d'%(int(time.time())))
    os.system('git push github --all -f')                                        #master->master is rejucted!! figour out the reason!!
elif command[1]=='list':
    with open(os.path.join('outcome','rawpostdata.js'),'rb+') as f:
        f=f.read().decode().split(';')
        f.pop(-1)
        for i in f:
            data=json.loads(i)
            print("%s    %s"%(data['postintro']['id'],data['postintro']['title']),end='\n')
elif command[1]=='help':
    data='''
maxwellyang github blog 命令行工具
init 初始化git与个人资料
state 查看个人资料
new  新建blog文章 
    post blog文章 
        markdown 
        webtext 'this is title'
    book 读书简笔 格式 图片加文字
change 更改文章内容
    markdown [id]
    [id]
upload 更新blog
list 查看文章列表
help 使用帮助
'''
    print(data,end="")
else: print("没有这个命令啦",end='\n')


