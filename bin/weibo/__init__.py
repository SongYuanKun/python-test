import logging
import time
from multiprocessing import Process

from bs4 import BeautifulSoup

from dao.OPMysql import OPMysql
from weibo import UserReptile
from weibo.QueryWeiBo import QueryWeiBo

if __name__ == '__main__':

    opm = OPMysql()
    url = 'https://d.weibo.com/'

    while True:
        html = QueryWeiBo.query_wei_bo(url)
        html = BeautifulSoup(html, 'html5lib')
        itemList = html.find_all("div", attrs={"action-type": "feed_list_item"})

        for item in itemList:
            id = item['mid']
            avatar = item.find("img", class_="W_face_radius")['src']
            userHome = item.find("div", class_="WB_info").find("a")['href']
            userId = item.find("div", class_="WB_info").find("a")['usercard'].split("&")[0].split("=")[1]
            createTime = item.find("div", class_="WB_from").find("a")['date']
            device = item.find("div", class_="WB_from").find_all("a")
            if len(device) == 2:
                device = device[1].get_text()
            else:
                device = ''
            content = item.find(attrs={'node-type': 'feed_list_content'}).get_text()
            topic = item.find(attrs={'node-type': 'feed_list_content'}).find("a", class_="a_topic")
            if topic is not None:
                topic = topic['href']
            else:
                topic = ''
            query_sql = "select * from weibo where id=%s"
            select_result = opm.op_select(query_sql, id)
            if not select_result:
                insert_sql = "insert into weibo(id,avatar,userHome,userId,content,topic,device,createTime)" \
                             " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                try:
                    opm.op_insert(insert_sql, (id, avatar, userHome, userId, content, topic, device, createTime))
                except Exception as e:
                    logging.error(e)
                    logging.error(id, avatar, userHome, userId, content, topic, device, createTime)
            p = Process(target=UserReptile.UserReptile.run(userHome))
            p.start()

        time.sleep(10)
        logging.info("sleep:10")
