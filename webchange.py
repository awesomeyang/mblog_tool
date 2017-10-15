'''
change content with textextre
'''
import sys
import os
import json
import sqlite3
if __name__=='__main__':
    id=sys.argv[1:]
    con=sqlite3.connect(os.path.join('outcome','data.db'))
    cur=con.cursor()
    try:
        sql=cur.execute("SELECT * FROM ARTICAL WHERE ID=?",(id[0],)).fetchone()
        jsondata={'id':sql[0],'title':sql[1],'date':sql[2],'intro':sql[3],'content':sql[4]}
        with open(os.path.join('outcome','temppostdata.js'),'w+') as f:
            outcome=" var data="+json.dumps(jsondata)+";"           
            f.write(outcome)
    except Exception as e:
        print('不存在这个id!')
    finally:
        con.commit()
        con.close()                    