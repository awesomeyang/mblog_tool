'''
markdown transformer by maxwell yang blog
'''
import markdown
import os

filelist=os.listdir()
for i in filelist:
    if i.endswith('.md',mode="r",encoding="utf-8"):
        mdfile=open(i)
        mdfiledata=mdfile.read()
        md=markdown.markdown(mdfiledata)
        
    else pass
