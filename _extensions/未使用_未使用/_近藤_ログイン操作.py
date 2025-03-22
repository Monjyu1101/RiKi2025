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
        self.func_name = "login_operation"
        self.func_ver  = "v0.20240423"
        self.func_auth = "hPDGnNkfn4rhlUejzKQ7jH65VogNGj91kVn/DbJNzXw="
        self.function  = {
            "name": self.func_name,
            "description": "ＩＤ入力欄、パスワード入力欄ならびにログインボタンの中心座標をもとに、自動ログイン操作を行う",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_x": {
                        "type": "integer",
                        "description": "ＩＤ入力欄のＸ座標の整数値"
                    },
                    "id_y": {
                        "type": "integer",
                        "description": "ＩＤ入力欄のＹ座標の整数値"
                    },
                    "pw_x": {
                        "type": "integer",
                        "description": "パスワード入力欄のＸ座標の整数値"
                    },
                    "pw_y": {
                        "type": "integer",
                        "description": "パスワード入力欄のＹ座標の整数値"
                    },
                    "btn_x": {
                        "type": "integer",
                        "description": "ログインボタンのＸ座標の整数値"
                    },
                    "btn_y": {
                        "type": "integer",
                        "description": "ログインボタンのＹ座標の整数値"
                    },
                },
                "required": ["id_x", "id_y", "pw_x", "pw_y", "btn_x", "btn_y"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        id_x, id_y   = 0, 0
        pw_x, pw_y   = 0, 0
        btn_x, btn_y = 0, 0
        if (json_kwargs is not None):
            args_dic = json.loads(json_kwargs)
            id_x  = int(args_dic.get('id_x',  0))
            id_y  = int(args_dic.get('id_y',  0))
            pw_x  = int(args_dic.get('pw_x',  0))
            pw_y  = int(args_dic.get('pw_y',  0))
            btn_x = int(args_dic.get('btn_x', 0))
            btn_y = int(args_dic.get('btn_y', 0))

        print(id_x, id_y  )
        print(pw_x, pw_y  )
        print(btn_x, btn_y)

        # 戻り
        dic = {}
        dic['result'] = "ok"
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ ' \
                      + '"id_x" : "300",' \
                      + '"id_y" : "300",' \
                      + '"pw_x" : "300",' \
                      + '"pw_y" : "350",' \
                      + '"btn_x" : "300",' \
                      + '"btn_y" : "400"' \
                      + ' }'))


