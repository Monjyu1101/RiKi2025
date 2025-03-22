#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

import json

import requests
# SSLエラーを無視するための処理
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

import ssl
import urllib
# SSLエラーを無視するための処理
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

from bs4 import BeautifulSoup

def url2text(url_path='https://www.google.co.jp/', ):
        text = ''

        try:

            # なろうページ？
            narou_pages = ''
            if (url_path[:26] == 'https://ncode.syosetu.com/'):
                page_path = url_path[26:]
                page_hit  = page_path.find('/')
                # 最初の"/"
                if (page_hit >= 0):
                    page_str = page_path[page_hit:]
                    try:
                        # ページ番号
                        page_n = int(page_str.replace('/',''))
                        narou_pages = '[なろう] ' + page_path[:page_hit] + ' ' + str(page_n)
                    except:
                        pass

            # -----------
            # 通常の手法
            # -----------
            if (text == '') and (narou_pages==''):
                html = requests.get(url_path, timeout=(5,15), verify=False, )
                html_content   = html.content
                html_encording = html.encoding
                # html.parser, html5lib, lxml,
                soup = BeautifulSoup(html_content, 'html.parser', from_encoding=html_encording)

                try:
                    for script in soup(["script", "style"]):
                        script.decompose()
                    t = soup.get_text()
                    for line in t.splitlines():
                        if (line.strip() != ''):
                            text += line.strip() + '\n'
                except:
                    pass

            # -----------
            # なろう
            # -----------
            if (narou_pages != ''):
                html = urllib.request.urlopen(url_path, context=ssl_context, )
                soup = BeautifulSoup(html, 'html.parser')

                # タイトル
                title = ''
                try:
                    title = soup.find('p', class_='chapter_title').get_text()
                except:
                    try:
                        title = soup.find('p', class_='margin_r20').get_text()
                    except:
                        pass
                if (title != ''):
                    text += 'タイトル：' + title + '\n'

                # サブタイトル
                sub_title = ''
                try:
                    sub_title = soup.find('p', class_='novel_subtitle').get_text()
                except:
                    pass
                if (sub_title != ''):
                    text += sub_title + '\n'

                # 本文
                for l in range(1, 9999):
                    p_list = soup.find_all('p', id='L' + str(l))
                    if (len(p_list) == 0):
                        break
                    if (l == 1):
                        text += '本文' + '\n'
                    for p in p_list:
                        text += p.get_text() + '\n'

            # -----------
            # 別の手法
            # -----------
            if (text == ''):
                html = urllib.request.urlopen(url_path, context=ssl_context, )
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    t = soup.get_text()
                    for line in t.splitlines():
                        if (line.strip() != ''):
                            text += line.strip() + '\n'
                except:
                    pass

        except Exception as e:
            print(e)

        # 編集
        text = text.replace('\r', '')
        text = text.replace('。', '。\n')
        text = text.replace('。\n」','。」')
        hit = True
        while (hit == True):
            if (text.find('\n\n')>0):
                hit = True
                text = text.replace('\n\n', '\n')
            else:
                hit = False
        text = text.strip()

        if (text == ''):
            return '!'
        else:
            return text



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_new_info_from_web_to_text"
        self.func_ver  = "v0.20230820"
        self.func_auth = "8Ss+N/dLKZmX5PTI+RF1f12Q3Tdu12hMiiq7xZtIksapX5HfQExAArmYdh/oaDDp"
        self.function  = {
            "name": self.func_name,
            "description": "最新情報やwebの情報を取得するするため、検索urlや指定urlのwebページの内容を取得する（2000文字）",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "ウェブページのurl (例) https://openai.com/blog/chatgpt"
                    },
                    "max_text_length": {
                        "type": "string",
                        "description": "取得する最大文字数 (例) 2000"
                    },
                },
                "required": ["url"]
            }
        }

        self.last_url  = ''
        self.last_text = ''
        res = self.func_reset()

    def __del__(self, ):
        pass

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        url             = None
        max_text_length = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            url             = args_dic.get('url')
            max_text_length = args_dic.get('max_text_length')

        if (max_text_length == None) or (str(max_text_length) == '') or (str(max_text_length) == '0'):
            msx_text_length = '2000'

        # ２回連続はエラー
        if (url == self.last_url):
            # 戻り
            dic = {}
            dic['error'] = 'さきほどと同じページの内容はできません'
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump

        # 情報取得
        text = url2text(url_path=url, )
        self.last_url  = url
        self.last_text = text
        if (text != '') and (text != '!'):

            # 最大文字数
            if (max_text_length != None) and (str(max_text_length) != '') and (str(max_text_length) != '0'):
                length = int(max_text_length)
                text = text[:length]

            # 戻り
            dic = {}
            dic['text'] = text
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump

        else:

            # 戻り
            dic = {}
            dic['error'] = '内容取得できませんでした'
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ ' \
                      + '"url" : "https://openai.com/blog/chatgpt"' \
                      + ' }'))
