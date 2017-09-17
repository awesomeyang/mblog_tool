import sys
import os
import webbrowser
import time
import json
import shutil
'''
maxwellyang github blog 命令行工具
init 初始化git与个人资料
state 查看个人资料
new  新建blog文章 
    -p blog文章 
    -b 读书简笔 格式 图片加文字
change 更改文章内容
upload 更新blog
list 查看文章列表
help 使用帮助
'''


command=sys.argv
if command[1]=='init':
    print("欢迎使用maxwellblog 命令行工具")
    with open('userdata.json','r',encoding='utf-8') as f:                             #git设置
        j=json.loads(f.read())                                       
    os.system('git init %s'%(os.path.join('.','githubpage')))
    os.chdir('githubpage')
    os.system('git config --global push.default current')
    os.system('git add *')
    os.system("git commit -m firstcommit")
    os.system('git remote add github %s'%(j['githuburl']))    
    os.system('git push github --all -f')
    print('如果失败请先按照教程完成第二步')                                          #暂时未实现自动生成ssh的功能 姓名自我介绍功能暂时写死
 
    
elif command[1]=='state':
    with open('userdata.json','r',encoding='utf-8') as f:
        j=json.loads(f.read())
        print('username:%s \nintroduction:%s\neducation:%s\naward:%s\n '%(j['username'],j['introduction'],j['education'],j['award']))
elif command[1]=='new':
    if command[2]=='-p':
        if command[3]=='-m':
            os.system("python handlemd.py")
        elif command[3]=='-t':
            webbrowser.open('http://localhost:8000')     
            os.system("python webtext.py --title %s"%(command[4]))      #title格式 'this is a title'
    elif command[1]=='-b':
        pass
elif command[1]=='change':
    pass                                                                #内容更改目前需要手动完成
elif command[1]=='upload':
    shutil.copyfile(os.path.join('outcome','postdata.js'),os.path.join('githubpage','javascripts','postdata.js'))
    os.chdir('githubpage')
    os.system('git commit -am %d'%(int(time.time())))
    os.system('git push github --all -f')                                        #master->master is rejucted!! figour out the reason!!
elif command[1]=='list':
    pass
elif command[1]=='help':
    data="欢迎使用mawellyang githubblog命令行工具\n init 初始化git与个人资料\n state 查看个人资料\n new  新建blog文章\n    -p blog文章 \n    -b 读书简笔\n change 更改文章内容\n list 查看文章列表\n help 使用帮助"
    print(data,end="")
else: print("没有这个命令啦",end='\n')


