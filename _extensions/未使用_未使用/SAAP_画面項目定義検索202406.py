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

import datetime
import pandas as pd
import io

import     AZiP_社内システム_SQL実行202405
proc_sql = AZiP_社内システム_SQL実行202405._class()



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_saap_schema_screen_fields"
        self.func_ver  = "v0.20240609"
        self.func_auth = "vB6iLafWVkqg/KH3P6YxIf1VCER2sM/c4q1lOjfOGUZBeDLfh4ZYqNFmz5xhI/4r"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
SAAPシステムを検索し、画面フォームの項目スキーマ情報を取得する。
結果はjsonやEXCELで出力する。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "saap_system": {
                            "type": "string",
                            "description": "SAAPシステムの指定 SAAPシステム名または管理,勤怠,日報 (例) 管理 "
                    },
                    "form_name": {
                            "type": "string",
                            "description": "画面ファーム名 M得意先,T売上等 (例) M得意先"
                    },
                },
                "required": ["saap_system", "form_name"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        saap_system = None
        form_name   = None
        if (json_kwargs != None):
            args_dic  = json.loads(json_kwargs)
            saap_system = args_dic.get('saap_system')
            form_name   = args_dic.get('form_name')

        # 検索処理
        sql  =  " SELECT \n"
        sql +=  "        H.フォームID,   \n"
        sql +=  "        H.フォーム名,   \n"
        sql +=  "        B.入力順,       \n"
        sql +=  "        B.フィールド名, \n"
        sql +=  "        B.入力有無,     \n"
        sql +=  "        B.項目タイプ,   \n"
        sql +=  "        B.バイト長,     \n"
        sql +=  "        B.小数桁数,     \n"
        sql +=  "        B.POP有無       \n"
        sql +=  " FROM      画面項目定義H H \n"
        sql +=  " LEFT JOIN 画面項目定義B B \n"
        sql +=  " ON        B.フォームID = H.フォームID \n"
        sql += f" WHERE \n"
        sql += f"    H.フォームID =    '{ form_name         }' \n"
        sql += f" OR H.フォームID =    '{ form_name + 'H'   }' \n"
        sql += f" OR H.フォームID =    '{ form_name + 'B'   }' \n"
        sql += f" OR H.フォームID like '{ form_name + '_%'  }' \n"
        sql += f" OR H.フォームID like '{ form_name + 'B_%' }' \n"
        sql +=  " ORDER BY H.フォーム名, H.フォームID, B.入力順"

        # SQL実行
        dic = {}
        dic['database'] = saap_system
        dic['SQL']      = sql
        json_dump  = json.dumps(dic, ensure_ascii=False, )
        res_json   = proc_sql.func_proc(json_dump)
        args_dic   = json.loads(res_json)
        res_okng   = args_dic.get('result')
        res_msg    = args_dic.get('message')
        res_json   = args_dic.get('json')
        excel_path = args_dic.get('excel_path')

        # JSON化
        dic = {}
        dic['result'] = res_okng
        if (res_msg is not None):
            dic['message'] = res_msg
        if (res_json is not None):
            dic['json']    = res_json
        if (excel_path is not None):
            dic['excel_path'] = excel_path
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "saap_system" : "管理", "form_name" : "Mホワイトボード" }'))
    #print(ext.func_proc('{}'))


