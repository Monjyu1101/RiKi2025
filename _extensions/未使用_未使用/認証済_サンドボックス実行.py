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
import time



import importlib

sandbox = None
try:
    import    addin_autoSandbox
    sandbox = addin_autoSandbox._class()
except:
    try:
        loader = importlib.machinery.SourceFileLoader('addin_autoSandbox.py', '_extensions/clipngpt/addin_autoSandbox.py')
        #loader = importlib.machinery.SourceFileLoader('addin_autoSandbox.py', '_extensions/function/addin_autoSandbox.py')
        addin_autoSandbox = loader.load_module()
        sandbox = addin_autoSandbox._class()
    except:
        print('★"addin_autoSandbox"は利用できません！')



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "execute_local_sandbox"
        self.func_ver  = "v0.20240630"
        self.func_auth = "mSZp8ufLywaaiw7nQ5UgalMV0kBOjglkYnQ99MoPLcXY5910V/+9BGmMO1CGPA6Y"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
zip圧縮されたソースファイル一式を自動解凍し、
ユーザーローカルのサンドボックス環境で実行確認を行います。
実行確認が行えるのは、html、python、python(flask)、reactです。
reactの場合は、ルートにpackage.jsonファイルが必要です。
また、python(flask)やreactの場合は、実行起動と同時にlocalhost:ポートでブラウザも開き、フロント動作の確認も行えます。
ソースファイル一式は、事前にzip形式で必要なのでダウンロードリンクが必要です。この機能はダウンロードは行いません。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "事前にダウンロード済みのzip圧縮ファイルパス (例) HalloWorld.zip"
                    },
                },
                "required": ["zip_file_path"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数 無し
        zip_file_path = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            zip_file_path = args_dic.get('zip_file_path')

        # 処理
        res_okng = 'ng'
        res_msg  = ''

        # サンドボックス
        #try:
        if True:
            if (sandbox is not None):
                dic = {}
                dic['file_path'] = zip_file_path
                json_dump = json.dumps(dic, ensure_ascii=False, )
                res_json = sandbox.func_proc(json_dump)
                args_dic = json.loads(res_json)
                res_okng = args_dic.get('result')
                res_msg  = args_dic.get('result_text')
                if (res_msg is None):
                    res_msg = args_dic.get('error_text')
            else:
                res_okng = 'ng'
                res_msg  = '★サンドボックスは利用できません！'
                print(res_msg)
        #except Exception as e:
        #    print(e)

        # 戻り
        dic = {}
        dic['result'] = res_okng
        if (res_okng == 'ok'):
            if (res_msg is not None) and (res_msg != ''):
                dic['result_text'] = res_msg
        else:
            if (res_msg is not None) and (res_msg != ''):
                dic['error_text']  = res_msg
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump



if __name__ == '__main__':

    ext = _class()
    #print(ext.func_proc('{ ' \
    #                  + '"zip_file_path" : "HalloWorldSample.zip"' \
    #                  + ' }'))
    #print(ext.func_proc('{ ' \
    #                  + '"zip_file_path" : "HalloWorldFlaskSample.zip"' \
    #                  + ' }'))
    print(ext.func_proc('{ ' \
                      + '"zip_file_path" : "HalloWorldReactSample.zip"' \
                      + ' }'))
    time.sleep(10.00)

