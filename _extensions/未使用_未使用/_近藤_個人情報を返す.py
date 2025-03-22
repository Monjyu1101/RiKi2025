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
        self.func_name = "get_personal_info_to_json"
        self.func_ver  = "v0.20230803"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "私や自分について、住所,電話番号,勤務先情報,社員ID,プレイリストURL等の個人情報を返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "person": {
                        "type": "string",
                        "description": "私や自分を特定した場合の単語 (例) 私"
                    },
                },
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        dir_path = os.path.dirname(__file__)
        with codecs.open(dir_path + '/' + '_近藤_個人情報.json', 'r', 'utf-8') as f:
            self.personal_info = json.load(f)
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数 無し

        # 戻り
        json_dump = json.dumps(self.personal_info, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc())
