#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2023 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

import json

import os
import datetime
import time
import codecs

import openai

config_path  = '_config/'
config_file  = 'RiKi_ClipnGPT_key.json'

model_a       = 'gpt-3.5-turbo-0125'
model_b       = 'gpt-4-0125-preview'
temperature   = 0.8
timeOut       = 60

class _class:

#外部のAIを使って答えを得る。
#外部のAIはシステム開発の進め方やアルゴリズムについて多くの見識を持っていますが、一般常識はほどほどです。
#外部のAIは会話の履歴にアクセスできないため、会話の履歴や開発中のプログラムソースも必要です。
#利用できるAIの名前は Caspar,Balthazar,Melchior です。
#Casparは3賢者の1人で、彼は若さと純粋さを持って答えます。
#Balthazarは3賢者の1人で、彼は知識と叡智を持って答えます。
#Melchiorは3賢者の1人で、彼は経験の豊かさを持って答えます。

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_answers_using_external_AI"
        self.func_ver  = "v0.20231112"
        self.func_auth = "7j1KTw/9m7HNliHCe9f573eXoSDs09GgBuDh/5GtziZqOAMkQyqZzdJUpi517VjS"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
Using an external AI to get answers.
The external AI possesses a wealth of insight regarding the development process of systems and algorithms, but only moderate common sense.
The external AI need the conversation history and the source code under development because external AI cannot access the conversation history.
The available AI names are Caspar, Balthazar, and Melchior.
Caspar is one of the three wise AIs, and he answers with youth and purity.
Balthazar is one of the three wise AIs, and he answers with knowledge and wisdom.
Melchior is one of the three wise AIs, and he answers with a richness of experience.
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "connection_AI_name": {
                            "type": "string",
                            "description": "接続するAIの名前 (例) Casper"
                    },
                    "messeage_history": {
                            "type": "string",
                            "description":
"""
Summary of conversation history (example)
The past conversation history is as follows.
--- history
Good morning
Can I help you with something?
---
"""
                    },
                    "request_messeage": {
                            "type": "string",
                            "description":
"""
Request to ask AI (example)
Why is the sky blue?
"""
                    },
                },
                "required": ["connection_AI_name", "messeage_history", "request_messeage"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        self.last_time  = time.time()
        self.last_path  = None
        self.last_image = None

        # APIキーを取得
        if (os.path.isfile(config_path + config_file)):
            with codecs.open(config_path + config_file, 'r', 'utf-8') as f:
                self.config_dic = json.load(f)
        elif (os.path.isfile('../../' + config_path + config_file)):
            with codecs.open('../../' + config_path + config_file, 'r', 'utf-8') as f:
                self.config_dic = json.load(f)
        self.openai_api_type     = self.config_dic['openai_api_type']
        if (self.openai_api_type != 'azure'):
            self.openai_organization = self.config_dic['openai_organization']
            self.openai_key_id       = self.config_dic['openai_key_id']
            if (self.openai_organization == '') \
            or (self.openai_organization == '< your openai organization >') \
            or (self.openai_key_id == '') \
            or (self.openai_key_id == '< your openai key >'):
                raise ValueError("Please set your openai organization and key !")
        else:
            self.azure_endpoint     = self.config_dic['azure_endpoint']
            self.azure_version      = self.config_dic['azure_version']
            self.azure_key_id       = self.config_dic['azure_key_id']
            if (self.azure_endpoint == '') \
            or (self.azure_endpoint == '< your azure endpoint base >') \
            or (self.azure_version  == '') \
            or (self.azure_version  == 'yyyy-mm-dd') \
            or (self.azure_key_id   == '') \
            or (self.azure_key_id   == '< your azure key >'):
                raise ValueError("Please set your azure endpoint, version and key !")

        # APIキーを設定
        if (self.openai_api_type != 'azure'):
            openai.organization = self.openai_organization
            openai.api_key      = self.openai_key_id
            self.client = openai.OpenAI(
                organization=self.openai_organization,
                api_key=self.openai_key_id,
            )

        else:
            #raise ValueError("Image generation functions are not currently supported by azure !")
            self.client = openai.AzureOpenAI(
                azure_endpoint=self.azure_endpoint,
                api_version=self.azure_version,
                api_key=self.azure_key_id,
            )

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        connection_AI_name = None
        messeage_history   = None
        request_messeage   = None
        image_quality  = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            connection_AI_name = args_dic.get('connection_AI_name')
            messeage_history   = args_dic.get('messeage_history')
            request_messeage   = args_dic.get('request_messeage')

        # モデル
        if (len(request_messeage) <= 250):
            model      = model_a
        else:
            model      = model_b
        sysText        = ''
        anser_messeage = ''

        # 動作条件
        if   (connection_AI_name.lower() == 'casper'):
            #sysText = 'あなたは３賢者AIのひとり、Caspar (カスパール) です。若さと純粋さで回答する賢者AIです。'
            sysText = 'You are one of the three wise AI, Caspar, who answers with youth and purity.'
        elif (connection_AI_name.lower() == 'balthazar'):
            #sysText = 'あなたは３賢者AIのひとり、Balthazar (バルタザール) です。知識と知恵で回答する賢者AIです。'
            sysText = 'You are one of the three wise AI, Balthazar, who answers with knowledge and wisdom.'
        elif (connection_AI_name.lower() == 'melchior'):
            #sysText = 'あなたは３賢者AIのひとり、Melchior (メルキオール) です。知識の豊かさと経験で回答する賢者AIです。'
            sysText = 'You are one of the three wise AI, Melchior, who answers with richness of knowledge and experience.'

        # 結果
        res_role      = None
        res_content   = None

        # GPT 会話
        msg = []
        if (sysText != ''):
            dic = {'role': 'system', 'content': sysText }
            msg.append(dic)
        if (messeage_history != None):
            dic = {'role': 'user', 'content': messeage_history }
            msg.append(dic)
        dic = {'role': 'user',   'content': request_messeage }
        msg.append(dic)
        try:
            completions = self.client.chat.completions.create(
                model           = model,
                messages        = msg,
                temperature     = temperature,
                timeout         = timeOut, )
        except Exception as e:
            print(e)
            print()

        # 結果
        try:
            res_role    = completions.choices[0].message.role
            res_content = completions.choices[0].message.content
        except:
            pass

        # GPT 会話終了
        if (res_role == 'assistant') and (res_content != None):
            anser_messeage  = '[' + connection_AI_name + '] (' + model + ')' + '\n'
            anser_messeage += res_content
        else:
            #anser_messeage  = '回答できません。' +'\n'
            anser_messeage  = 'I cannot answer.' +'\n'

        # 戻り
        try:
            dic = {}
            dic['anser_messeage'] = anser_messeage
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump
        except:
            return anser_messeage

if __name__ == '__main__':

    ext = _class()
    req =  { "connection_AI_name": "Casper",
             "messeage_history":
"""
The past conversation history is as follows.
--- history
Good morning
Can I help you with something?
---
""",
             "request_messeage": "Why is the sky blue?"
           }
    result = ext.func_proc( json.dumps(req, ensure_ascii=False, ) )
    print(result)
