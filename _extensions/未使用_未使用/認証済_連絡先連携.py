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
        self.func_name = "get_contact_address_info_to_json"
        self.func_ver  = "v0.20230803"
        self.func_auth = "zyasfANjhgsRZgUjMTsaqCSO3vrMKWohoNMAHE+cYuTmKBOi4U3c1T7Ccqy+qhd9"
        self.function  = {
            "name": self.func_name,
            "description": "指定した連絡先の郵便番号、住所、電話番号、FAX番号およびメールアドレス等の情報を返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_name": {
                            "type": "string",
                            "description": "連絡先の名前 (例) みき"
                    },
                },
                "required": ["contact_name"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        dir_path = os.path.dirname(__file__)
        self.pandas_df = pandas.read_excel(dir_path + '/' + '認証済_連絡先情報.xlsx')
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        contact_name = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            contact_name = args_dic.get('contact_name')

        # 処理
        hit = False
        for s in range(len(self.pandas_df)):
            id   = self.pandas_df.loc[s, '連絡先コード']
            nm   = self.pandas_df.loc[s, '連絡先名']
            ubin = self.pandas_df.loc[s, '郵便番号']
            adr  = self.pandas_df.loc[s, '住所']
            tel  = self.pandas_df.loc[s, '電話番号']
            fax  = self.pandas_df.loc[s, 'FAX番号']
            mail = self.pandas_df.loc[s, 'メールアドレス']
            if (nm.find( contact_name ) >= 0):
                hit = True
                dic = {}
                dic['contact_id'] = str(id)
                dic['contact_name'] = str(nm)
                dic['contact_zip_code'] = str(ubin)
                dic['contact_address'] = str(adr)
                dic['contact_telephone_number'] = str(tel)
                dic['contact_fax_number'] = str(fax)
                dic['contact_mail_address'] = str(mail)
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump

        dic = {}
        dic['result'] = 'データ取得に失敗しました'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "contact_name" : "みき" }'))
