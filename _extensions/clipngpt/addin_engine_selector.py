#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

import json

res_sysText_ja = \
"""
----- あなたの役割 -----
あなたは、会話履歴と最後のユーザー入力から、ユーザーの意図を推測し、適切なクラスに分類します。
ユーザー入力の内容を理解し、それを正しい分類に関連付けて回答します。
以下のクラスのうち、適切なものに分類して回答してください。
回答は以下のjsonスキーマ形式でお願いします。
'{"chat_class": str}'
""" + '\n\n'

res_sysText_en = \
"""
----- Your Role -----
You will infer the user's intent from the conversation history and the last user input, and classify it into the appropriate class.
Understand the content of the user's input and associate it with the correct classification to respond.
Please classify and respond to the appropriate one of the following classes.
Please provide your response using the specified English words in the following JSON schema format.
'{"chat_class": str}'
""" + '\n\n'

res_reqText_ja = \
"""
----- あなたへの依頼 -----
会話履歴と最後のユーザー入力から、ユーザーの意図を分類してください。
決められた日本語の単語で分類、回答してください。
1) おはよう、こんにちは等、簡単なあいさつは、"簡単な挨拶"
2) 今日もお願いします等、少し複雑なあいさつは、"複雑な挨拶"
3) 会話の続きや指示の続き等、新たな要求ではないときは、"会話の続き"
4) 画像分析に関する指示や質問なら、"画像分析"
5) プログラムの作成や生成を伴う高度な指示は、"コード生成"
6) プログラムの実行を伴う高度な指示は、"コード実行"
7) インターネット上の最新情報の検索が必要な指示は、"ウェブ検索"
8) 事前登録文書の検索が必要な指示は、"文書検索"
9) あいさつ文ではないが、toolやfunctionを利用しない簡単な会話は、"簡単な会話"
10) toolやfunctionを利用し、１ステップで終わる会話は、"複雑な会話"
11) toolやfunctionを利用し、回答までに数ステップ必要と思われる複雑な会話は、"アシスタント"
12) 上記のいずれにも当てはまらない場合は、"その他"
回答は必ず日本語の単語、"簡単な挨拶","複雑な挨拶","会話の続き","画像分析","コード生成","コード実行",
"ウェブ検索","文書検索","簡単な会話","複雑な会話","アシスタント"または"その他"の何れかに分類お願いします。
""" + '\n\n'

