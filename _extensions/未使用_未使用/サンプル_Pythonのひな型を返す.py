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
import codecs

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_python_script_template_to_text"
        self.func_ver  = "v0.20230803"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "拡張ファンクションで利用できるpythonスクリプトのひな型を返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "template_type": {
                        "type": "string",
                        "description": "ひな型のタイプ (例) 拡張ファンクション"
                    },
                },
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        dir_path = os.path.dirname(__file__)

        # 拡張ファンクション
        filename = dir_path + '/' + 'サンプル_Pythonを書き出す.py'
        self.ext_function = self.get_hinagata(filename)

        return True

    def get_hinagata(self, filename):
        encoding =  'utf-8-sig'
        text = ''
        r = codecs.open(filename, 'r', encoding)
        for t in r:
            t = t.replace('\r', '')
            text += t
        r.close
        r = None
        return text

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        template_type    = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            template_type = args_dic.get('template_type')

        # 拡張ファンクション
        if True:

            # 戻り
            dic = {}
            dic['result'] = '実行しました'
            dic['template_type'] = '拡張ファンクション'
            dic['python_script'] = self.ext_function
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "template_type" : "ひな型" }'))
