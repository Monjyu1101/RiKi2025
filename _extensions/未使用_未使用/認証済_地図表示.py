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
import os
import time

from selenium.webdriver import Edge
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver import Safari
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "execute_map_display"
        self.func_ver  = "v0.20230820"
        self.func_auth = "WVTTNIJ5p4pGPCZDFyNkewOSxCcrTrHYls2Qid5stc8="
        self.function  = {
            "name": self.func_name,
            "description": \
"""
指定したブラウザで指定場所の地図や目的地までの経路地図の表示、さらに指定があれば第２の目的地までの経路地図を表示する。
地図ならびに経路表示を消去することも出来る
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "show_or_hide": {
                        "type": "string",
                        "description": "表示または消去の指定 show,hide (例) show"
                    },
                    "departure": {
                        "type": "string",
                        "description": "指定場所（出発地）の正確な住所。「自宅」など曖昧な内容ではなく必ず住所の内容 (例) 兵庫県三木市福井１０−３０"
                    },
                    "destination": {
                        "type": "string",
                        "description": "経路表示のときの目的地の正確な住所。得意先名など曖昧な内容ではなく必ず住所の内容 (例) 兵庫県加古川市加古川町篠原町30-1"
                    },
                    "destination2": {
                        "type": "string",
                        "description": "経路表示のときの第２の目的地の正確な住所。得意先名など曖昧な内容ではなく必ず住所の内容 (例) 兵庫県姫路市本町６８"
                    },
                    "browser": {
                        "type": "string",
                        "description": "ブラウザーの選択 edge,chrome,firefox,safari (例) edge"
                    },
                },
                "required": ["show_or_hide"]
            }
        }

        self.engine_list = []
        res = self.func_reset()

    def __del__(self, ):
        for e in self.engine_list:
            try:
                e.quit()
                e = None
            except:
                pass

    def func_reset(self, ):
        self.__del__()
        return True

    def browser_open(self, url='https://www.google.com/', browser='edge', ):
        try:
            # ブラウザ
            if (browser != None):
                browser = browser.lower()
            if (os.name == 'nt'):
                if   (browser == 'chrome'):
                    engine = Chrome()
                elif (browser == 'firefox'):
                    engine = Firefox()
                elif (browser == 'safari'):
                    engine = Safari()
                else:
                    engine = Edge()
            else:
                if   (browser == 'safari'):
                    engine = Safari()
                elif (browser == 'edge'):
                    engine = Edge()
                elif (browser == 'firefox'):
                    engine = Firefox()
                else:
                    engine = Chrome()
            self.engine_list.append(engine)

            # 最大化
            try:
                engine.maximize_window()
            except Exception as e:
                print(e)

            # WEB ページ開く
            engine.get(url)

            # 全要素取得待機
            engine_wait = WebDriverWait(engine, 10)
            element = engine_wait.until(EC.visibility_of_all_elements_located)

            return True
        except Exception as e:
            print(e)

        return False



    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        show_or_hide = None
        departure    = None
        destination  = None
        destination2 = None
        browser      = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            show_or_hide = args_dic.get('show_or_hide')
            departure    = args_dic.get('departure')
            destination  = args_dic.get('destination')
            destination2 = args_dic.get('destination2')
            browser      = args_dic.get('browser')

        # 地図、経路表示
        if (show_or_hide == 'show'):

            departure = departure.replace('　','')
            departure = departure.replace(' ','')
            if (destination != None):
                destination = destination.replace('　','')
                destination = destination.replace(' ','')
            if (destination2 != None):
                destination2 = destination2.replace('　','')
                destination2 = destination2.replace(' ','')

            if (destination == None):
                url = 'https://www.google.com/maps/place/' + departure
            else:
                url = 'https://www.google.com/maps/dir/' + departure + '/' + destination

            if (destination2 != None):
                url += '/' + destination2

            # ブラウザ表示
            res = self.browser_open(url=url, browser=browser, )
            if (res == True):

                dic = {}
                dic['result'] = "地図表示しました" 
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump

            else:

                dic = {}
                dic['error'] = "地図表示に失敗しました" 
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump

        # 地図、経路消去
        if (show_or_hide == 'hide'):

            # リセット
            self.func_reset()

            dic = {}
            dic['result'] = "地図表示を消去しました" 
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ ' \
                      + '"show_or_hide" : "show",' \
                      + '"departure" : "三木市役所、兵庫県三木市福井１０−３０",' \
                      + '"browser" : "edge"' \
                      + ' }'))
    time.sleep(10.00)
    print(ext.func_proc('{ ' \
                      + '"show_or_hide" : "hide"' \
                      + ' }'))
    time.sleep(2.00)

    print(ext.func_proc('{ ' \
                      + '"show_or_hide" : "show",' \
                      + '"departure" : "三木市役所、兵庫県三木市福井１０−３０",' \
                      + '"destination" : "JR西日本加古川駅、兵庫県加古川市加古川町篠原町30-1",' \
                      + '"destination2" : "姫路城、兵庫県姫路市本町６８", ' \
                      + '"browser" : "edge"' \
                      + ' }'))
    time.sleep(10.00)
    print(ext.func_proc('{ ' \
                      + '"show_or_hide" : "hide"' \
                      + ' }'))
    time.sleep(2.00)

