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
        self.func_name = "write_python_script_to_playground"
        self.func_ver  = "v0.20230803"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "生成されたpythonコードを実験場へ出力（書き出し）する",
            "parameters": {
                "type": "object",
                "properties": {
                    "python_script": {
                            "type": "string",
                            "description": "python_script (例) print('Hallo World!')"
                    },
                    "output_path": {
                            "type": "string",
                            "description": "出力ファイルパス (例) temp/output.txt"
                    },
                },
                "required": ["python_script"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 入力引数
        python_script    = None
        input_file_path  = None
        output_file_path = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            python_script    = args_dic.get('python_script')
            input_file_path  = args_dic.get('input_file_path')
            output_file_path = args_dic.get('output_file_path')

        # 処理（コード出力）
        dir_path = os.path.dirname(__file__) + '/'
        filename = dir_path + '__chatgpt_genarate.py'
        encoding='utf-8'
        w = codecs.open(filename, 'w', encoding)
        w.write(python_script)
        w.close()
        w = None

        # 結果出力
        dic = {}
        dic['result']      = '実行しました'
        dic['output_path'] = filename
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump

if __name__ == '__main__':

    # テスト用コード
    ext = _class()
    print(ext.func_proc('{ "python_script" : "print(123)", "input_file_path" : "", "output_file_path" : "" }'))
