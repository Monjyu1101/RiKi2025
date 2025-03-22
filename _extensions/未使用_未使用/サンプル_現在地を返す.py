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

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_current_location_info"
        self.func_ver  = "v0.20230803"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "現在の場所を返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "現在地を表す単語 (例) ここ"
                    },
                },
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数 無し

        # 戻り
        dic = {}
        dic['location'] = '兵庫県三木市'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc())