res_reqText_en = \
"""
----- Your Task -----
Please classify the user's intent from the conversation history and the last user input.
Classify and respond with the predetermined Japanese terms.
1) Simple greetings such as "Good morning, Hello" should be classified as "簡単な挨拶" (Simple Greeting).
2) Slightly complicated greetings such as "Please take care of me today too" should be classified as "複雑な挨拶" (Complex Greeting).
3) When it is a continuation of the conversation or instructions and does not contain a new request, classify it as "会話の続き" (Continuation of Conversation).
4) Instructions or questions related to image analysis should be classified as "画像分析" (Image Analysis).
5) Advanced instructions involving the creation or generation of programs should be classified as "コード生成" (Code Generation).
6) Advanced instructions involving the execution of programs should be classified as "コード実行" (Code Execution).
7) Instructions that require searching for the latest information on the Internet should be classified as "ウェブ検索" (Web Search).
8) Instructions that require searching pre-registered documents should be classified as "文書検索" (Document Search).
9) Conversations that are not greetings but are simple conversations without the use of tools or functions should be classified as "簡単な会話" (Simple Conversation).
10) Conversations that use tools or functions and end in one step should be classified as "複雑な会話" (Complex Conversation).
11) Conversations that use tools or functions and are expected to require several steps to answer should be classified as "アシスタント" (Assistant).
12) If it does not fall into any of the above categories, classify it as "その他" (Other).
Please respond using the Japanese terms: "簡単な挨拶" (Simple Greeting), "複雑な挨拶" (Complex Greeting), "会話の続き" (Continuation of Conversation), "画像分析" (Image Analysis), "コード生成" (Code Generation), "コード実行" (Code Execution), "ウェブ検索" (Web Search), "文書検索" (Document Search), "簡単な会話" (Simple Conversation), "複雑な会話" (Complex Conversation), "アシスタント" (Assistant), or "その他" (Other).
""" + '\n\n'



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "choose_an_ai_engine"
        self.func_ver  = "v0.20240608"
        self.func_auth = "8IqHYAtmhpcvVYjM7aDqVuUSDMObVzhyaLsRN6hC+58="
        self.function  = {
            "name": self.func_name,
            "description": \
"""
２ステップでAIエンジンを選択。
ステップ１(getPrompt)
　過去の会話履歴の要約と、今回の要求を受け取り、会話クラスを分析するためのスクリプトを生成する。
ステップ２(class2engine)
　会話クラスを受け取り、利用するエンジンを決める。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "runMode": {
                        "type": "string",
                        "description": "実行モード 例) assistant"
                    },
                    "openai_exec": {
                        "type": "string",
                        "description": "openai実行有効 yes,no 例) yes"
                    },
                    "freeai_exec": {
                        "type": "string",
                        "description": "freeai実行有効 yes,no 例) yes"
                    },
                    "ollama_exec": {
                        "type": "string",
                        "description": "ollama実行有効 yes,no 例) yes"
                    },
                    "engine_greeting": {
                        "type": "string",
                        "description": "greetingエンジン auto,openai,freeai,local, 例) auto"
                    },
                    "engine_chat": {
                        "type": "string",
                        "description": "chatエンジン auto,openai,freeai,local, 例) auto"
                    },
                    "engine_vision": {
                        "type": "string",
                        "description": "visionエンジン auto,openai,freeai,local, 例) auto"
                    },
                    "engine_fileSearch": {
                        "type": "string",
                        "description": "fileSearchエンジン auto,openai,freeai,local, 例) auto"
                    },
                    "engine_webSearch": {
                        "type": "string",
                        "description": "webSearchエンジン auto,openai,freeai,local, 例) auto"
                    },
                    "engine_assistant": {
                        "type": "string",
                        "description": "assistantエンジン auto,openai,freeai,local, 例) auto"
                    },
                    "runStep": {
                        "type": "string",
                        "description": "実行ステップ 1(getPrompt)または2(class2engine) 例) 1"
                    },
                    "step1_history": {
                        "type": "string",
                        "description": "過去の会話履歴 例) おはよう"
                    },
                    "step1_text": {
                        "type": "string",
                        "description": "今回の要求文 例) 今日は何月何日？"
                    },
                    "step2_class": {
                        "type": "string",
                        "description": "会話クラス 例) chat"
                    },
                },
                "required": ["runMode", "openai_enable", "freeai_enable", "ollama_enable", "engine_chat", "engine_vision", "engine_assistant", "runStep"]
            }
        }

        # 初期設定
        self.runMode                = 'assistant'
        self.openai_exec            = True
        self.freeai_exec            = True
        self.ollama_exec            = True
        self.cgpt_engine_greeting   = 'auto'
        self.cgpt_engine_chat       = 'auto'
        self.cgpt_engine_vision     = 'auto'
        self.cgpt_engine_fileSearch = 'auto'
        self.cgpt_engine_webSearch  = 'auto'
        self.cgpt_engine_assistant  = 'auto'
        self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        openai_exec     = ''
        freeai_exec     = ''
        ollama_exec     = ''
        runStep         = ''
        historyText     = ''
        inpText         = ''
        chat_class      = 'auto'
        if (json_kwargs is not None):
            args_dic = json.loads(json_kwargs)
            self.runMode                = args_dic.get('runMode', self.runMode)
            openai_exec                 = args_dic.get('openai_exec', '')
            freeai_exec                 = args_dic.get('freeai_exec', '')
            ollama_exec                 = args_dic.get('ollama_exec', '')
            self.cgpt_engine_greeting   = args_dic.get('engine_greeting', self.cgpt_engine_greeting)
            self.cgpt_engine_chat       = args_dic.get('engine_chat', self.cgpt_engine_chat)
            self.cgpt_engine_vision     = args_dic.get('engine_vision', self.cgpt_engine_vision)
            self.cgpt_engine_fileSearch = args_dic.get('engine_fileSearch', self.cgpt_engine_fileSearch)
            self.cgpt_engine_webSearch  = args_dic.get('engine_webSearch', self.cgpt_engine_webSearch)
            self.cgpt_engine_assistant  = args_dic.get('engine_assistant', self.cgpt_engine_assistant)
            runStep                     = args_dic.get('runStep', '')
            historyText                 = args_dic.get('step1_historyText', '')
            inpText                     = args_dic.get('step1_inpText', '')
            chat_class                  = args_dic.get('step2_class', 'auto')

        if (openai_exec != ''):
            if (openai_exec in ['yes', 'True']):
                self.openai_exec = True
            else:
                self.openai_exec = False
        if (freeai_exec != ''):
            if (freeai_exec in ['yes', 'True']):
                self.freeai_exec = True
            else:
                self.freeai_exec = False
        if (ollama_exec != ''):
            if (ollama_exec in ['yes', 'True']):
                self.ollama_exec = True
            else:
                self.ollama_exec = False

        # ------------------------------
        # ステップ１
        # ------------------------------
        if (str(runStep) == '1'):

            # エンジン選択
            res_engine = 'freeai'
            if   ((self.openai_exec == True) and (self.freeai_exec == True)):
                if (self.cgpt_engine_chat != 'auto'):
                    res_engine = self.cgpt_engine_chat
            if   ((self.openai_exec == True) and (self.freeai_exec != True) and (self.ollama_exec != True)):
                res_engine = 'openai'
            elif ((self.openai_exec != True) and (self.freeai_exec == True) and (self.ollama_exec != True)):
                res_engine = 'freeai'
            elif ((self.openai_exec != True) and (self.freeai_exec != True) and (self.ollama_exec == True)):
                res_engine = 'ollama'

            # 要求文
            if (res_engine == 'freeai'):
                res_sysText = res_sysText_ja
                res_reqText = res_reqText_ja
            else:
                res_sysText = res_sysText_en
                res_reqText = res_reqText_en

            res_inpText = ''
            if (historyText.strip() != ''):
                res_inpText += "''' これは過去の会話履歴です。\n"
                res_inpText += historyText.rstrip() + '\n'
                res_inpText += "''' 会話履歴はここまでです。ここから最後のユーザー入力です。\n\n"
            res_inpText += inpText.rstrip() + '\n'

            # 戻り
            dic = {}
            dic['result']  = 'ok'
            dic['sysText'] = res_sysText
            dic['reqText'] = res_reqText
            dic['inpText'] = res_inpText
            dic['engine']  = res_engine
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump

        # ------------------------------
        # ステップ２
        # ------------------------------
        elif (str(runStep) == '2'):

            # dafault補正
            if (chat_class == 'auto') \
            or (chat_class == 'greeting') \
            or (chat_class == '簡単な挨拶'):
                chat_class   = self.cgpt_engine_greeting
                if (chat_class == 'auto') and (self.freeai_exec == True):
                    chat_class  = 'freeai'
                if (chat_class == 'auto') and (self.openai_exec == True):
                    chat_class  = 'openai'

            if (chat_class == 'chat') \
            or (chat_class == '複雑な挨拶') \
            or (chat_class == '簡単な会話') \
            or (chat_class == 'その他'):
                chat_class   = self.cgpt_engine_chat
                if (chat_class == 'auto') and (self.freeai_exec == True):
                    chat_class  = 'freeai'
                if (chat_class == 'auto') and (self.openai_exec == True):
                    chat_class  = 'openai'

            if (chat_class == 'vision') \
            or (chat_class == '画像分析'):
                chat_class  = self.cgpt_engine_vision
                if (chat_class == 'auto') and (self.freeai_exec == True):
                    chat_class  = 'freeai'
                if (chat_class == 'auto') and (self.openai_exec == True):
                    chat_class  = 'openai'

            if (chat_class == 'fileSearch') \
            or (chat_class == '文書検索'):
                chat_class  = self.cgpt_engine_fileSearch
                if (chat_class == 'auto') and (self.openai_exec == True):
                    chat_class  = 'assistant' #'openai'
                if (chat_class == 'auto') and (self.freeai_exec == True):
                    chat_class  = 'freeai'

            if (chat_class == 'webSearch') \
            or (chat_class == 'ウェブ検索'):
                chat_class  = self.cgpt_engine_webSearch
                if (chat_class == 'auto') and (self.freeai_exec == True):
                    chat_class  = 'freeai'
                if (chat_class == 'auto') and (self.openai_exec == True):
                    chat_class  = 'assistant' #'openai'

            if (chat_class == 'assistant') \
            or (chat_class == 'コード生成') \
            or (chat_class == 'コード実行') \
            or (chat_class == '複雑な会話') \
            or (chat_class == 'アシスタント'):
                chat_class  = self.cgpt_engine_assistant
                if (chat_class == 'auto') and (self.openai_exec == True):
                    chat_class  = 'assistant' #'openai'
                if (chat_class == 'auto') and (self.freeai_exec == True):
                    chat_class  = 'freeai'

            elif (chat_class == 'freeai') \
            or   (chat_class == 'f-flash') or (chat_class == 'f-pro') or (chat_class == 'f-ultra'):
                if (self.freeai_exec != True):
                    if   (self.openai_exec == True):
                        chat_class = 'assistant' #'openai'

            elif (chat_class == 'ollama') \
            or   (chat_class == 'mini') or (chat_class == 'phi3') or (chat_class == 'moondream'):
                if (self.ollama_exec != True):
                    if   (self.freeai_exec == True):
                        chat_class = 'freeai'
                    elif (self.openai_exec == True):
                        chat_class = 'openai'

            # エンジン選択
            res_engine = 'auto'
            if   (chat_class == 'auto') \
            or   (chat_class == 'openai'):
                if (self.openai_exec == True):
                    res_engine = 'openai'
            elif (chat_class == 'assistant') \
            or   (chat_class == 'コード生成') \
            or   (chat_class == 'コード実行') \
            or   (chat_class == '文書検索') \
            or   (chat_class == '複雑な会話') \
            or   (chat_class == 'アシスタント'):
                if (self.openai_exec == True):
                    res_engine = 'openai'
            elif (chat_class == 'freeai') \
            or   (chat_class == 'f-flash') or (chat_class == 'free') or (chat_class == 'f-ultra'):
                if (self.freeai_exec == True):
                    res_engine = 'freeai'
            elif (chat_class == 'ollama') \
            or   (chat_class == 'mini') or (chat_class == 'phi3') or (chat_class == 'moondream'):
                if (self.ollama_exec == True):
                    res_engine = 'ollama'

            # 省略時エンジン
            if (res_engine == 'auto'):
                res_engine = 'freeai'

            # エンジン補正
            if (self.openai_exec == True) \
            or (self.freeai_exec == True) \
            or (self.ollama_exec == True):
                if   ((self.openai_exec == True) and (self.freeai_exec != True) and (self.ollama_exec != True)):
                    res_engine = 'openai'
                elif ((self.openai_exec != True) and (self.freeai_exec == True) and (self.ollama_exec != True)):
                    res_engine = 'freeai'
                elif ((self.openai_exec != True) and (self.freeai_exec != True) and (self.ollama_exec == True)):
                    res_engine = 'ollama'

            # 戻り
            dic = {}
            dic['result']  = 'ok'
            dic['class']   = chat_class
            dic['engine']  = res_engine
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump

        # ------------------------------
        # ？
        # ------------------------------
        else:

            # 戻り
            dic = {}
            dic['result']  = 'ng'
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "runMode" : "assistant" }'))

    print(ext.func_proc('{ ' \
                      + '"runStep":"1", "step1_history":"Hi,", "step1_text":"Im Good!" ' \
                      + ' }'))

    print(ext.func_proc('{ ' \
                      + '"runStep":"2", "step2_class":"auto" ' \
                      + ' }'))


