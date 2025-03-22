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

import ollama
import subprocess

import socket
qHOSTNAME = socket.gethostname().lower()

use_ollama_server_list = ['kondou-latitude', 'kondou-sub64']
use_ollama_server_ip   = '192.168.200.96'



prompt_ja = \
"""
画像を詳しく説明してください。
"""

prompt_en1 = \
"""
Please explain the image in detail.
"""

prompt_en2 = \
"""
以下の英語を日本語に翻訳してください。
"""

class moondream_class:
    def __init__(self, ):
        self.bot_auth               = None
        self.init_run               = False
        self.ollama_v_enable        = False
        self.ollama_a_enable        = False

    def init(self, ):
        self.init_run               = True

        # ollama
        self.ollama_server          = 'localhost'
        self.ollama_port            = '11434'
        self.ollama_v_enable        = False
        self.ollama_v_model         = 'moondream:latest'
        self.ollama_a_enable        = False
        self.ollama_a_model         = 'phi3:mini-128k'
        if(qHOSTNAME in use_ollama_server_list):
            self.ollama_server      = use_ollama_server_ip

        # ollama 認証
        self.bot_auth               = False
        self.ollama_client = None
        self.ollama_models = []
        try:
            self.ollama_client = ollama.Client(host=f"http://{ self.ollama_server }:{ self.ollama_port }", )
            get_models  = self.ollama_client.list().get('models')
            for model in get_models:
                self.ollama_models.append(model.get('name'))
        except:
            print(' ollama  : server (' + self.ollama_server + ') not enabled! ')
            if (self.ollama_server == 'localhost'):
                self.ollama_client = None
            else:
                print(' ollama  : localhost try ... ')
                try:
                    del self.ollama_client
                    self.ollama_client = ollama.Client(host="http://localhost:11434", )
                    get_models  = self.ollama_client.list().get('models')
                    for model in get_models:
                        self.ollama_models.append(model.get('name'))
                    self.ollama_server = 'localhost'
                    self.ollama_port   = '11434'
                except:
                    self.ollama_client = None

        # ollama モデル設定 (v)
        if (self.ollama_v_model in self.ollama_models):
            self.ollama_v_enable = True
            self.bot_auth        = True
            print(' ollama  : model enabled. (' + self.ollama_v_model + ') ')
        else:
            if (self.ollama_server == 'localhost'):
                try:
                    print(' ollama  : model download ... (' + self.ollama_v_model + ') ')
                    if (os.name == 'nt'):
                        try:
                            subprocess.Popen(['cmd.exe', '/c', 'ollama', 'pull', self.ollama_v_model, ])
                        except:
                            pass
                    self.ollama_client.pull(self.ollama_v_model, )
                    self.ollama_v_enable = True
                    self.bot_auth        = True
                    self.ollama_models.append(self.ollama_v_model)
                    print(' ollama  : model download complete.')
                except:
                    print(' ollama  : model download error!')

        # ollama モデル設定 (a)
        if (self.ollama_a_model in self.ollama_models):
            self.ollama_a_enable = True
            self.bot_auth        = True
            print(' ollama  : model enabled. (' + self.ollama_a_model + ') ')
        else:
            if (self.ollama_server == 'localhost'):
                try:
                    print(' ollama  : model download ... (' + self.ollama_a_model + ') ')
                    if (os.name == 'nt'):
                        try:
                            subprocess.Popen(['cmd.exe', '/c', 'ollama', 'pull', self.ollama_a_model, ])
                        except:
                            pass
                    self.ollama_client.pull(self.ollama_a_model, )
                    self.ollama_a_enable = True
                    self.bot_auth        = True
                    self.ollama_models.append(self.ollama_a_model)
                    print(' ollama  : model download complete.')
                except:
                    print(' ollama  : model download error!')

        if (self.bot_auth == True):
            print(f"{ self.ollama_server } (ollama) authenticate OK!")
        else:
            print(f"{ self.ollama_server } (ollama) authenticate NG!")

    # ollama moondream
    def ollama_moondream(self, file_path=None, ):
        if (self.init_run == False):
            self.init()

        res_text = ''

        try:
            if (self.ollama_v_enable == True):

                # プロンプト
                messages = []
                msg = {"role": "user", "content": prompt_en1, "images":[file_path] }
                messages.append(msg)

                # AI 画像認識
                response = self.ollama_client.chat(
                            model=self.ollama_v_model, 
                            messages=messages, )

                # 結果
                text = response['message']['content'].strip()
                text = text.replace('.', '.\n')
                res_text += text + '\n'

            if  (res_text != '') \
            and (self.ollama_a_enable == True):

                # プロンプト
                messages = []
                msg = {"role": "user", "content": prompt_en2 + '\n' + text, }
                messages.append(msg)

                # AI 翻訳処理
                response = self.ollama_client.chat(
                            model=self.ollama_a_model, 
                            messages=messages, )

                # 結果
                text     = response['message']['content'].strip()
                res_text += text + '\n'

        except Exception as e:
            print(e)

        # 文書成形
        text = self.text_replace(text=res_text, )
        if (text.strip() != ''):
            res_text = text
        else:
            res_text = '!'

        return res_text

    def text_replace(self, text='', ):
        if (text.strip() == ''):
            return ''

        text = text.replace('\r', '')

        text = text.replace('。', '。\n')
        text = text.replace('?', '?\n')
        text = text.replace('？', '?\n')
        text = text.replace('!', '!\n')
        text = text.replace('！', '!\n')
        text = text.replace('。\n」','。」')
        text = text.replace('。\n"' ,'。"')
        text = text.replace("。\n'" ,"。'")
        text = text.replace('?\n」','?」')
        text = text.replace('?\n"' ,'?"')
        text = text.replace("?\n'" ,"?'")
        text = text.replace('!\n」','!」')
        text = text.replace('!\n"' ,'!"')
        text = text.replace("!\n'" ,"!'")
        text = text.replace("!\n=" ,"!=")
        text = text.replace("!\n--" ,"!--")

        text = text.replace('\n \n ' ,'\n')
        text = text.replace('\n \n' ,'\n')

        hit = True
        while (hit == True):
            if (text.find('\n\n')>0):
                hit = True
                text = text.replace('\n\n', '\n')
            else:
                hit = False

        return text.strip()



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "vision_annotation_to_text"
        self.func_ver  = "v0.20240630"
        self.func_auth = "5jim9cejw7GOgoegtxDC7X3rYfbC+pU4fTMARR+9aY2XZ/s9Y83HK1t5AyGUsGos"
        self.function  = {
            "name": self.func_name,
            "description": "イメージの認識(moondream)",
            "parameters": {
                "type": "object",
                "properties": {
                    "runMode": {
                        "type": "string",
                        "description": "実行モード 例) assistant"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "addin_yolo_test.jpg"
                    },
                },
                "required": ["runMode", "file_path"]
            }
        }

        # 初期設定
        self.runMode   = 'assistant'
        self.moondream = moondream_class()
        self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        file_path = None
        if (json_kwargs is not None):
            args_dic = json.loads(json_kwargs)
            self.runMode   = args_dic.get('runMode', self.runMode)
            file_path      = args_dic.get('file_path')

        # 処理
        res_okng = 'ng'
        res_text = None

        if (file_path is None) or (not os.path.isfile(file_path)):
            pass

        else:
            res_text = self.moondream.ollama_moondream(file_path=file_path, )

        # 戻り
        dic = {}
        if (res_text is not None) and (res_text != '') and (res_text != '!'):
            dic['result']      = 'ok'
            dic['result_text'] = res_text
        else:
            dic['result']      = 'ng'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "runMode" : "assistant", ' \
                      + '"file_path" : "addin_yolo_test.jpg"' \
                      + ' }'))


