import logging
import re
import urllib.request

from bs4 import BeautifulSoup

headers = {
    'Cookie': 'SINAGLOBAL=2078721877459.5728.1559567242749; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56FTYyHNeazSVoGRzuyNLL5JpX5KMhUgL.Fo-7S0nRShnfe0B2dJLoIpRLxK.L1-zLB-2LxKBLBo.L12zLxKnL1hnL1-H0IN.t; ALF=1591756369; SSOLoginState=1560220369; SCF=Akrwmn7zAkMkrSsx3CPh5CDHZCpghGBbokghT8-Cb_e6bPXRSAb4tp16gPGUJ5pOaAhyXKbMBJeKhFn48CjrvgA.; SUB=_2A25x-2KCDeRhGeNO7FoZ9CbJyDiIHXVTcdNKrDV8PUNbmtBeLVamkW9NTsEfVwWe7pv3HDTLIFkXx64u4vbvZfxf; SUHB=0oUoPW4u4aTh8k; TC-Page-G0=45685168db6903150ce64a1b7437dbbb|1560220372|1560220368; wb_view_log_5078848534=1920*10801; _s_tentry=login.sina.com.cn; Apache=3794245684225.5303.1560220392288; ULV=1560220392296:3:3:3:3794245684225.5303.1560220392288:1559616976827; webim_unReadCount=%7B%22time%22%3A1560220403915%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D',
    'Host': 'd.weibo.com',
    'Referer': 'https://d.weibo.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}


class QueryWeiBo(object):

    @staticmethod
    def query_wei_bo(host):
        req = urllib.request.Request(host, None, headers=headers)
        try:
            response = urllib.request.urlopen(req).read().decode("UTF-8")
            response = BeautifulSoup(response, 'html5lib')
        except Exception as e:
            logging.error(e)
            return None
        str_tag = '{"ns":"pl.content.homeFeed.index'
        html = response.find_all(string=re.compile(str_tag))
        result = ''
        for html_sub in html:
            html_sub = str(html_sub)
            index = html_sub.find(str_tag)
            html_sub = html_sub.replace(str_tag, '')[index:]
            index = html_sub.find(',"html":"')
            html_sub = html_sub.replace(',"html":"', '')
            result += html_sub[index:-20].replace("\\\"", "").replace("\\r", "").replace("\\n", "").replace("\\t",
                                                                                                            "").replace(
                "\\/", "/").replace("/\"", "\"")
        return result
