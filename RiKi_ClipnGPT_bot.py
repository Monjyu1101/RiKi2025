#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

import sys
import os
import time
import datetime
import codecs
import glob
import shutil

import base64
import json



# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_input  = 'temp/input/'
qPath_output = 'temp/output/'

# 共通ルーチン
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

# openai,freeai,ollama チャットボット
import speech_bot_function
import speech_bot_openai
import speech_bot_openai_key as openai_key
import speech_bot_freeai
import speech_bot_freeai_key as freeai_key
import speech_bot_ollama
import speech_bot_ollama_key as ollama_key



# base64 encode
def base64_encode(file_path):
    with open(file_path, "rb") as input_file:
        return base64.b64encode(input_file.read()).decode('utf-8')

import socket
qHOSTNAME = socket.gethostname().lower()

use_ollama_server_list = ['kondou-latitude', 'kondou-sub64', 'repair-surface7', ]
use_ollama_server_ip   = '192.168.200.96' #kondou-sub64



class _bot:

    def __init__(self, ):
        self.runMode                    = 'debug'
        self.limit_mode                 = False
        self.conf                       = None
        self.addin                      = None
        self.log_queue                  = None

        self.cgpt_secure_level          = 'medium'
        self.cgpt_functions_path        = '_extensions/function/'

        self.cgpt_engine_greeting       = 'auto'
        self.cgpt_engine_chat           = 'auto'
        self.cgpt_engine_vision         = 'auto'
        self.cgpt_engine_fileSearch     = 'auto'
        self.cgpt_engine_webSearch      = 'auto'
        self.cgpt_engine_assistant      = 'auto'

        self.openai_api_type            = ''
        self.openai_default_gpt         = 'auto'
        self.openai_default_class       = ''
        self.openai_auto_continue       = ''
        self.openai_max_step            = ''
        self.openai_max_session         = ''

        self.freeai_api_type            = 'freeai'
        self.freeai_default_gpt         = 'auto'
        self.freeai_default_class       = ''
        self.freeai_auto_continue       = ''
        self.freeai_max_step            = ''
        self.freeai_max_session         = ''
        self.freeai_max_wait_sec        = ''

        self.ollama_api_type            = 'ollama'
        self.ollama_default_gpt         = 'auto'
        self.ollama_default_class       = ''
        self.ollama_auto_continue       = ''
        self.ollama_max_step            = ''
        self.ollama_max_session         = ''
        self.ollama_max_wait_sec        = ''

        self.openai_organization        = '< your openai organization >'
        self.openai_key_id              = '< your openai key >'
        self.azure_endpoint             = '< your azure endpoint base >' 
        self.azure_version              = 'yyyy-mm-dd'
        self.azure_key_id               = '< your azure key >'
        self.freeai_key_id              = '< your freeai key >'
        self.ollama_server              = 'auto'
        self.ollama_port                = 'auto'

        self.openai_nick_name           = ''
        self.openai_model               = ''
        self.openai_token               = ''
        self.openai_temperature         = '0.5'
        self.openai_max_step            = '10'
        self.openai_inpLang             = 'ja-JP'
        self.openai_outLang             = 'ja-JP'

        self.freeai_nick_name           = ''
        self.freeai_model               = ''
        self.freeai_token               = ''
        self.freeai_temperature         = '0.5'
        self.freeai_max_step            = '10'
        self.freeai_inpLang             = 'ja-JP'
        self.freeai_outLang             = 'ja-JP'

        self.ollama_nick_name           = ''
        self.ollama_model               = ''
        self.ollama_token               = ''
        self.ollama_temperature         = '0.5'
        self.ollama_max_step            = '10'
        self.ollama_inpLang             = 'ja-JP'
        self.ollama_outLang             = 'ja-JP'

        self.openai_enable              = False
        self.openai_exec                = False
        self.freeai_enable              = False
        self.freeai_exec                = False
        self.ollama_enable              = False
        self.ollama_exec                = False

        self.gpt_enable                 = False
        self.gpt_functions_enable       = False
        self.gpt_run_count              = 0
        self.gpt_run_last               = time.time()

        self.seq                        = 0
        self.history                    = []
        self.last_chat_class            = 'chat'
        self.last_model_select          = 'auto'



    def print(self, session_id='admin', text='', ):
        print(text, flush=True)
        if (session_id == 'admin') and (self.log_queue is not None):
            try:
                self.log_queue.put(['chatBot', text + '\n'])
            except:
                pass

    def stream(self, session_id='admin', text='', ):
        print(text, end='', flush=True)
        if (session_id == 'admin') and (self.log_queue is not None):
            try:
                self.log_queue.put(['chatBot', text])
            except:
                pass

    def text_replace(self, text=''):
        if "```" not in text:
            return self.text_replace_sub(text)
        else:
            # ```が2か所以上含まれている場合の処理
            first_triple_quote_index = text.find("```")
            last_triple_quote_index = text.rfind("```")
            if first_triple_quote_index == last_triple_quote_index:
                return self.text_replace_sub(text)
            # textの先頭から最初の```までをtext_replace_subで成形
            text_before_first_triple_quote = text[:first_triple_quote_index]
            formatted_before = self.text_replace_sub(text_before_first_triple_quote)
            formatted_before = formatted_before.strip() + '\n'
            # 最初の```から最後の```の直前までを文字列として抽出
            code_block = text[first_triple_quote_index : last_triple_quote_index]
            code_block = code_block.strip() + '\n'
            # 最後の```以降の部分をtext_replace_subで成形
            text_after_last_triple_quote = text[last_triple_quote_index:]
            formatted_after = self.text_replace_sub(text_after_last_triple_quote)
            formatted_after = formatted_after.strip() + '\n'
            # 結果を結合して戻り値とする
            return (formatted_before + code_block + formatted_after).strip()

    def text_replace_sub(self, text='', ):
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



    def init(self, qLog_fn='', runMode='debug', limit_mode=False,
             conf=None, addin=None, log_queue=None, ):

        self.runMode                    = runMode
        self.limit_mode                 = limit_mode
        self.conf                       = conf
        self.addin                      = addin
        self.log_queue                  = log_queue

        # ログ
        self.proc_name = 'bot'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')
        
        if (conf is not None):
            self.cgpt_secure_level          = conf.cgpt_secure_level
            self.cgpt_functions_path        = conf.cgpt_functions_path

            self.cgpt_engine_greeting       = conf.cgpt_engine_greeting
            self.cgpt_engine_chat           = conf.cgpt_engine_chat
            self.cgpt_engine_vision         = conf.cgpt_engine_vision
            self.cgpt_engine_fileSearch     = conf.cgpt_engine_fileSearch
            self.cgpt_engine_webSearch      = conf.cgpt_engine_webSearch
            self.cgpt_engine_assistant      = conf.cgpt_engine_assistant

            self.openai_api_type            = conf.openai_api_type
            self.openai_default_gpt         = conf.openai_default_gpt
            #self.openai_default_class       = conf.openai_default_class
            #self.openai_auto_continue       = conf.openai_auto_continue
            #self.openai_max_step            = conf.openai_max_step
            #self.openai_max_session         = conf.openai_max_session

            #self.freeai_api_type            = conf._api_type
            #self.freeai_default_gpt         = conf._default_gpt
            #self.freeai_default_class       = conf._default_class
            #self.freeai_auto_continue       = conf._auto_continue
            #self.freeai_max_step            = conf._max_step
            #self.freeai_max_session         = conf.freeai_max_session
            #self.freeai_max_wait_sec        = conf.freeai_max_wait_sec

            #self.ollama_api_type            = conf.ollama_api_type
            #self.ollama_default_gpt         = conf.ollama_default_gpt
            #self.ollama_default_class       = conf.ollama_default_class
            #self.ollama_auto_continue       = conf.ollama_auto_continue
            #self.ollama_max_step            = conf.ollama_max_step
            #self.ollama_max_session         = conf.ollama_max_session
            #self.ollama_max_wait_sec        = conf.ollama_max_wait_sec

            self.openai_organization        = conf.openai_organization
            self.openai_key_id              = conf.openai_key_id
            self.azure_endpoint             = conf.azure_endpoint
            self.azure_version              = conf.azure_version
            self.azure_key_id               = conf.azure_key_id
            self.freeai_key_id              = conf.freeai_key_id
            self.ollama_server              = conf.ollama_server
            self.ollama_port                = conf.ollama_port

            self.openai_nick_name           = conf.openai_nick_name
            self.openai_model               = conf.openai_model
            self.openai_token               = conf.openai_token
            self.openai_temperature         = conf.openai_temperature
            self.openai_max_step            = conf.openai_max_step 
            self.openai_inpLang             = conf.openai_inpLang
            self.openai_outLang             = conf.openai_outLang

            self.freeai_nick_name           = conf.freeai_nick_name
            self.freeai_model               = conf.freeai_model
            self.freeai_token               = conf.freeai_token
            self.freeai_temperature         = conf.freeai_temperature
            self.freeai_max_step            = conf.freeai_max_step 
            self.freeai_inpLang             = conf.freeai_inpLang
            self.freeai_outLang             = conf.freeai_outLang

            self.ollama_nick_name           = conf.ollama_nick_name
            self.ollama_model               = conf.ollama_model
            self.ollama_token               = conf.ollama_token
            self.ollama_temperature         = conf.ollama_temperature
            self.ollama_max_step            = conf.ollama_max_step 
            #self.ollama_max_wait_sec        = conf.ollama_max_wait_sec
            self.ollama_inpLang             = conf.ollama_inpLang
            self.ollama_outLang             = conf.ollama_outLang

        if(qHOSTNAME in use_ollama_server_list):
            if (self.ollama_server == 'auto'):
                self.ollama_server          = use_ollama_server_ip

        # function 定義
        self.botFunc = speech_bot_function.botFunction()
        self.botFunc.init()

        # OPENAI 定義
        self.openaiAPI = speech_bot_openai.ChatBotAPI()
        self.openaiAPI.init(log_queue=log_queue, )

        # OPENAI 認証

        openai_api_type = openai_key.getkey('chatgpt','openai_api_type')
        if  (self.openai_api_type != ''):
            openai_api_type = self.openai_api_type
        
        openai_default_gpt = openai_key.getkey('chatgpt','openai_default_gpt')
        if  (self.openai_default_gpt != ''):
            openai_default_gpt = self.openai_default_gpt

        openai_default_class = openai_key.getkey('chatgpt','openai_default_class')
        if  (self.openai_default_class != ''):
            openai_default_class = self.openai_default_class

        openai_auto_continue = openai_key.getkey('chatgpt','openai_auto_continue')
        if  (self.openai_auto_continue != ''):
            openai_auto_continue = self.openai_auto_continue

        openai_max_step = openai_key.getkey('chatgpt','openai_max_step')
        if  (self.openai_max_step != ''):
            openai_max_step = self.openai_max_step

        openai_max_session = openai_key.getkey('chatgpt','openai_max_session')
        if  (self.openai_max_session != ''):
            openai_max_session = self.openai_max_session

        openai_organization = openai_key.getkey('chatgpt','openai_organization')
        if  (self.openai_organization != '< your openai organization >') \
        and (self.openai_organization != ''):
            openai_organization = self.openai_organization

        openai_key_id = openai_key.getkey('chatgpt','openai_key_id')
        if  (self.openai_key_id != '< your openai key >') \
        and (self.openai_key_id != ''):
            openai_key_id = self.openai_key_id

        azure_endpoint = openai_key.getkey('chatgpt','azure_endpoint')
        if  (self.azure_endpoint != '< your azure endpoint base >') \
        and (self.azure_endpoint != ''):
            azure_endpoint = self.azure_endpoint

        azure_version = openai_key.getkey('chatgpt','azure_version')
        if  (self.azure_version != 'yyyy-mm-dd') \
        and (self.azure_version != ''):
            azure_version = self.azure_version

        azure_key_id = openai_key.getkey('chatgpt','azure_key_id')
        if  (self.azure_key_id != '< your azure key >') \
        and (self.azure_key_id != ''):
            azure_key_id = self.azure_key_id

        if (openai_api_type != 'azure'):
            gpt_a_nick_name = openai_key.getkey('chatgpt','gpt_a_nick_name')
            gpt_a_model1    = openai_key.getkey('chatgpt','gpt_a_model1')
            gpt_a_token1    = openai_key.getkey('chatgpt','gpt_a_token1')
            gpt_a_model2    = openai_key.getkey('chatgpt','gpt_a_model2')
            gpt_a_token2    = openai_key.getkey('chatgpt','gpt_a_token2')
            gpt_a_model3    = openai_key.getkey('chatgpt','gpt_a_model3')
            gpt_a_token3    = openai_key.getkey('chatgpt','gpt_a_token3')
            gpt_b_nick_name = openai_key.getkey('chatgpt','gpt_b_nick_name')
            gpt_b_model1    = openai_key.getkey('chatgpt','gpt_b_model1')
            gpt_b_token1    = openai_key.getkey('chatgpt','gpt_b_token1')
            gpt_b_model2    = openai_key.getkey('chatgpt','gpt_b_model2')
            gpt_b_token2    = openai_key.getkey('chatgpt','gpt_b_token2')
            gpt_b_model3    = openai_key.getkey('chatgpt','gpt_b_model3')
            gpt_b_token3    = openai_key.getkey('chatgpt','gpt_b_token3')
            gpt_b_length    = openai_key.getkey('chatgpt','gpt_b_length')
            gpt_v_nick_name = openai_key.getkey('chatgpt','gpt_v_nick_name')
            gpt_v_model     = openai_key.getkey('chatgpt','gpt_v_model')
            gpt_v_token     = openai_key.getkey('chatgpt','gpt_v_token')
            gpt_x_nick_name = openai_key.getkey('chatgpt','gpt_x_nick_name')
            gpt_x_model1    = openai_key.getkey('chatgpt','gpt_x_model1')
            gpt_x_token1    = openai_key.getkey('chatgpt','gpt_x_token1')
            gpt_x_model2    = openai_key.getkey('chatgpt','gpt_x_model2')
            gpt_x_token2    = openai_key.getkey('chatgpt','gpt_x_token2')
        else:
            gpt_a_nick_name = openai_key.getkey('chatgpt','azure_a_nick_name')
            gpt_a_model1    = openai_key.getkey('chatgpt','azure_a_model1')
            gpt_a_token1    = openai_key.getkey('chatgpt','azure_a_token1')
            gpt_a_model2    = openai_key.getkey('chatgpt','azure_a_model2')
            gpt_a_token2    = openai_key.getkey('chatgpt','azure_a_token2')
            gpt_a_model3    = openai_key.getkey('chatgpt','azure_a_model3')
            gpt_a_token3    = openai_key.getkey('chatgpt','azure_a_token3')
            gpt_b_nick_name = openai_key.getkey('chatgpt','azure_b_nick_name')
            gpt_b_model1    = openai_key.getkey('chatgpt','azure_b_model1')
            gpt_b_token1    = openai_key.getkey('chatgpt','azure_b_token1')
            gpt_b_model2    = openai_key.getkey('chatgpt','azure_b_model2')
            gpt_b_token2    = openai_key.getkey('chatgpt','azure_b_token2')
            gpt_b_model3    = openai_key.getkey('chatgpt','azure_b_model3')
            gpt_b_token3    = openai_key.getkey('chatgpt','azure_b_token3')
            gpt_b_length    = openai_key.getkey('chatgpt','azure_b_length')
            gpt_v_nick_name = openai_key.getkey('chatgpt','azure_v_nick_name')
            gpt_v_model     = openai_key.getkey('chatgpt','azure_v_model')
            gpt_v_token     = openai_key.getkey('chatgpt','azure_v_token')
            gpt_x_nick_name = openai_key.getkey('chatgpt','azure_x_nick_name')
            gpt_x_model1    = openai_key.getkey('chatgpt','azure_x_model1')
            gpt_x_token1    = openai_key.getkey('chatgpt','azure_x_token1')
            gpt_x_model2    = openai_key.getkey('chatgpt','azure_x_model2')
            gpt_x_token2    = openai_key.getkey('chatgpt','azure_x_token2')

        # 利用制限
        if (self.limit_mode == True):
                openai_default_gpt  = 'auto'
                limited_nick_name   = 'GPT'
                limited_model       = gpt_a_model1
                limited_token       = '1000'

                gpt_a_nick_name     = limited_nick_name
                gpt_a_model1        = limited_model
                gpt_a_model2        = limited_model
                gpt_a_model3        = limited_model
                gpt_a_token1        = limited_token
                gpt_a_token2        = limited_token
                gpt_a_token3        = limited_token
                gpt_b_nick_name     = limited_nick_name
                gpt_b_model1        = limited_model
                gpt_b_model2        = limited_model
                gpt_b_model3        = limited_model
                gpt_b_token1        = limited_token
                gpt_b_token2        = limited_token
                gpt_b_token3        = limited_token
                gpt_v_nick_name     = limited_nick_name
                gpt_v_model         = limited_model
                gpt_v_token         = limited_token
                gpt_x_nick_name     = limited_nick_name
                gpt_x_model1        = limited_model
                gpt_x_model2        = limited_model
                gpt_x_token1        = limited_token
                gpt_x_token2        = limited_token

        else:
            if  (self.openai_model != ''):
                limited_nick_name   = 'GPT'
                limited_model       = self.openai_model
                limited_token       = self.openai_token

                gpt_a_nick_name     = limited_nick_name
                gpt_a_model1        = limited_model
                gpt_a_model2        = limited_model
                gpt_a_model3        = limited_model
                gpt_a_token1        = limited_token
                gpt_a_token2        = limited_token
                gpt_a_token3        = limited_token
                gpt_b_nick_name     = limited_nick_name
                gpt_b_model1        = limited_model
                gpt_b_model2        = limited_model
                gpt_b_model3        = limited_model
                gpt_b_token1        = limited_token
                gpt_b_token2        = limited_token
                gpt_b_token3        = limited_token
                gpt_v_nick_name     = limited_nick_name
                gpt_v_model         = limited_model
                gpt_v_token         = limited_token
                gpt_x_nick_name     = limited_nick_name
                gpt_x_model1        = limited_model
                gpt_x_model2        = limited_model
                gpt_x_token1        = limited_token
                gpt_x_token2        = limited_token

        #print('openai_api_type', openai_api_type)
        #print('openai_organization', openai_organization)
        #print('openai_key_id', openai_key_id)
        #print('azure_endpoint', azure_endpoint)
        #print('azure_version', azure_version)
        #print('azure_key_id', azure_key_id)

        res = self.openaiAPI.authenticate('chatgpt', openai_api_type, 
                                                     openai_default_gpt, openai_default_class,
                                                     openai_auto_continue,
                                                     openai_max_step, openai_max_session,
                                                     openai_organization, openai_key_id,
                                                     azure_endpoint, azure_version, azure_key_id,
                                                     gpt_a_nick_name,
                                                     gpt_a_model1, gpt_a_token1,
                                                     gpt_a_model2, gpt_a_token2,
                                                     gpt_a_model3, gpt_a_token3,
                                                     gpt_b_nick_name,
                                                     gpt_b_model1, gpt_b_token1,
                                                     gpt_b_model2, gpt_b_token2,
                                                     gpt_b_model3, gpt_b_token3,
                                                     gpt_b_length,
                                                     gpt_v_nick_name,
                                                     gpt_v_model,  gpt_v_token,
                                                     gpt_x_nick_name,
                                                     gpt_x_model1, gpt_x_token1,
                                                     gpt_x_model2, gpt_x_token2,
                                          )
        if (res == True):
            self.openai_enable = True
            self.openai_exec   = True
            qLog.log('info', self.proc_id, 'openai (ChatGPT) authenticate OK!')
        else:
            qLog.log('error', self.proc_id, 'openai (ChatGPT) authenticate NG!')

        # freeai 定義
        self.freeaiAPI = speech_bot_freeai._freeaiAPI()
        self.freeaiAPI.init(log_queue=log_queue, )

        freeai_api_type     = freeai_key.getkey('freeai','freeai_api_type')
        if  (self.freeai_api_type != ''):
            freeai_api_type = self.freeai_api_type

        freeai_default_gpt  = freeai_key.getkey('freeai','freeai_default_gpt')
        if  (self.freeai_default_gpt != ''):
            freeai_default_gpt = self.freeai_default_gpt

        freeai_default_class  = freeai_key.getkey('freeai','freeai_default_class')
        if  (self.freeai_default_class != ''):
            freeai_default_class = self.freeai_default_class

        freeai_auto_continue  = freeai_key.getkey('freeai','freeai_auto_continue')
        if  (self.freeai_auto_continue != ''):
            freeai_auto_continue = self.freeai_auto_continue

        freeai_max_step  = freeai_key.getkey('freeai','freeai_max_step')
        if  (self.freeai_max_step != ''):
            freeai_max_step = self.freeai_max_step

        freeai_max_session  = freeai_key.getkey('freeai','freeai_max_session')
        if  (self.freeai_max_session != ''):
            freeai_max_session = self.freeai_max_session

        freeai_max_wait_sec  = freeai_key.getkey('freeai','freeai_max_wait_sec')
        if  (self.freeai_max_wait_sec != ''):
            freeai_max_wait_sec = self.freeai_max_wait_sec

        freeai_key_id = freeai_key.getkey('freeai','freeai_key_id')
        if  (self.freeai_key_id != '< your freeai key >') \
        and (self.freeai_key_id != ''):
            freeai_key_id = self.freeai_key_id

        freeai_a_nick_name = freeai_key.getkey('freeai','freeai_a_nick_name')
        freeai_a_model     = freeai_key.getkey('freeai','freeai_a_model')
        freeai_a_token     = freeai_key.getkey('freeai','freeai_a_token')
        freeai_a_use_tools = freeai_key.getkey('freeai','freeai_a_use_tools')

        freeai_b_nick_name = freeai_key.getkey('freeai','freeai_b_nick_name')
        freeai_b_model     = freeai_key.getkey('freeai','freeai_b_model')
        freeai_b_token     = freeai_key.getkey('freeai','freeai_b_token')
        freeai_b_use_tools = freeai_key.getkey('freeai','freeai_b_use_tools')

        freeai_v_nick_name = freeai_key.getkey('freeai','freeai_v_nick_name')
        freeai_v_model     = freeai_key.getkey('freeai','freeai_v_model')
        freeai_v_token     = freeai_key.getkey('freeai','freeai_v_token')
        freeai_v_use_tools = freeai_key.getkey('freeai','freeai_v_use_tools')

        freeai_x_nick_name = freeai_key.getkey('freeai','freeai_x_nick_name')
        freeai_x_model     = freeai_key.getkey('freeai','freeai_x_model')
        freeai_x_token     = freeai_key.getkey('freeai','freeai_x_token')
        freeai_x_use_tools = freeai_key.getkey('freeai','freeai_x_use_tools')

        if  (self.freeai_model != ''):
                limited_nick_name   = 'FreeAI'
                limited_model       = self.freeai_model
                limited_token       = self.freeai_token

                freeai_a_nick_name  = limited_nick_name
                freeai_a_model      = limited_model
                freeai_a_token      = limited_token
                freeai_a_use_tools  = 'no'
                freeai_b_nick_name  = limited_nick_name
                freeai_b_model      = limited_model
                freeai_b_token      = limited_token
                freeai_b_use_tools  = 'no'
                freeai_v_nick_name  = limited_nick_name
                freeai_v_model      = limited_model
                freeai_v_token      = limited_token
                freeai_v_use_tools  = 'no'
                freeai_x_nick_name  = limited_nick_name
                freeai_x_model      = limited_model
                freeai_x_token      = limited_token
                freeai_x_use_tools  = 'no'

        # freeai 認証
        res = self.freeaiAPI.authenticate('freeai',
                            freeai_api_type,
                            freeai_default_gpt, freeai_default_class,
                            freeai_auto_continue, freeai_max_step, freeai_max_session,
                            freeai_max_wait_sec,
                            freeai_key_id,
                            freeai_a_nick_name, freeai_a_model, freeai_a_token,
                            freeai_a_use_tools,
                            freeai_b_nick_name, freeai_b_model, freeai_b_token,
                            freeai_b_use_tools,
                            freeai_v_nick_name, freeai_v_model, freeai_v_token,
                            freeai_v_use_tools,
                            freeai_x_nick_name, freeai_x_model, freeai_x_token,
                            freeai_x_use_tools,
                            )
        if (res == True):
            self.freeai_enable = True
            self.freeai_exec   = True
            qLog.log('info', self.proc_id, 'google (FreeAI) authenticate OK!')
        else:
            qLog.log('error', self.proc_id, 'google (FreeAI) authenticate NG!')

        # ollama 定義
        self.ollamaAPI = speech_bot_ollama._ollamaAPI()
        self.ollamaAPI.init(log_queue=log_queue, )

        ollama_api_type     = ollama_key.getkey('ollama','ollama_api_type')
        if  (self.ollama_api_type != ''):
            ollama_api_type = self.ollama_api_type

        ollama_default_gpt  = ollama_key.getkey('ollama','ollama_default_gpt')
        if  (self.ollama_default_gpt != ''):
            ollama_default_gpt = self.ollama_default_gpt

        ollama_default_class  = ollama_key.getkey('ollama','ollama_default_class')
        if  (self.ollama_default_class != ''):
            ollama_default_class = self.ollama_default_class

        ollama_auto_continue  = ollama_key.getkey('ollama','ollama_auto_continue')
        if  (self.ollama_auto_continue != ''):
            ollama_auto_continue = self.ollama_auto_continue

        ollama_max_step  = ollama_key.getkey('ollama','ollama_max_step')
        if  (self.ollama_max_step != ''):
            ollama_max_step = self.ollama_max_step

        ollama_max_session  = ollama_key.getkey('ollama','ollama_max_session')
        if  (self.ollama_max_session != ''):
            ollama_max_session = self.ollama_max_session

        ollama_max_wait_sec  = ollama_key.getkey('ollama','ollama_max_wait_sec')
        if  (self.ollama_max_wait_sec != ''):
            ollama_max_wait_sec = self.ollama_max_wait_sec

        ollama_server = ollama_key.getkey('ollama','ollama_server')
        if  (self.ollama_server != 'auto') \
        and (self.ollama_server != ''):
            ollama_server = self.ollama_server

        ollama_port = ollama_key.getkey('ollama','ollama_port')
        if  (self.ollama_port != 'auto') \
        and (self.ollama_port != ''):
            ollama_port = self.ollama_port

        ollama_a_nick_name = ollama_key.getkey('ollama','ollama_a_nick_name')
        ollama_a_model     = ollama_key.getkey('ollama','ollama_a_model')
        ollama_a_token     = ollama_key.getkey('ollama','ollama_a_token')
        ollama_a_use_tools = ollama_key.getkey('ollama','ollama_a_use_tools')

        ollama_b_nick_name = ollama_key.getkey('ollama','ollama_b_nick_name')
        ollama_b_model     = ollama_key.getkey('ollama','ollama_b_model')
        ollama_b_token     = ollama_key.getkey('ollama','ollama_b_token')
        ollama_b_use_tools = ollama_key.getkey('ollama','ollama_b_use_tools')

        ollama_v_nick_name = ollama_key.getkey('ollama','ollama_v_nick_name')
        ollama_v_model     = ollama_key.getkey('ollama','ollama_v_model')
        ollama_v_token     = ollama_key.getkey('ollama','ollama_v_token')
        ollama_v_use_tools = ollama_key.getkey('ollama','ollama_v_use_tools')

        ollama_x_nick_name = ollama_key.getkey('ollama','ollama_x_nick_name')
        ollama_x_model     = ollama_key.getkey('ollama','ollama_x_model')
        ollama_x_token     = ollama_key.getkey('ollama','ollama_x_token')
        ollama_x_use_tools = ollama_key.getkey('ollama','ollama_x_use_tools')

        if  (self.ollama_model != ''):
                limited_nick_name   = 'ollama'
                limited_model       = self.ollama_model
                limited_token       = self.ollama_token

                ollama_a_nick_name  = limited_nick_name
                ollama_a_model      = limited_model
                ollama_a_token      = limited_token
                ollama_a_use_tools  = 'no'
                ollama_b_nick_name  = limited_nick_name
                ollama_b_model      = limited_model
                ollama_b_token      = limited_token
                ollama_b_use_tools  = 'no'
                ollama_v_nick_name  = limited_nick_name
                ollama_v_model      = limited_model
                ollama_v_token      = limited_token
                ollama_v_use_tools  = 'no'
                ollama_x_nick_name  = limited_nick_name
                ollama_x_model      = limited_model
                ollama_x_token      = limited_token
                ollama_x_use_tools  = 'no'

        # ollama 認証
        res = self.ollamaAPI.authenticate('ollama',
                            ollama_api_type,
                            ollama_default_gpt, ollama_default_class,
                            ollama_auto_continue, ollama_max_step, ollama_max_session,
                            ollama_max_wait_sec,
                            ollama_server, ollama_port,
                            ollama_a_nick_name, ollama_a_model, ollama_a_token,
                            ollama_a_use_tools,
                            ollama_b_nick_name, ollama_b_model, ollama_b_token,
                            ollama_b_use_tools,
                            ollama_v_nick_name, ollama_v_model, ollama_v_token,
                            ollama_v_use_tools,
                            ollama_x_nick_name, ollama_x_model, ollama_x_token,
                            ollama_x_use_tools,
                            )
        if (res == True):
            self.ollama_enable = True
            self.ollama_exec   = True
            qLog.log('info', self.proc_id, f"{ self.ollamaAPI.ollama_server } (ollama) authenticate OK!")
        else:
            qLog.log('error', self.proc_id,f"{ self.ollamaAPI.ollama_server } (ollama) authenticate NG!")

        if (self.openai_enable == True) \
        or (self.freeai_enable == True) \
        or (self.ollama_enable == True):
             self.gpt_enable = True

        return True

    def gpt_history_reset(self, ):
        qLog.log('info', self.proc_id, 'Reset History')
        res = self.openaiAPI.reset()
        res = self.freeaiAPI.reset()
        res = self.ollamaAPI.reset()
        self.history           = []
        self.last_chat_class   = 'chat'
        self.last_model_select = 'auto'
        return True

    def gpt_functions_load(self, ):
        qLog.log('info', self.proc_id, 'Load functions ...')
        res = False
        msg = ''
        if (self.gpt_functions_enable == True):
            res, msg = self.botFunc.functions_load(functions_path=self.cgpt_functions_path, secure_level=self.cgpt_secure_level, )
            res = self.openaiAPI.reset()
            res = self.freeaiAPI.reset()
            res = self.ollamaAPI.reset()
            self.history           = []
            self.last_chat_class   = 'chat'
            self.last_model_select = 'auto'
        return res, msg

    def gpt_functions_reset(self, ):
        qLog.log('info', self.proc_id, 'Reset functions ...')
        res = False
        msg = ''
        if (self.gpt_functions_enable == True):
            res, msg = self.botFunc.functions_reset()
            res = self.openaiAPI.reset()
            res = self.freeaiAPI.reset()
            res = self.ollamaAPI.reset()
            self.history           = []
            self.last_chat_class   = 'chat'
            self.last_model_select = 'auto'
        return res, msg

    def gpt_functions_unload(self, ):
        qLog.log('info', self.proc_id, 'Unload functions ...')
        res = False
        msg = ''
        if (self.gpt_functions_enable == True):
            res, msg = self.botFunc.functions_unload()
            res = self.openaiAPI.reset()
            res = self.freeaiAPI.reset()
            res = self.ollamaAPI.reset()
            self.history           = []
            self.last_chat_class   = 'chat'
            self.last_model_select = 'auto'
        return res, msg



    def history_zip1(self, history=[]):
        res_history = history

        if (len(res_history) > 0):
            for h in reversed(range(len(res_history))):
                tm = res_history[h]['time']
                if ((time.time() - tm) > 900): #15分で忘れてもらう
                    if (h != 0):
                        del res_history[h]
                    else:
                        if (res_history[0]['role'] != 'system'):
                            del res_history[0]

        return res_history

    def history_zip2(self, history=[], leave_count=4, ):
        res_history = history

        if (len(res_history) > 6):
            for h in reversed(range(2, len(res_history) - leave_count)):
                del res_history[h]

        return res_history

    def files_check(self, filePath=[], ):
        upload_files = []
        image_urls   = []

        # filePath確認
        if (len(filePath) > 0):
            try:

                for file_name in filePath:
                    if (os.path.isfile(file_name)):
                        if (os.path.getsize(file_name) <= 20000000):

                            upload_files.append(file_name)
                            file_ext = os.path.splitext(file_name)[1][1:].lower()
                            if (file_ext in ('jpg', 'jpeg', 'png')):
                                base64_text = base64_encode(file_name)
                                if (file_ext in ('jpg', 'jpeg')):
                                    url = {"url": f"data:image/jpeg;base64,{base64_text}"}
                                    image_url = {'type':'image_url', 'image_url': url}
                                    image_urls.append(image_url)
                                if (file_ext == 'png'):
                                    url = {"url": f"data:image/png;base64,{base64_text}"}
                                    image_url = {'type':'image_url', 'image_url': url}
                                    image_urls.append(image_url)

            except Exception as e:
                print(e)

        return upload_files, image_urls

    def model_check(self, chat_class='auto', model_select='auto',
                    session_id='internal', history=[], function_modules={},
                    sysText=None, reqText=None, inpText='こんにちは', 
                    upload_files=[], image_urls=[], ):

        # 戻り値
        chat_class   = chat_class
        model_select = model_select
        nick_name    = None
        model_name   = None
        res_engine   = 'auto'

        # model 指定
        if (model_select == 'auto'):
            if (self.openaiAPI.gpt_x_nick_name != ''):
                if (inpText.strip()[:len(self.openaiAPI.gpt_x_nick_name)+1].lower() == (self.openaiAPI.gpt_x_nick_name.lower() + ',')):

                    chat_class   = 'assistant'
                    model_select = 'x'
                    nick_name    = self.openaiAPI.gpt_x_nick_name
                    model_name   = None
                    res_engine   = 'openai'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.openaiAPI.gpt_v_nick_name != ''):
                if (inpText.strip()[:len(self.openaiAPI.gpt_v_nick_name)+1].lower() == (self.openaiAPI.gpt_v_nick_name.lower() + ',')):

                    if  (len(image_urls) == 0):
                        chat_class   = 'assistant'
                        model_select = 'auto'
                        nick_name    = None
                        model_name   = None
                        res_engine   = 'openai'
                        self.print(session_id, f" ClipnGPT: change chat class = [ vision → { chat_class } ]")
                    else:
                        if (len(image_urls) == len(upload_files)):
                            chat_class   = 'vision'
                            model_select = 'v'
                            model_name   = self.openaiAPI.gpt_v_model
                            nick_name    = self.openaiAPI.gpt_v_nick_name
                            res_engine   = 'openai'
                            self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")
                        else:
                            chat_class   = 'assistant'
                            model_select = 'x'
                            model_name   = self.openaiAPI.gpt_x_model2
                            nick_name    = self.openaiAPI.gpt_x_nick_name
                            res_engine   = 'openai'
                            self.print(session_id, f" ClipnGPT: change chat class = [ vision → { chat_class } ]")

        if (model_select == 'auto'):
            if (self.openaiAPI.gpt_b_nick_name != ''):
                if (inpText.strip()[:len(self.openaiAPI.gpt_b_nick_name)+1].lower() == (self.openaiAPI.gpt_b_nick_name.lower() + ',')):

                    chat_class   = 'openai'
                    model_select = 'b'
                    nick_name    = self.openaiAPI.gpt_b_nick_name
                    model_name   = None
                    res_engine   = 'openai'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.openaiAPI.gpt_a_nick_name != ''):
                if (inpText.strip()[:len(self.openaiAPI.gpt_a_nick_name)+1].lower() == (self.openaiAPI.gpt_a_nick_name.lower() + ',')):

                    chat_class   = 'openai'
                    model_select = 'a'
                    nick_name    = self.openaiAPI.gpt_a_nick_name
                    model_name   = None
                    res_engine   = 'openai'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.freeaiAPI.freeai_x_nick_name != ''):
                if (inpText.strip()[:len(self.freeaiAPI.freeai_x_nick_name)+1].lower() == (self.freeaiAPI.freeai_x_nick_name.lower() + ',')):

                    chat_class   = self.freeaiAPI.freeai_x_nick_name.lower()
                    model_select = 'x'
                    nick_name    = self.freeaiAPI.freeai_x_nick_name
                    model_name   = None
                    res_engine   = 'freeai'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.freeaiAPI.freeai_v_nick_name != ''):
                if (inpText.strip()[:len(self.freeaiAPI.freeai_v_nick_name)+1].lower() == (self.freeaiAPI.freeai_v_nick_name.lower() + ',')):

                    if  (len(image_urls) > 0) \
                    and (len(image_urls) == len(upload_files)):
                        #chat_class   = self.freeaiAPI.freeai_v_nick_name.lower()
                        chat_class   = 'freeai'
                        model_select = 'v'
                        nick_name    = self.freeaiAPI.freeai_v_nick_name
                        model_name   = None
                        res_engine   = 'freeai'
                        self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")
                    else:
                        chat_class   = self.freeaiAPI.freeai_x_nick_name.lower()
                        model_select = 'x'
                        nick_name    = self.freeaiAPI.freeai_x_nick_name
                        model_name   = None
                        res_engine   = 'freeai'
                        self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.freeaiAPI.freeai_b_nick_name != ''):
                if (inpText.strip()[:len(self.freeaiAPI.freeai_b_nick_name)+1].lower() == (self.freeaiAPI.freeai_b_nick_name.lower() + ',')):

                    #chat_class   = self.freeaiAPI.freeai_b_nick_name.lower()
                    chat_class   = 'freeai'
                    model_select = 'b'
                    nick_name    = self.freeaiAPI.freeai_b_nick_name
                    model_name   = None
                    res_engine   = 'freeai'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.freeaiAPI.freeai_a_nick_name != ''):
                if (inpText.strip()[:len(self.freeaiAPI.freeai_a_nick_name)+1].lower() == (self.freeaiAPI.freeai_a_nick_name.lower() + ',')):

                    chat_class   = self.freeaiAPI.freeai_a_nick_name.lower()
                    model_select = 'a'
                    nick_name    = self.freeaiAPI.freeai_a_nick_name
                    model_name   = None
                    res_engine   = 'freeai'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.ollamaAPI.ollama_x_nick_name != ''):
                if (inpText.strip()[:len(self.ollamaAPI.ollama_x_nick_name)+1].lower() == (self.ollamaAPI.ollama_x_nick_name.lower() + ',')):

                    chat_class   = 'ollama'
                    model_select = 'x'
                    nick_name    = self.ollamaAPI.ollama_b_nick_name
                    model_name   = None
                    res_engine   = 'ollama'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.ollamaAPI.ollama_v_nick_name != ''):
                if (inpText.strip()[:len(self.ollamaAPI.ollama_v_nick_name)+1].lower() == (self.ollamaAPI.ollama_v_nick_name.lower() + ',')):

                    if  (len(image_urls) > 0) \
                    and (len(image_urls) == len(upload_files)):
                        chat_class   = 'ollama'
                        model_select = 'v'
                        nick_name    = self.ollamaAPI.ollama_v_nick_name
                        model_name   = None
                        res_engine   = 'ollama'
                        self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")
                    else:
                        chat_class   = 'ollama'
                        model_select = 'x'
                        nick_name    = self.ollamaAPI.ollama_b_nick_name
                        model_name   = None
                        res_engine   = 'ollama'
                        self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.ollamaAPI.ollama_b_nick_name != ''):
                if (inpText.strip()[:len(self.ollamaAPI.ollama_b_nick_name)+1].lower() == (self.ollamaAPI.ollama_b_nick_name.lower() + ',')):

                    chat_class   = 'ollama'
                    model_select = 'b'
                    nick_name    = self.ollamaAPI.ollama_b_nick_name
                    model_name   = None
                    res_engine   = 'ollama'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (model_select == 'auto'):
            if (self.ollamaAPI.ollama_a_nick_name != ''):
                if (inpText.strip()[:len(self.ollamaAPI.ollama_a_nick_name)+1].lower() == (self.ollamaAPI.ollama_a_nick_name.lower() + ',')):

                    chat_class   = 'ollama'
                    model_select = 'a'
                    nick_name    = self.ollamaAPI.ollama_a_nick_name
                    model_name   = None
                    res_engine   = 'ollama'
                    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        # チャットクラス指定
        if (chat_class == 'auto'):
            if (inpText.strip()[:5].lower() == ('riki,')):

                chat_class   = 'assistant'
                model_select = 'x'
                model_name   = self.openaiAPI.gpt_x_model2
                nick_name    = self.openaiAPI.gpt_x_nick_name
                res_engine   = 'openai'
                self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (chat_class == 'auto'):
            if (inpText.strip()[:10].lower() == ('assistant,')):

                chat_class   = 'assistant'
                model_select = 'x'
                model_name   = self.openaiAPI.gpt_x_model2
                nick_name    = self.openaiAPI.gpt_x_nick_name
                res_engine   = 'openai'
                self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (chat_class == 'auto'):
            if (inpText.strip()[:7].lower() == ('vision,')):

                if  (len(image_urls) == 0):
                    chat_class   = 'assistant'
                    model_select = 'auto'
                    nick_name    = None
                    model_name   = None
                    res_engine   = 'openai'
                    self.print(session_id, f" ClipnGPT: change chat class = [ vision → { chat_class } ]")
                else:
                    if (len(image_urls) == len(upload_files)):
                        chat_class   = 'vision'
                        model_select = 'v'
                        model_name   = self.openaiAPI.gpt_v_model
                        nick_name    = self.openaiAPI.gpt_v_nick_name
                        res_engine   = 'openai'
                        self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")
                    else:
                        chat_class   = 'assistant'
                        model_select = 'x'
                        model_name   = self.openaiAPI.gpt_x_model2
                        nick_name    = self.openaiAPI.gpt_x_nick_name
                        res_engine   = 'openai'
                        self.print(session_id, f" ClipnGPT: change chat class = [ vision → { chat_class } ]")

        if (chat_class == 'auto'):
            if (inpText.strip()[:7].lower() == ('openai,')):

                chat_class   = 'openai'
                model_select = 'auto'
                nick_name    = None
                model_name   = None
                res_engine   = 'openai'
                self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (chat_class == 'auto'):
            if (inpText.strip()[:7].lower() == ('freeai,')):

                chat_class   = 'freeai'
                model_select = 'auto'
                nick_name    = None
                model_name   = None
                res_engine   = 'freeai'
                self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (chat_class == 'auto'):
            if (inpText.strip()[:5].lower() == ('free,')):

                chat_class   = 'freeai'
                model_select = 'auto'
                nick_name    = None
                model_name   = None
                res_engine   = 'freeai'
                self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (chat_class == 'auto'):
            if (inpText.strip()[:7].lower() == ('ollama,')):

                chat_class   = 'ollama'
                model_select = 'auto'
                nick_name    = None
                model_name   = None
                res_engine   = 'ollama'
                self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (chat_class == 'auto'):
            if (inpText.strip()[:6].lower() == ('local,')):

                chat_class   = 'ollama'
                model_select = 'auto'
                nick_name    = None
                model_name   = None
                res_engine   = 'ollama'
                self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (chat_class == 'auto'):
            if  (len(upload_files) > 0) \
            and (len(image_urls) == len(upload_files)):
                chat_class   = 'vision'
                model_select = 'v'
                model_name   = self.openaiAPI.gpt_v_model
                nick_name    = self.openaiAPI.gpt_v_nick_name
                res_engine   = 'auto'
                self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")
            #else:
            #    chat_class   = 'assistant'
            #    model_select = 'x'
            #    model_name   = self.openaiAPI.gpt_x_model2
            #    nick_name    = self.openaiAPI.gpt_x_nick_name
            #    res_engine   = 'openai'
            #    self.print(session_id, f" ClipnGPT: user chat class = [ { chat_class } ]")

        if (self.openai_exec == True) \
        or (self.ollama_exec == True):

            if  (res_engine == 'openai') and (self.openai_exec != True):

                if  (self.freeai_exec == True):
                    if (chat_class != 'freeai'):
                        self.print(session_id, f" ClipnGPT: change chat class = [ { chat_class } → freeai ]")
                    chat_class   = 'freeai'
                    model_select = 'auto'
                    model_name   = None
                    nick_name    = None
                    res_engine   = 'freeai'

            if (self.openai_exec != True) and (self.freeai_exec != True):

                if (chat_class != 'ollama'):
                    self.print(session_id, f" ClipnGPT: change chat class = [ { chat_class } → ollama ]")
                chat_class   = 'ollama'
                model_select = 'auto'
                model_name   = None
                nick_name    = None
                res_engine   = 'ollama'

        # エンジン
        if (res_engine == 'auto'):
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

        # チャットクラス判定
        if (chat_class == 'auto'):
            wk_jsonSchema = '{"chat_class": str}'
            wk_sysText = \
