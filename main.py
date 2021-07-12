# coding=UTF-8
import json,re
from urllib import parse
import execjs
import hashlib
import requests

class zhihu_v2():
    def __init__(self):
        self.userid = input('请输入用户id，查询所有回答！\n')
        

        if self.userid == "":
          self.userid = "yi-qi-chi-fan-qu-chi-dong-xi"

        print("userid:" + self.userid)

        self.use_url = 'https://www.zhihu.com' + "/api/v4/members/"+self.userid+"/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset=0&limit=20&sort_by=created"
        
        with open('zhihucookie.txt', 'r', encoding='utf-8') as c:
            cookie = c.read()
        self.cookie = cookie

    def get_path_form_url(_, uri):
        res = uri.replace("https://www.zhihu.com", "")
        return res

    def get_headers(self):
        star = 'd_c0='
        end = ';'
        cookie_mes = self.cookie[self.cookie.index(star):].replace(star, '')
        cookie_mes = cookie_mes[:cookie_mes.index(end)]
        f = "+".join(["101_3_2.0", self.get_path_form_url(self.use_url), cookie_mes])
        fmd5 = hashlib.new('md5', f.encode()).hexdigest()
        with open('g_encrypt.js', 'r') as f:
            ctx1 = execjs.compile(f.read(), cwd='node_modules')
        encrypt_str = "2.0_%s" % ctx1.call('b', fmd5)
        print(encrypt_str)
        headers = {
            "x-api-version": "3.0.91",
            'x-app-za': 'OS=Web',
            "x-zse-93": "101_3_2.0",
            "x-zse-96": encrypt_str,
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Cookie": self.cookie,
        }
        self.zh_ask(headers)

    def zh_ask(self, headers):
        resp = requests.get(url=self.use_url, headers=headers)

        json_mes = json.loads(resp.text)

        #print(json_mes)
        print(self.use_url)
        #print(headers)

        with open('json_result.txt', 'a', encoding='utf-8') as f:
            try:
                for iterating_var in json_mes['data']:
                  # 正则提取图片地址 data-original=
                  pic_urls = re.findall('data-original="(.*?)"',iterating_var['content'],re.S)
                  for key in pic_urls:
                    f.write(key.replace("_720w", "") + "\n")

                if json_mes['paging']['is_end'] == False :
                  offsets = re.findall('offset=(\d+)',json_mes['paging']['next'],re.S)
                  print("还有记录","offsets",offsets)

                  # nexturl = json_mes['paging']['next']
                  nexturl = re.sub(r'offset=(\d+)', "offset=" + offsets[0], self.use_url)

                  # print(nexturl)

                  self.use_url = nexturl
                  self.get_headers()
            except:
                pass

def start():
    op.get_headers()


if __name__ == '__main__':
    op = zhihu_v2()
    start()