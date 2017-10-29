'''
markdown transformer by maxwell yang blog
用马克飞象一定要导出md文件才可以
'''
import markdown
import os
import sys
from webtext import handlehtml
import re
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
from latex import latextoImage

class myextension(Extension):
    def extendMarkdown(self,md,md_globals):
        md.registerExtension(self)
        Myprocess=myprocess()
        md.preprocessors.add('mypro',Myprocess,'<normalize_whitespace')

class myprocess(Preprocessor):                              #最佳解决方案改写markdown extension 只支持一行写一个latex公式
    def run(self,lines):
        latex=[]
        for i in range(len(lines)):
            m=re.findall("\$(.*)\$",lines[i])
            if m!=[]:
                for l in m: 
                    latex.append(l)
                    lines[i].replace(l,"<img scr='images/mdimage{id}.png'>".format(id=i))
        la=latextoImage(latex)   
        return lines                          #有可能出错必须返回新的list

if __name__=='__main__':
    filelist=os.listdir()
    index1=index2=0
    for i in filelist:
        if i.endswith('.md') and i!="README.md":
            name=i.strip('.md')
            mdfile=open(i,'r',encoding='utf-8')
            mdfiledata=mdfile.read()
            configs={}
            md=markdown.markdown(mdfiledata,output_format='html5',extensions=[myextension(configs=configs)])
            if sys.argv[1]=='change':
                handlehtml(md,title=name,change=1,id=sys.argv[2])
                break   
            else:
                pass
                handlehtml(md,title=name)
            mdfile.close()
            index1+=1
            #os.remove(i)                                              #处理完删除文件
            print('已处理完 %s,总共处理md文件 %d个'%(i,index))
        elif i.endswith('.html') and i!='index.html':                   #根据config 确定是否要使用base64编码显示图片 
            name=i.strip('.html') 
            htmlfile=open(i,'r',encoding='utf-8')
            filedata=htmlfile.read()
            if sys.argv[1]=='change':
                handlehtml(filedata,title=name,change=1,id=sys.argv[2])
                break   
            else:
                handlehtml(filedata,title=name)
            htmlfile.close()
            index2+=1
            print('已处理完 %s,总共处理md文件 %d个'%(i,index2))
    if index==0:
        print('no markdown or html file to handle!')
