'''
change content with textextre
'''
import sys
import os
import json
if __name__=='__main__':
    id=sys.argv[1]
    with open(os.path.join('outcome','rawpostdata.js'),'rb+') as f:
        f=f.read().decode().split(';')
        f.pop(-1)
        for i in f:
            ji=json.loads(i)
            if ji['post']['id']==id:
                with open(os.path.join('outcome','temppostdata.js'),'wb+') as pf:
                    outcome='var data=function(){ var data='+json.dumps(i)+';return data}'
                    boutcome=outcome.encode('utf-8')
                    pf.write(boutcome)
                break
            
                    
