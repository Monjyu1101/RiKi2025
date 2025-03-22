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

import _v6__qRiKi_key
qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_encrypt_or_decrypt_text"
        self.func_ver  = "v0.20230803"
        self.func_auth = "9u1MIxHEw1aG6y1+l+Ehe0Ej1+umOIeJAlCVa8J5zDjrKVOIi/T8aMa0K33eoBWp"
        self.function  = {
            "name": self.func_name,
            "description": "入力された文字列を暗号化または復号化の指示により処理し、その結果の文字列を返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                            "type": "string",
                            "description": "入力された文字列 (例) hallo world!"
                    },
                    "process": {
                            "type": "string",
                            "description": "暗号化'encrypt'または復号化'decrypt'の指示 (例) encrypt"
                    },
                },
                "required": ["text", "process"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        text    = None
        process = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            text    = args_dic.get('text')
            process = args_dic.get('process')

        res_text = ''
        try:

            # 暗号化
            if (process == 'encrypt'):
                res_text = qRiKi_key.encryptText(text=text)

                # 戻り
                dic = {}
                dic['encrypt_text'] = res_text
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump

            # 復号化
            elif (process == 'decrypt'):
                res_text = qRiKi_key.decryptText(text=text)

                # 戻り
                dic = {}
                dic['decrypt_text'] = res_text
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump

        except Exception as e:
            print(e)
            res_text = e

        # 戻り
        dic = {}
        dic['error'] = res_text
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc( '{ "text": "hallo world!", "process": "encrypt" }' ))
