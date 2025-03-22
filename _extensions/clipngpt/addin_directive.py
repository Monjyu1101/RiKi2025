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

# 指令文字列
check_header_list = '["riki","assistant","vision","openai","freeai","free","local",]'
check_inner_list  = '["???","？？？","!!!","！！！",]'

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "check_directive_text"
        self.func_ver  = "v0.20240421"
        self.func_auth = "dOU3srqOdDZgjRevofZ8IFPkMygWmlwdZLMTTaYtWrseC3+q69Ai+GD4evO6W/ao"
        self.function  = {
            "name": self.func_name,
            "description": "指示文のチェック",
            "parameters": {
                "type": "object",
                "properties": {
                    "runMode": {
                        "type": "string",
                        "description": "実行モード 例) assistant"
                    },
                    "original_text": {
                        "type": "string",
                        "description": "原文 (例) いま何時？？？"
                    },
                },
                "required": ["runMode", "original_text"]
            }
        }

        # 初期設定
        self.runMode = 'assistant'
        self.func_reset()

    def func_reset(self, ):
        self.check_header = eval(check_header_list)
        for i in reversed(range(len(self.check_header))):
            if (self.check_header[i] == ''):
                del self.check_header[i]
        self.check_inner = eval(check_inner_list)
        for i in reversed(range(len(self.check_inner))):
            if (self.check_inner[i] == ''):
                del self.check_inner[i]
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        runMode                 = ''
        original_text           = ''
        openai_nick_name        = ''
        freeai_nick_name        = ''
        gpt_a_nick_name         = ''
        gpt_b_nick_name         = ''
        gpt_v_nick_name         = ''
        gpt_x_nick_name         = ''
        freeai_a_nick_name      = ''
        freeai_b_nick_name      = ''
        freeai_v_nick_name      = ''
        freeai_x_nick_name      = ''
        ollama_a_nick_name      = ''
        ollama_b_nick_name      = ''
        ollama_v_nick_name      = ''
        ollama_x_nick_name      = ''
        if (json_kwargs is not None):
            args_dic = json.loads(json_kwargs)
            runMode                 = args_dic.get('runMode', '')
            original_text           = args_dic.get('original_text', '')
            openai_nick_name        = args_dic.get('openai_nick_name', '')
            gpt_a_nick_name         = args_dic.get('gpt_a_nick_name', '')
            gpt_b_nick_name         = args_dic.get('gpt_b_nick_name', '')
            gpt_v_nick_name         = args_dic.get('gpt_v_nick_name', '')
            gpt_x_nick_name         = args_dic.get('gpt_x_nick_name', '')
            freeai_a_nick_name      = args_dic.get('freeai_a_nick_name', '')
            freeai_b_nick_name      = args_dic.get('freeai_b_nick_name', '')
            freeai_v_nick_name      = args_dic.get('freeai_v_nick_name', '')
            freeai_x_nick_name      = args_dic.get('freeai_x_nick_name', '')
            ollama_a_nick_name      = args_dic.get('ollama_a_nick_name', '')
            ollama_b_nick_name      = args_dic.get('ollama_b_nick_name', '')
            ollama_v_nick_name      = args_dic.get('ollama_v_nick_name', '')
            ollama_x_nick_name      = args_dic.get('ollama_x_nick_name', '')

        if (runMode == ''):
            runMode = self.runMode
        else:
            self.runMode = runMode

        # 処理
        res_okng = 'ng'
        res_text = None

        text     = original_text.strip()
        if (text == ''):
            pass

        else:

            # ヘッダー文字列？
            if (res_text is None):
                for s in self.check_header:
                    nm = s + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                        break 

            # ニックネーム指定？
            if (res_text is None):
                if (openai_nick_name != ''):
                    nm = openai_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        res_text = text[len(str(nm)):]
                if (freeai_nick_name != ''):
                    nm = freeai_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        res_text = text[len(str(nm)):]

                if (gpt_a_nick_name != ''):
                    nm = gpt_a_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (gpt_b_nick_name != ''):
                    nm = gpt_b_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (gpt_v_nick_name != ''):
                    nm = gpt_v_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (gpt_x_nick_name != ''):
                    nm = gpt_x_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text

                if (freeai_a_nick_name != ''):
                    nm = freeai_a_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (freeai_b_nick_name != ''):
                    nm = freeai_b_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (freeai_v_nick_name != ''):
                    nm = freeai_v_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (freeai_x_nick_name != ''):
                    nm = freeai_x_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text

                if (ollama_a_nick_name != ''):
                    nm = ollama_a_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (ollama_b_nick_name != ''):
                    nm = ollama_b_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (ollama_v_nick_name != ''):
                    nm = ollama_v_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text
                if (ollama_x_nick_name != ''):
                    nm = ollama_x_nick_name + ','
                    if (text[:len(str(nm))].lower() == str(nm).lower()):
                        #res_text = text[len(str(nm)):]
                        res_text = original_text

            # インナー文字列？
            if (res_text is None):
                for inner in self.check_inner:
                    if (text.find(str(inner)) >= 0):
                        res_text = text.replace(str(inner), '')
                        break 

            # 特殊文字列等
            if (res_text is None):
                if (text[-3:] == '===') or (text[-3:] == '＝＝＝'):
                    res_text  = '以下の式を計算して！' + '\n'
                    res_text += "''' \n"
                    res_text += text[:-3] + '\n'
                    res_text += "'''"
                elif (text[-3:].lower() == ',ja') or (text[-3:].lower() == '，ｊａ'):
                    res_text  = '以下の文章を和訳して！' + '\n'
                    res_text += "''' \n"
                    res_text += text[:-3] + '\n'
                    res_text += "'''"
                elif (text[-3:].lower() == ',en') or (text[-3:].lower() == '，ｅｎ'):
                    res_text  = '以下の文章を英訳して！' + '\n'
                    res_text += "''' \n"
                    res_text += text[:-3] + '\n'
                    res_text += "'''"
 
        # 戻り
        dic = {}
        if (res_text is not None):
            if (res_text != ''):
                dic['result']      = 'ok'
                dic['result_text'] = res_text
            else:
                dic['result']      = 'ng'
        else:
            dic['result']      = 'ng'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "runMode" : "assistant" }'))

    print(ext.func_proc('{ ' \
                      + '"original_text" : "gpt,テストです"' \
                      + ' }'))

    print(ext.func_proc('{ ' \
                      + '"original_text" : "テストです???"' \
                      + ' }'))

    print(ext.func_proc('{ ' \
                      + '"original_text" : "テスト!!!です"' \
                      + ' }'))

    print(ext.func_proc('{ ' \
                      + '"original_text" : "123x456==="' \
                      + ' }'))

    print(ext.func_proc('{ ' \
                      + '"original_text" : "This is testting,ja"' \
                      + ' }'))

    print(ext.func_proc('{ ' \
                      + '"original_text" : "テストです,en"' \
                      + ' }'))


