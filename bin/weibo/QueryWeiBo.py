import re
import urllib.request

from bs4 import BeautifulSoup

headers = {
    'Cookie': 'SINAGLOBAL=2078721877459.5728.1559567242749; wvr=6; SSOLoginState=1559616971; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=6054902381065.152.1559616976820; ULV=1559616976827:2:2:2:6054902381065.152.1559616976820:1559567242756; YF-Page-G0=761bd8cde5c9cef594414e10263abf81|1559638878|1559638691; SCF=Akrwmn7zAkMkrSsx3CPh5CDHZCpghGBbokghT8-Cb_e6Q0R1Btyui_ugX8ocKZkDHwopT9D2JZf4S-PP3Kn8Gek.; SUB=_2A25x80JVDeRhGeNO7FoZ9CbJyDiIHXVSiTSdrDV8PUJbmtAKLVXakW9NTsEfVwuExUy7QbdPyGRW5D3vKIi0LYTh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56FTYyHNeazSVoGRzuyNLL5JpX5K-hUgL.Fo-7S0nRShnfe0B2dJLoIpRLxK.L1-zLB-2LxKBLBo.L12zLxKnL1hnL1-H0IN.t; SUHB=0bt8ODauWAFrWB; ALF=1591240068; wb_view_log_5078848534=1920*10801; webim_unReadCount=%7B%22time%22%3A1559704076379%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D; TC-Page-G0=7a922a70806a77294c00d51d22d0a6b7|1559704077|1559704067'
}


class QueryWeiBo(object):

    @staticmethod
    def query_wei_bo(host):
        req = urllib.request.Request(host, None, headers=headers)
        response = urllib.request.urlopen(req).read().decode("UTF-8")
        response = BeautifulSoup(response, 'html5lib')
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
