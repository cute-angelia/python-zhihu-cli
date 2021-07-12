# coding=UTF-8
import json
from urllib import parse
import execjs
import hashlib
import requests

class zhihu_v2():
    def __init__(self):
        self.question = input('请输入想搜索的问题，按回车键进行搜索！\n')
        data1 = {'': self.question}

        self.question = parse.urlencode(data1)
        print(self.question)
        self.parse_url = "/api/v4/search_v3?t=general&q" + self.question + "&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0"
        self.use_url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q' + self.question + '&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0'
        with open('zhihucookie.txt', 'r', encoding='utf-8') as c:
            cookie = c.read()
        self.cookie = cookie

    def get_headers(self):
        star = 'd_c0='
        end = ';'
        cookie_mes = self.cookie[self.cookie.index(star):].replace(star, '')
        cookie_mes = cookie_mes[:cookie_mes.index(end)]
        f = "+".join(["101_3_2.0", self.parse_url, cookie_mes])
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
        print(resp.text)
        json_mes = json.loads(resp.text)
        with open('json_mes1.txt', 'a', encoding='utf-8') as f:
            try:
                for i in range(0, 23):
                    try:
                        id = json_mes['data'][i]['object']['id']
                        if len(str(id)) < 15:
                            try:
                                title = json_mes['data'][i]['object']['title']
                                title = str(title).replace('<em>', '').replace('</em>', '')
            
                            except KeyError:
                                title = json_mes['data'][i]['highlight']['title']
                                title = str(title).replace('<em>', '').replace('</em>', '')
            
                            try:
                                excerpt = json_mes['data'][i]['object']['excerpt']
                                excerpt = str(excerpt).replace('<em>', '').replace('</em>', '')
                            except KeyError:
                                excerpt = '该问题，暂无描述！'
            
                            try:
                                url = json_mes['data'][i]['object']['url']
                                url = str(url).replace('api', 'www').replace('questions', 'question').replace('answers', 'answer')
                            except KeyError:
                                try:
                                    url = json_mes['data'][i]['object']['answer']['url']
                                    url = str(url).replace('api', 'www').replace('questions', 'question').replace('answers', 'answer')
                                except KeyError:
                                    url = json_mes['data'][i]['object']['question']['url']
                                    url = str(url).replace('api', 'www').replace('questions', 'question').replace('answers', 'answer')
            
            
                            try:
                                voteup_count = json_mes['data'][i]['object']['voteup_count']
                                comment_count = json_mes['data'][i]['object']['comment_count']
            
                            except KeyError:
                                try:
                                    voteup_count = json_mes['data'][i]['object']['answer']['voteup_count']
                                    comment_count = json_mes['data'][i]['object']['answer']['comment_count']
            
                                except KeyError:
                                    try:
                                        voteup_count = json_mes['data'][i]['object']['question']['voteup_count']
                                        comment_count = json_mes['data'][i]['object']['question']['comment_count']
                                    except KeyError:
                                        voteup_count = json_mes['data'][i]['object']['follower_count']
            
                        else:
                            excerpt = '协会问题，暂无描述！'
                            title = json_mes['data'][i]['object']['content_list'][0]['title']
                            title = str(title).replace('<em>', '').replace('</em>', '')
                            url = '协会问题，暂无链接！'
                            voteup_count = 'null'
                            comment_count = 'null'
            
            
                    except KeyError:
                        try:
                            id = json_mes['data'][i]['object']['answer_obj']['id']
            
                            excerpt = json_mes['data'][i]['object']['answer_obj']['excerpt']
                            excerpt = str(excerpt).replace('<em>', '').replace('</em>', '')
            
                            title = json_mes['data'][i]['object']['body']['title']
                            title = str(title).replace('<em>', '').replace('</em>', '')
            
                            url = json_mes['data'][i]['object']['answer_obj']['url']
                            url = str(url).replace('api', 'www').replace('questions', 'question').replace('answers', 'answer')
            
                            voteup_count =  json_mes['data'][i]['object']['answer_obj']['voteup_count']
                            comment_count =  json_mes['data'][i]['object']['answer_obj']['comment_count']
            
                        except KeyError:
                            id = json_mes['data'][i]['object']['answers'][0]['id']
            
                            excerpt = json_mes['data'][i]['object']['answers'][0]['excerpt']
                            excerpt = str(excerpt).replace('<em>', '').replace('</em>', '')
            
                            title = json_mes['data'][i]['highlight']['title']
                            title = str(title).replace('<em>', '').replace('</em>', '')
            
            
                            url = json_mes['data'][i]['object']['answers'][0]['url']
                            url = str(url).replace('api', 'www').replace('questions', 'question').replace('answers', 'answer')
            
                    print(('{}\t {}\t {}\t {}\n{}\n\n'.format(title, voteup_count, comment_count, url, excerpt,)))
                    f.write(('{}\t {}\t {}\t {}\n{}\n\n'.format(title, voteup_count, comment_count, url, excerpt,)))

            except:
                pass


def start():
    op.get_headers()


if __name__ == '__main__':
    op = zhihu_v2()
    start()