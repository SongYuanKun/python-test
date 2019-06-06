import logging
import re
import urllib.request

from bs4 import BeautifulSoup

headers = {
    'Cookie': 'SINAGLOBAL=2078721877459.5728.1559567242749; wvr=6; SSOLoginState=1559616971; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=6054902381065.152.1559616976820; ULV=1559616976827:2:2:2:6054902381065.152.1559616976820:1559567242756; YF-Page-G0=761bd8cde5c9cef594414e10263abf81|1559638878|1559638691; SCF=Akrwmn7zAkMkrSsx3CPh5CDHZCpghGBbokghT8-Cb_e6h1DL1lW1HS3M3lyi2VPdWXHn45CA1tkMTfT69TWi6a0.; SUB=_2A25x_LAPDeRhGeNO7FoZ9CbJyDiIHXVSi6bHrDV8PUJbmtAKLXXlkW9NTsEfV5vyQBojZx6sF7hCiuJSoG8Lb3Bi; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56FTYyHNeazSVoGRzuyNLL5JpX5K-hUgL.Fo-7S0nRShnfe0B2dJLoIpRLxK.L1-zLB-2LxKBLBo.L12zLxKnL1hnL1-H0IN.t; SUHB=0mxUV9efmcWC8Q; ALF=1591342045; TC-Page-G0=153ff31dae1cf71cc65e7e399bfce283|1559806052|1559806044'
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
