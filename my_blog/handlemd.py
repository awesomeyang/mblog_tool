'''
markdown transformer by maxwell yang blog
'''
import markdown
import os
from webtext import complete_store 

if __name__=='__main__':
    filelist=os.listdir()
    index=0
    for i in filelist:
        if i.endswith('.md'):
            name=i.strip('.md')
            mdfile=open(i,'r',encoding='utf-8')
            mdfiledata=mdfile.read()
            md=markdown.markdown(mdfiledata)
            complete_store(md,title=name)
            mdfile.close()
            index+=1
            print('已处理完 %s,总共处理md文件 %d个'%(i,index))
    if index==0:
        print('no markdown file to handle!')
