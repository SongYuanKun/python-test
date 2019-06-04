import urllib.request

import pymysql
from DBUtils.PooledDB import PooledDB
from dao.MySqlProp import MySqlProp
from bs4 import BeautifulSoup

from weibo.WeiboEntity import WeiboEntity

headers = {
    'Cookie': 'SINAGLOBAL=2078721877459.5728.1559567242749; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56FTYyHNeazSVoGRzuyNLL5JpX5KMhUgL.Fo-7S0nRShnfe0B2dJLoIpRLxK.L1-zLB-2LxKBLBo.L12zLxKnL1hnL1-H0IN.t; ALF=1591152969; SSOLoginState=1559616971; SCF=Akrwmn7zAkMkrSsx3CPh5CB73CVrskw5IanFPiMkjiUd7_D2L9eslIDQvpNy34GG6X-Dvt5R2P8UyAIs7i1nSpA.; SUB=_2A25x8a2cDeRhGeNO7FoZ9CbJyDiIHXVShphUrDV8PUNbmtBeLUbzkW9NTsEfV1NgwcsGV_fzEJ0nd9G660Gc6CKd; SUHB=0z1AENAxjM_bl2; wb_view_log_5078848534=1920*10801; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=6054902381065.152.1559616976820; ULV=1559616976827:2:2:2:6054902381065.152.1559616976820:1559567242756; TC-Page-G0=b993e9b6e353749ed3459e1837a0ae89|1559638565|1559638559; webim_unReadCount=%7B%22time%22%3A1559638684668%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D; YF-Page-G0=761bd8cde5c9cef594414e10263abf81|1559638691|1559638691'
}

req = urllib.request.Request('https://d.weibo.com/', None, headers)
response = urllib.request.urlopen(req).read().decode("UTF-8")
str = '{"ns":"pl.content.homeFeed.index","domid":"Pl_Core_NewMixFeed__3","css":["style/css/module/list/comb_WB_feed_profile.css?version=';
index = response.find(str)
html = response.replace(str, '')[index:]
index = html.find(',"html":"')
html = html.replace(',"html":"', '')
html = html[index:-20].replace("\\\"", "").replace("\\r", "").replace("\\n", "").replace("\\t", "").replace("\/", "/")

html = BeautifulSoup(html, 'html5lib')
itemList = html.find_all("div", attrs={"action-type": "feed_list_item"})
# html = html.div.div.div.find(id="plc_frame").find(class_="WB_frame").find("div", id="plc_main").find("div", id="plc_discover")


prop = MySqlProp()
pool = PooledDB(pymysql.connect, host=prop.host, port=3306, user=prop.user, password=prop.passWord, database=prop.db)
print(len(itemList))

for item in itemList:
    id = item['mid']
    avatar = item.find("img", class_="W_face_radius")['src']
    userHome = item.find("div", class_="WB_info").find("a")['href']
    userId = item.find("div", class_="WB_info").find("a")['usercard'].split("&")[0].split("=")[1]
    createTime = item.find("div", class_="WB_from").find("a")['date']
    device = item.find("div", class_="WB_from").find_all("a")
    if (len(device) == 2):
        device = device[1].get_text()
    else:
        device = ''
    content = item.find(attrs={'node-type': 'feed_list_content'}).get_text()
    topic = item.find(attrs={'node-type': 'feed_list_content'}).find("a", class_="a_topic")
    if topic != None:
        topic = topic['href']
    else:
        topic = ''

    insertSql = "insert into weibo(id,avatar,userHome,userId,content,topic,device,createTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    conn = pool.connection();
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(insertSql, (id, avatar, userHome, userId, content, topic, device, createTime))
    conn.commit()
    print(id)
