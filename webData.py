import requests
from bs4 import BeautifulSoup
import json



jsonFile = open("url.json",'r' , encoding='utf-8') 
urls = json.load( jsonFile)
items = urls.items()
for key , value in items:
    fatherClass = key 
    url = value
    # print(key , value)

    response = requests.get(url)
    response.encoding = response.apparent_encoding #设置编码格式
    print("状态码:"+ str( response.status_code ) ) #打印状态码
    # print(response.text)#输出爬取的信息

    soup = BeautifulSoup(response.text, "lxml")
    div = soup.find_all('div' , attrs={'class':"MuiTypography-root MuiTypography-body1"})


    triples = []
    for d in div:
        childrens = d.contents
        
        name = childrens[0].text
        description = childrens[1].text
        name = name.replace(" ", "")
        description = description.replace(" ", "")

        subClassStr = "<http://%s> <http://%s> <http://%s>."
        descriptionStr = "<http://%s> <http://%s> <http://%s>."
        instanceStr ="<http://%s> <http://%s> <http://%s>."
        subClassStr = subClassStr %(name , "subclass", fatherClass)
        descriptionStr = descriptionStr%( name , "description",description )
        print("名字：", name , "————————描述：", description)
        triples.append(subClassStr)
        triples.append(descriptionStr)

        for i in range(10):
            tempStr = instanceStr %(name , "instance" , name + str(i))
            triples.append(tempStr)


    filename = ("%s_triples.nt") % (fatherClass)
    with open(filename,"w+", encoding='utf-8') as fd:
        fd.write("\n".join(triples))
        print("write %s success!"% fatherClass)