"""
あなたは、会話履歴と最後のユーザー入力から適切な会話クラスに分類します。
回答は以下のjsonスキーマ形式でお願いします。
'{"chat_class": str}'
"""
            wk_reqText = \
"""
会話クラスの回答は必ず日本語の単語、"簡単な挨拶","複雑な挨拶","会話の続き","画像分析","コード生成","コード実行",
"ウェブ検索","文書検索","簡単な会話","複雑な会話","アシスタント"または"その他"の何れかに分類お願いします。
"""
            wk_inpText  = "''' 最後のユーザー入力 \n"
            wk_inpText += inpText + '\n'
            wk_inpText += "''' \n"

            # history 圧縮 (最後４つ残す)
            old_history = self.history_zip2(history=history, )
            wk_history  = ''
            if (len(old_history) > 2):
                for m in range(len(old_history) - 1):
                    role    = str(old_history[m].get('role', ''))
                    content = str(old_history[m].get('content', ''))
                    name    = str(old_history[m].get('name', ''))
                    if (role != 'system'):
                        # 全てユーザーメッセージにて処理
                        if (name is None) or (name == ''):
                            wk_history += '(' + role + ')' + '\n'
                            wk_history += content + '\n\n'

            # 拡張アドイン エンジン選択(1)
            if (self.addin is not None):
                addin_module = self.addin.addin_modules.get('addin_engine_selector', None)
                if (addin_module is not None):

                    res_json = None
                    try:
                        if (addin_module['onoff'] == 'on'):
                            dic = {}
                            dic['runStep']           = '1'
                            dic['openai_exec']       = str(self.openai_exec)
                            dic['freeai_exec']       = str(self.freeai_exec)
                            dic['ollama_exec']       = str(self.ollama_exec)
                            dic['engine_greeting']   = self.cgpt_engine_greeting
                            dic['engine_chat']       = self.cgpt_engine_chat
                            dic['engine_vision']     = self.cgpt_engine_vision
                            dic['engine_fileSearch'] = self.cgpt_engine_fileSearch
                            dic['engine_webSearch']  = self.cgpt_engine_webSearch
                            dic['engine_assistant']  = self.cgpt_engine_assistant
                            dic['step1_historyText'] = wk_history
                            dic['step1_inpText']     = inpText
                            json_dump = json.dumps(dic, ensure_ascii=False, )

                            func_proc = addin_module['func_proc']
                            res_json  = func_proc(json_dump)
                    except Exception as e:
                        print(e)
                        res_json = None

                    if (res_json is not None):
                        args_dic = json.loads(res_json)
                        wk_sysText = args_dic.get('sysText', '')
                        wk_reqText = args_dic.get('reqText', '')
                        wk_inpText = args_dic.get('inpText', '')
                        res_engine = args_dic.get('engine', res_engine)

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

            # モデル判定 freeai
            if (res_engine == 'freeai') and (self.freeai_exec == True):

                self.freeaiAPI.seq = self.seq
                wk_json, wk_path, wk_files, wk_nick_name, wk_model_name, _ = \
                self.freeaiAPI.run_gpt( chat_class='internal', model_select='a',
                                        nick_name=None, model_name=None, 
                                        session_id='internal', history=[], function_modules={},
                                        sysText=wk_sysText, reqText=wk_reqText, inpText=wk_inpText,
                                        upload_files=[], image_urls=[],
                                        jsonSchema=wk_jsonSchema, )
                self.seq = self.freeaiAPI.seq

            # モデル判定 ollama
            elif (res_engine == 'ollama') and (self.ollama_exec == True):

                self.ollamaAPI.seq = self.seq
                wk_json, wk_path, wk_files, wk_nick_name, wk_model_name, _ = \
                self.ollamaAPI.run_gpt( chat_class='internal', model_select='a',
                                        nick_name=None, model_name=None, 
                                        session_id='internal', history=[], function_modules={},
                                        sysText=wk_sysText, reqText=wk_reqText, inpText=wk_inpText,
                                        upload_files=[], image_urls=[],
                                        jsonSchema=wk_jsonSchema, )
                self.seq = self.ollamaAPI.seq

            # モデル判定 OpenAI
            else:

                self.openaiAPI.seq = self.seq
                wk_json, wk_path, wk_files, wk_nick_name, wk_model_name, _ = \
                self.openaiAPI.run_gpt( chat_class='internal', model_select='auto',
                                        nick_name=None, model_name=None, 
                                        session_id='internal', history=[], function_modules={},
                                        sysText=wk_sysText, reqText=wk_reqText, inpText=wk_inpText,
                                        upload_files=[], image_urls=[],
                                        jsonSchema=wk_jsonSchema, )
                self.seq = self.openaiAPI.seq

            chat_class = wk_json
            try:
                args_dic   = json.loads(wk_json)
                chat_class = args_dic.get('chat_class', 'auto')
                model_select = 'auto'
                model_name   = None
                nick_name    = None
            except:
                self.print(session_id, wk_json)

            self.print(session_id, f" ClipnGPT: auto chat class = [ { chat_class } ] ({ wk_model_name })")

            # model 復元
            if (chat_class == 'continue') \
            or (chat_class == '会話の続き'):
                chat_class   = self.last_chat_class
                #model_select = self.last_model_select
                model_select = 'auto'
                model_name   = None
                nick_name    = None

        # 拡張アドイン エンジン選択(2)
        new_class = chat_class
        if (self.addin is not None):
            addin_module = self.addin.addin_modules.get('addin_engine_selector', None)
            if (addin_module is not None):

                    res_json = None
                    try:
                        if (addin_module['onoff'] == 'on'):
                            dic = {}
                            dic['runStep']           = '2'
                            dic['openai_exec']       = str(self.openai_exec)
                            dic['freeai_exec']       = str(self.freeai_exec)
                            dic['ollama_exec']       = str(self.ollama_exec)
                            dic['engine_greeting']   = self.cgpt_engine_greeting
                            dic['engine_chat']       = self.cgpt_engine_chat
                            dic['engine_vision']     = self.cgpt_engine_vision
                            dic['engine_fileSearch'] = self.cgpt_engine_fileSearch
                            dic['engine_webSearch']  = self.cgpt_engine_webSearch
                            dic['engine_assistant']  = self.cgpt_engine_assistant
                            dic['step2_class']       = chat_class
                            json_dump = json.dumps(dic, ensure_ascii=False, )

                            func_proc = addin_module['func_proc']
                            res_json  = func_proc(json_dump)
                    except Exception as e:
                        print(e)
                        res_json = None

                    if (res_json is not None):
                        args_dic = json.loads(res_json)
                        new_class   = args_dic.get('class', chat_class)
                        res_engine  = args_dic.get('engine', res_engine)

        if (new_class != chat_class):
            self.print(session_id, f" ClipnGPT: change chat class = [ { chat_class } → { new_class } ]")
            chat_class   = new_class
            model_select = 'auto'
            model_name   = None
            nick_name    = None

        # model 保管
        if  (chat_class != 'continue') \
        and (chat_class != '会話の続き'):
            self.last_chat_class   = chat_class
            self.last_model_select = model_select

        #print(chat_class, model_select, model_name)

        return chat_class, model_select, nick_name, model_name, res_engine

    def chatBot(self, chat_class='auto', model_select='auto',
                session_id='admin', history=[], function_modules={},
                sysText=None, reqText=None, inpText='こんにちは', 
                filePath=[],
                temperature=0.8, max_step=10, inpLang='ja-JP', outLang='ja-JP', ):

        # 戻り値
        res_text        = ''
        res_path        = ''
        res_files       = []
        nick_name       = None
        model_name      = None
        res_history     = history

        if (sysText is None) or (sysText == ''):
            sysText = 'あなたは教師のように話す賢いアシスタントです。'

        # ファイル分離
        upload_files    = []
        image_urls      = []
        try:
            upload_files, image_urls = self.files_check(filePath=filePath, )
        except Exception as e:
            print(e)

        # 実行モデル判定
        try:
            run_engine = 'auto'
            chat_class, model_select, nick_name, model_name, run_engine = \
            self.model_check(   chat_class=chat_class, model_select=model_select, 
                                session_id='internal', history=[], function_modules={}, 
                                sysText=sysText, reqText=reqText, inpText=inpText, 
                                upload_files=upload_files, image_urls=image_urls, )
        except Exception as e:
            print(e)

        # freeai
        if (run_engine == 'freeai') and (self.freeai_exec == True):

                #try:
                    self.freeaiAPI.seq = self.seq
                    res_text, res_path, res_files, nick_name, model_name, res_history = \
                    self.freeaiAPI.run_gpt( chat_class=chat_class, model_select=model_select,
                                            nick_name=nick_name, model_name=model_name,
                                            session_id=session_id, history=res_history, function_modules=function_modules,
                                            sysText=sysText, reqText=reqText, inpText=inpText,
                                            upload_files=upload_files, image_urls=image_urls,
                                            temperature=self.freeaiAPI.temperature, max_step=self.freeaiAPI.freeai_max_step, )
                    self.seq = self.freeaiAPI.seq
                    self.openaiAPI.assistant_id = {}
                    self.openaiAPI.thread_id    = {}

                #except Exception as e:
                #    print(e)

        # ollama
        elif (run_engine == 'ollama') and (self.ollama_exec == True):

                #try:
                    self.ollamaAPI.seq = self.seq
                    res_text, res_path, res_files, nick_name, model_name, res_history = \
                    self.ollamaAPI.run_gpt( chat_class=chat_class, model_select=model_select,
                                            nick_name=nick_name, model_name=model_name,
                                            session_id=session_id, history=res_history, function_modules=function_modules,
                                            sysText=sysText, reqText=reqText, inpText=inpText,
                                            upload_files=upload_files, image_urls=image_urls,
                                            temperature=self.ollamaAPI.temperature, max_step=self.ollamaAPI.ollama_max_step, )
                    self.seq = self.ollamaAPI.seq
                    self.openaiAPI.assistant_id = {}
                    self.openaiAPI.thread_id    = {}

                #except Exception as e:
                #    print(e)

        # OpenAI
        else:

            # ChatGPT
            if  ((chat_class != 'assistant') \
            and  (chat_class != 'コード生成') \
            and  (chat_class != 'コード実行') \
            and  (chat_class != '文書検索') \
            and  (chat_class != '複雑な会話') \
            and  (chat_class != 'アシスタント') \
            and  (model_select != 'x')):
                #try:
                    self.openaiAPI.seq = self.seq
                    res_text, res_path, res_files, nick_name, model_name, res_history = \
                    self.openaiAPI.run_gpt( chat_class=chat_class, model_select=model_select,
                                            nick_name=nick_name, model_name=model_name,
                                            session_id=session_id, history=res_history, function_modules=function_modules,
                                            sysText=sysText, reqText=reqText, inpText=inpText,
                                            upload_files=upload_files, image_urls=image_urls,
                                            temperature=self.openaiAPI.temperature, max_step=self.openaiAPI.max_step, )
                    self.seq = self.openaiAPI.seq
                    self.openaiAPI.assistant_id = {}
                    self.openaiAPI.thread_id    = {}
                #except Exception as e:
                #    print(e)

            # Assistant
            else:
                #try:
                    self.openaiAPI.seq = self.seq
                    res_text, res_path, res_files, nick_name, model_name, res_history = \
                    self.openaiAPI.auto_assistant(  chat_class=chat_class, model_select=model_select,
                                                    nick_name=nick_name, model_name=model_name,
                                                    session_id=session_id, history=res_history, function_modules=function_modules,
                                                    sysText=sysText, reqText=reqText, inpText=inpText,
                                                    upload_files=upload_files, image_urls=image_urls,
                                                    temperature=self.openaiAPI.temperature, max_step=self.openaiAPI.max_step, )
                    self.seq = self.openaiAPI.seq
                #except Exception as e:
                #    print(e)

        # 文書成形
        text = self.text_replace(text=res_text, )
        if (text.strip() != ''):
            res_text = text
        else:
            res_text = '!'

        return res_text, res_path, res_files, nick_name, model_name, res_history



