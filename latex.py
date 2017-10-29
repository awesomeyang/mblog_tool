'''
handle Latex function
'''
import os
import sys
import requests
def morerequest():
    if fail[0]['text'] !="":                                                                                 #若有失败的例子重复请求 通过config配置
        for i in range(100):
            for t in fail:
                re=requests.post(url[2].format(name=imagename),cookies=cookies,data={'editorvalue':t['text']})
                image=requests.get(url[3].format(name=imagename),cookies=cookies)
                if re.status_code==200 and image.status_code==200:
                    with open(os.path.join('images','mdimage'+t['id']+'.png'),'wb+') as f:
                        f.write(image)
                        break
                if i==99:
                    print('网络出问题啦')
        
def vali(data):
    data=list(data)
    if data[1]=='0':
        return ''.join(data[4:10])
    else:
        print('输入格式出错,请查看帮助改进格式')
        return 0
def store(index,data):
    try:
        with open(os.path.join('images','mdimage'+str(index)+'.png'),'wb') as f:
            f.write(data)
    except IOError:
        print(3)
def latextoImage(text):
    url=('https://www.latex4technics.com', #cookies
        'https://www.latex4technics.com/includes/f_during.php?L4tid=&mrmode=1', #[0,name]
        'https://www.latex4technics.com/includes/f_during.php?L4tid={name}&mrmode=1', #post editorvalue=[content]
        'https://www.latex4technics.com/l4ttemp/{name}.png')
    try:
        cookies=requests.get(url[0]).cookies
        image1=requests.post(url[1],cookies=cookies,data={'editorvalue':text[0]})         #/alpha
        if vali(image1.text)==0 :
            print(text[0])
        else:
            imagename=vali(image1.text)
            image=requests.get(url[3].format(name=imagename),cookies=cookies)
            store(0,image.content)
    except Exception as e:
        print(e)
        return 0
    else:
        fail=[]       
        for i in range(1,len(text)):
            re=requests.post(url[2].format(name=imagename),cookies=cookies,data={'editorvalue':text[i]})
            image=requests.get(url[3].format(name=imagename),cookies=cookies)
            if re.status_code!=200 or image.status_code!=200:
                fail.append({'id':i,'text':text[i]})
                print(text[i])
                print('格式出错，请查看帮助改进格式')
            else:
                store(i,image.content)
    

def test():          #网络测试函数
    a=['\\alpha']
    latextoImage(a)
if __name__=='__main__':
    test()