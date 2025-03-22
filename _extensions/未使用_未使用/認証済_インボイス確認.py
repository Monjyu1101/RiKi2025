#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

# https://excelapi.org/

import json

import requests
import urllib

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_company_address_and_invoice_registered_status"
        self.func_ver  = "v0.20230803"
        self.func_auth = "9pDmL604XrGUhPJzY7hb2UtFsMUGbKTMRx9dxXIbkPrGZsyHvQqSqn61O22R0p24Un8aJ3fVpFLE540a0Iz92w=="
        self.function  = {
            "name": self.func_name,
            "description": "法人名または法人番号から、郵便番号、住所の法人情報とインボイス登録状況を取得する。１社に特定できない場合はおおまかな住所も指定して検索する。",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name_or_number": {
                        "type": "string",
                        "description": "法人名または法人番号 (例) トダ"
                    },
                    "address": {
                        "type": "string",
                        "description": "おおまかな住所 (例) 兵庫県三木市"
                    },
                },
                "required": ["company_name_or_number"]
            }
        }

        res = self.func_reset()

    def __del__(self, ):
        return True

    def func_reset(self, ):
        self.__del__()
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        company_name = None
        address      = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            company_name = args_dic.get('company_name_or_number')
            address = args_dic.get('address')

        # 名前から法人数
        url = "https://api.excelapi.org/company/number_sum?"
        url += 'name=' + urllib.parse.quote(company_name)
        if (address != None):
            url += '&address=' + urllib.parse.quote(address)
        response = requests.get(url)
        if (response.status_code == 200):
            件数 = int(response.content.decode())
            #print(件数)

            if   (件数 == 0):
                dic = {}
                dic['result'] = "法人が見つかりませんでした" 
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump
            elif (件数 != 1):
                dic = {}
                dic['result'] = "指定の名前を含む法人が、" + str(件数) + "件見つかりました。おおまかな住所を指定して絞り込んでください" 
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump
            else:

                # 名前から法人番号
                url = "https://api.excelapi.org/company/number?"
                url += 'name=' + urllib.parse.quote(company_name)
                if (address != None):
                    url += '&address=' + urllib.parse.quote(address)
                response = requests.get(url)
                if (response.status_code == 200):
                    法人番号 = str(response.content.decode())
                    #print(法人番号)

                    # 法人番号から法人名
                    url = "https://api.excelapi.org/company/name?"
                    url += 'id=' + urllib.parse.quote(法人番号)
                    response = requests.get(url)
                    if (response.status_code == 200):
                        法人名 = str(response.content.decode())
                        #print(法人名)

                    # 法人番号から郵便番号
                    url = "https://api.excelapi.org/company/zipcode?"
                    url += 'id=' + urllib.parse.quote(法人番号)
                    response = requests.get(url)
                    if (response.status_code == 200):
                        郵便番号 = str(response.content.decode())
                        #print(郵便番号)

                    # 法人番号から所在地
                    url = "https://api.excelapi.org/company/address?"
                    url += 'id=' + urllib.parse.quote(法人番号)
                    response = requests.get(url)
                    if (response.status_code == 200):
                        法人住所 = str(response.content.decode())
                        #print(法人住所)

                    # 法人番号からインボイスの登録状況
                    url = "https://api.excelapi.org/company/invoice_check?"
                    url += 'id=' + urllib.parse.quote(法人番号)
                    response = requests.get(url)
                    if (response.status_code == 200):
                        登録未登録 = str(response.content.decode())
                        #print(登録未登録)
                        registered = 'no'
                        if (登録未登録=='登録'):
                            registered = 'yes'

                    dic = {}
                    dic['result'] = "法人情報が取得出来ました" 
                    dic['company_number']     = 法人番号 
                    dic['company_name']       = 法人名 
                    dic['company_zipcode']    = 郵便番号 
                    dic['company_address']    = 法人住所
                    dic['invoice_registered'] = registered #登録未登録
                    json_dump = json.dumps(dic, ensure_ascii=False, )
                    #print('  --> ', json_dump)
                    return json_dump

        dic = {}
        dic['result'] = "法人情報の取得に失敗しました" 
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ ' \
                      + '"company_name_or_number" : "トダ"' \
                      + ' }'))
    print(ext.func_proc('{ ' \
                      + '"company_name_or_number" : "トダ",' \
                      + '"address" : "兵庫県三木市"' \
                      + ' }'))
