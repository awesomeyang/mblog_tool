import sys
import os
import webbrowser
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
    pass
elif command[1]=='state':
    pass
elif command[1]=='new':
    if command[2]=='-p':
        if command[3]=='-m':
            pass
        elif command[3]=='-t':
            print (command[3],end='\n')
            webbrowser.open('http://localhost:8000')     
            os.system("python webtext.py --title %s"%(command[4]))      #title格式 'this is a title'
             
    elif command[1]=='-b':
        pass
elif command[1]=='change':
    pass
elif command[1]=='upload':
    pass
elif command[1]=='list':
    pass
elif command[1]=='help':
    data="欢迎使用mawellyang githubblog命令行工具\n init 初始化git与个人资料\n state 查看个人资料\n new  新建blog文章\n    -p blog文章 \n    -b 读书简笔\n change 更改文章内容\n list 查看文章列表\n help 使用帮助"
    print(data,end="")
else: print("没有这个命令啦",end='\n')


