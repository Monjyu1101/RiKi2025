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
import pandas

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_sales_report_to_json"
        self.func_ver  = "v0.20230803"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "指定された日付範囲の売上レポートを取得しJSON形式で返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                            "type": "string",
                            "description": "日付範囲の開始日付、日付は%Y/%m/%d形式 (例) 2023/07/24"
                    },
                    "end_date": {
                            "type": "string",
                            "description": "日付範囲の終了日付、日付は%Y/%m/%d形式 (例) 2023/07/24"
                    },
                },
                "required": ["start_date", "end_date"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        dir_path = os.path.dirname(__file__)
        self.pandas_df = pandas.read_excel(dir_path + '/' + 'サンプル_売上レポート.xlsx')
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        start_date = None
        end_date   = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            start_date = args_dic.get('start_date')
            end_date   = args_dic.get('end_date')

        # JSON化
        res = self.pandas_df.to_json(force_ascii=False)

        dic = {}
        dic['result'] = '売上レポート取得できました'
        dic['json']   = res
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "start_date" : "2023/07/24", "end_date" : "2023/07/24" }'))