if __name__ == '__main__':

    chatbot = _bot()

    # 初期化
    chatbot.init(qLog_fn='', runMode='debug', limit_mode=False, 
                 conf=None, log_queue=None, )

    # 拡張ファンクション有効
    chatbot.gpt_functions_enable = True

    # ロード
    chatbot.gpt_functions_load()
    function_modules = {}
    for key, module_dic in chatbot.botFunc.function_modules.items():
        if (module_dic['onoff'] == 'on'):
            function_modules[key] = module_dic

    # openai テスト
    if True:
        sysText = None
        reqText = ''
        inpText = 'gpt,おはようございます'
        print()
        print('[Request]')
        print(reqText, inpText )
        print()

        res_text, res_path, res_files, res_name, res_api, res_history = \
        chatbot.chatBot(chat_class='auto', model_select='auto',
                        session_id='admin', history=chatbot.history, function_modules=function_modules,
                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=[],
                        temperature=chatbot.openai_temperature, max_step=chatbot.openai_max_step,        
                        inpLang=chatbot.openai_inpLang, outLang=chatbot.openai_outLang, )
        chatbot.history = res_history

        print()
        print(f"[{ res_name }] ({ res_api })")
        print(res_text)
        print()

    # freeai テスト
    if True:
        sysText = None
        reqText = ''
        inpText = 'free,おはようございます'
        print()
        print('[Request]')
        print(reqText, inpText )
        print()

        res_text, res_path, res_files, res_name, res_api, res_history = \
        chatbot.chatBot(chat_class='auto', model_select='auto',
                        session_id='admin', history=chatbot.history, function_modules=function_modules,
                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=[],
                        temperature=chatbot.freeai_temperature, max_step=chatbot.freeai_max_step,
                        inpLang=chatbot.freeai_inpLang, outLang=chatbot.freeai_outLang, )
        chatbot.history = res_history

        print()
        print(f"[{ res_name }] ({ res_api })")
        print(res_text)
        print()

    # ollama テスト
    if False:
        sysText = None
        reqText = ''
        inpText = 'olm-a,おはようございます'
        print()
        print('[Request]')
        print(reqText, inpText )
        print()

        res_text, res_path, res_files, res_name, res_api, res_history = \
        chatbot.chatBot(chat_class='auto', model_select='auto',
                        session_id='admin', history=chatbot.history, function_modules=function_modules,
                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=[],
                        temperature=chatbot.ollama_temperature, max_step=chatbot.ollama_max_step,
                        inpLang=chatbot.ollama_inpLang, outLang=chatbot.ollama_outLang, )
        chatbot.history = res_history

        print()
        print(f"[{ res_name }] ({ res_api })")
        print(res_text)
        print()

    # リセット
    if False:
        chatbot.gpt_functions_reset()

    # アンロード
    if False:
        chatbot.gpt_functions_unload()




