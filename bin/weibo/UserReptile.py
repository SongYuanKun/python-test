# 子进程要执行的代码

from bs4 import BeautifulSoup

from dao.OPMysql import OPMysql
from weibo.QueryWeiBo import QueryWeiBo


class UserReptile(object):

    @staticmethod
    def run(homepage):
        opm = OPMysql()
        html = QueryWeiBo.query_wei_bo(homepage)
        html = BeautifulSoup(html, 'html5lib')
        item_list = html.find_all("div", attrs={"action-type": "feed_list_item"})
        for item in item_list:
            id = item['diss-data'].split('=')[1]
            avatar = item.find("img", lambda tag: tag.has_attr('src'), class_="W_face_radius/")['src']
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
                opm.op_insert(insert_sql, (id, avatar, userHome, userId, content, topic, device, createTime))


if __name__ == '__main__':
    UserReptile.run('https://weibo.com/u/2322168320?refer_flag=1028035010_&is_hot=1')
