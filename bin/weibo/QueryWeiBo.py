import re
import urllib.request

from bs4 import BeautifulSoup

headers = {
    'Cookie': 'SINAGLOBAL=2078721877459.5728.1559567242749; wvr=6; '
              'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56FTYyHNeazSVoGRzuyNLL5JpX5KMhUgL.Fo-7S0nRShnfe0B2dJLoIpRLxK.L1'
              '-zLB-2LxKBLBo.L12zLxKnL1hnL1-H0IN.t; ALF=1591152969; SSOLoginState=1559616971; '
              'SCF=Akrwmn7zAkMkrSsx3CPh5CB73CVrskw5IanFPiMkjiUd7_D2L9eslIDQvpNy34GG6X-Dvt5R2P8UyAIs7i1nSpA.; '
              'SUB=_2A25x8a2cDeRhGeNO7FoZ9CbJyDiIHXVShphUrDV8PUNbmtBeLUbzkW9NTsEfV1NgwcsGV_fzEJ0nd9G660Gc6CKd; '
              'SUHB=0z1AENAxjM_bl2; wb_view_log_5078848534=1920*10801; _s_tentry=login.sina.com.cn; UOR=,,'
              'login.sina.com.cn; Apache=6054902381065.152.1559616976820; '
              'ULV=1559616976827:2:2:2:6054902381065.152.1559616976820:1559567242756; '
              'TC-Page-G0=b993e9b6e353749ed3459e1837a0ae89|1559638565|1559638559; '
              'webim_unReadCount=%7B%22time%22%3A1559638684668%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C'
              '%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D; '
              'YF-Page-G0=761bd8cde5c9cef594414e10263abf81|1559638691|1559638691 '
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
                "\\/",
                "/")
        return result

