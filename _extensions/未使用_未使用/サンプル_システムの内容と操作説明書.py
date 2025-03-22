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
        self.func_name = "get_operation_manual_to_text"
        self.func_ver  = ""
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "このシステム「クリップ,CLIP,GPT,力,RiKi」について質問があったときに使う説明書を返す。全文指定なら原文で返答し、そうでない場合は内容をもとに適切に返答する",
            "parameters": {
                "type": "object",
                "properties": {
                    "this_system_name": {
                        "type": "string",
                        "description": "このシステムと判断した呼称 (例) clip"
                    },
                },
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        # マニュアル読取
        dir_path = os.path.dirname(__file__)
        filename = dir_path + '/' + 'サンプル_システムの内容と操作説明書.txt'
        encoding =  'utf-8-sig'

        text = ''
        r = codecs.open(filename, 'r', encoding)
        for t in r:
            t = t.replace('\r', '')
            text += t
        r.close
        r = None

        hit = True
        while (hit == True):
            if (text.find('\n\n')>0):
                hit = True
                text = text.replace('\n\n', '\n')
            else:
                hit = False
        text = text.strip()

        self.manual_text = text

        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数 無し

        # 戻り
        dic = {}
        dic['text'] = self.manual_text
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc())
