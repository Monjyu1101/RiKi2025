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

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# 共通ルーチン
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

import _v6__qRiKi_key
qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()



config_file = 'RiKi_ClipnGPT_key.json'



class _conf:

    def __init__(self, ):
            self.runMode                        = 'debug'
            
            self.run_priority                   = 'auto'
            self.cgpt_screen                    = 'auto'
            self.cgpt_panel                     = 'auto'
            self.cgpt_alpha                     = '0.2'

            self.cgpt_guiTheme                  = 'Dark' # 'Default1', 'Dark',
            self.cgpt_keep_on_top               = 'no'
            self.cgpt_secure_level              = 'medium'
            self.cgpt_addins_path               = '_extensions/clipngpt/'
            self.cgpt_functions_path            = '_extensions/function/'

            self.cgpt_engine_greeting           = 'auto'
            self.cgpt_engine_chat               = 'auto'
            self.cgpt_engine_vision             = 'auto'
            self.cgpt_engine_fileSearch         = 'auto'
            self.cgpt_engine_webSearch          = 'auto'
            self.cgpt_engine_assistant          = 'auto'

            self.openai_api_type                = ''
            self.openai_default_gpt             = ''
            self.openai_organization            = '< your openai organization >'
            self.openai_key_id                  = '< your openai key >'
            self.azure_endpoint                 = '< your azure endpoint base >' 
            self.azure_version                  = 'yyyy-mm-dd'
            self.azure_key_id                   = '< your azure key >'
            self.freeai_key_id                  = '< your freeai key >'
            self.ollama_server                  = 'auto'
            self.ollama_port                    = 'auto'

            self.openai_nick_name               = ''
            self.openai_model                   = ''
            self.openai_token                   = ''
            self.openai_temperature             = '0.5'
            self.openai_max_step                = '10'
            self.openai_inpLang                 = 'ja-JP'
            self.openai_outLang                 = 'ja-JP'

            self.freeai_nick_name               = ''
            self.freeai_model                   = ''
            self.freeai_token                   = ''
            self.freeai_temperature             = '0.5'
            self.freeai_max_step                = '10'
            self.freeai_inpLang                 = 'ja-JP'
            self.freeai_outLang                 = 'ja-JP'

            self.ollama_nick_name               = ''
            self.ollama_model                   = ''
            self.ollama_token                   = ''
            self.ollama_temperature             = '0.5'
            self.ollama_max_step                = '10'
            self.ollama_inpLang                 = 'ja-JP'
            self.ollama_outLang                 = 'ja-JP'

            self.restui_start                   = 'auto'
            self.restui_local_ip                = '0.0.0.0'
            self.restui_local_port              = '61101'
            self.restui_allow_ip                = '255.255.255.255'
            self.restui_ssl                     = 'no'
            self.restui_ssl_cert                = '_config/localhost.crt'
            self.restui_ssl_key                 = '_config/localhost.key'
            self.restui_auth_key                = 'secret'

            self.webui_start                    = 'auto'
            self.webui_local_ip                 = '0.0.0.0'
            self.webui_local_port               = '51101'
            self.webui_allow_ip                 = '255.255.255.255'
            self.webui_ssl                      = 'no'
            self.webui_ssl_cert                 = '_config/localhost.crt'
            self.webui_ssl_key                  = '_config/localhost.key'
            self.webui_multi_session            = 10
            self.webui_admin_id                 = 'admin'
            self.webui_admin_pw                 = 'secret'
            self.webui_guest_id                 = 'guest'
            self.webui_guest_pw                 = 'guest'

            self.txt_input_path                 = 'temp/chat_input/'
            self.txt_output_path                = 'temp/chat_output/'
            self.stt_path                       = 'temp/s6_4stt_txt/'
            self.tts_path                       = 'temp/s6_5tts_txt/'
            self.tts_header                     = 'ja,free,'
            self.web_engine                     = 'auto'
            self.web_home                       = 'https://openai.com/blog/chatgpt'
            self.feedback_popup                 = 'no'
            self.feedback_mouse                 = 'yes'
            self.feedback_key                   = 'ctrl'
            self.feedback_sound                 = 'yes'
            self.feedback_sound_accept_file     = '_sounds/_sound_accept.mp3'
            self.feedback_sound_ok_file         = '_sounds/_sound_ok.mp3'
            self.feedback_sound_ng_file         = '_sounds/_sound_ng.mp3'

            self.default_role_text              = 'あなたは美しい日本語を話す賢いアシスタントです。'
            self.default_req_text1              = ''
            self.default_req_text2              = ''
            self.chatbot_role_text              = 'あなたは美しい日本語で楽しく話す賢いアシスタントです。'
            self.chatbot_req_text1              = '以下の呼びかけに楽しい会話が続くように返答してください。'
            self.chatbot_req_text2              = ''

    def init(self, qLog_fn='', runMode='debug',
                    cgpt_screen                 = 'auto',
                    cgpt_panel                  = 'auto',
                    cgpt_alpha                  = '0.2',
            ):
        
        # ログ
        self.proc_name = 'conf'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')

        res, dic = qRiKi_key.getCryptJson(config_file=config_file, auto_crypt=False, )

        if (res == False):
            dic['_crypt_']                      = 'none'
            dic['run_priority']                 = self.run_priority
            dic['cgpt_screen']                  = self.cgpt_screen
            dic['cgpt_panel']                   = self.cgpt_panel
            dic['cgpt_alpha']                   = self.cgpt_alpha

            dic['cgpt_guiTheme']                = self.cgpt_guiTheme
            dic['cgpt_keep_on_top']             = self.cgpt_keep_on_top
            dic['cgpt_secure_level']            = self.cgpt_secure_level
            dic['cgpt_addins_path']             = self.cgpt_addins_path
            dic['cgpt_functions_path']          = self.cgpt_functions_path

            dic['cgpt_engine_greeting']         = self.cgpt_engine_greeting
            dic['cgpt_engine_chat']             = self.cgpt_engine_chat
            dic['cgpt_engine_vision']           = self.cgpt_engine_vision
            dic['cgpt_engine_fileSearch']       = self.cgpt_engine_fileSearch
            dic['cgpt_engine_webSearch']        = self.cgpt_engine_webSearch
            dic['cgpt_engine_assistant']        = self.cgpt_engine_assistant

            dic['openai_api_type']              = self.openai_api_type
            dic['openai_default_gpt']           = self.openai_default_gpt
            dic['openai_organization']          = self.openai_organization
            dic['openai_key_id']                = self.openai_key_id
            dic['azure_endpoint']               = self.azure_endpoint
            dic['azure_version']                = self.azure_version
            dic['azure_key_id']                 = self.azure_key_id
            dic['freeai_key_id']                = self.freeai_key_id
            dic['ollama_server']                = self.ollama_server
            dic['ollama_port']                  = self.ollama_port

            dic['openai_nick_name']             = self.openai_nick_name
            dic['openai_model']                 = self.openai_model
            dic['openai_token']                 = self.openai_token
            dic['openai_temperature']           = self.openai_temperature
            dic['openai_max_step']              = self.openai_max_step
            dic['openai_inpLang']               = self.openai_inpLang
            dic['openai_outLang']               = self.openai_outLang

            dic['freeai_nick_name']             = self.freeai_nick_name
            dic['freeai_model']                 = self.freeai_model
            dic['freeai_token']                 = self.freeai_token
            dic['freeai_temperature']           = self.freeai_temperature
            dic['freeai_max_step']              = self.freeai_max_step
            dic['freeai_inpLang']               = self.freeai_inpLang
            dic['freeai_outLang']               = self.freeai_outLang

            dic['ollama_nick_name']             = self.ollama_nick_name
            dic['ollama_model']                 = self.ollama_model
            dic['ollama_token']                 = self.ollama_token
            dic['ollama_temperature']           = self.ollama_temperature
            dic['ollama_max_step']              = self.ollama_max_step
            dic['ollama_inpLang']               = self.ollama_inpLang
            dic['ollama_outLang']               = self.ollama_outLang

            dic['restui_start']                 = self.restui_start
            dic['restui_local_ip']              = self.restui_local_ip
            dic['restui_local_port']            = self.restui_local_port
            dic['restui_allow_ip']              = self.restui_allow_ip
            dic['restui_ssl']                   = self.restui_ssl
            dic['restui_ssl_cert']              = self.restui_ssl_cert
            dic['restui_ssl_key']               = self.restui_ssl_key
            dic['restui_auth_key']              = self.restui_auth_key

            dic['webui_start']                  = self.webui_start
            dic['webui_local_ip']               = self.webui_local_ip
            dic['webui_local_port']             = self.webui_local_port
            dic['webui_allow_ip']               = self.webui_allow_ip
            dic['webui_ssl']                    = self.webui_ssl
            dic['webui_ssl_cert']               = self.webui_ssl_cert
            dic['webui_ssl_key']                = self.webui_ssl_key
            dic['webui_multi_session']          = self.webui_multi_session
            dic['webui_admin_id']               = self.webui_admin_id
            dic['webui_admin_pw']               = self.webui_admin_pw
            dic['webui_guest_id']               = self.webui_guest_id
            dic['webui_guest_pw']               = self.webui_guest_pw

            dic['txt_input_path']               = self.txt_input_path
            dic['txt_output_path']              = self.txt_output_path
            dic['stt_path']                     = self.stt_path
            dic['tts_path']                     = self.tts_path
            dic['tts_header']                   = self.tts_header
            dic['web_engine']                   = self.web_engine
            dic['web_home']                     = self.web_home
            dic['feedback_popup']               = self.feedback_popup
            dic['feedback_mouse']               = self.feedback_mouse
            dic['feedback_key']                 = self.feedback_key
            dic['feedback_sound']               = self.feedback_sound
            dic['feedback_sound_accept_file']   = self.feedback_sound_accept_file
            dic['feedback_sound_ok_file']       = self.feedback_sound_ok_file
            dic['feedback_sound_ng_file']       = self.feedback_sound_ng_file

            dic['default_role_text']            = self.default_role_text
            dic['default_req_text1']            = self.default_req_text1
            dic['default_req_text2']            = self.default_req_text2
            dic['chatbot_role_text']            = self.chatbot_role_text
            dic['chatbot_req_text1']            = self.chatbot_req_text1
            dic['chatbot_req_text2']            = self.chatbot_req_text2
            res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )

        if (res == True):
            self.run_priority                   = dic['run_priority']
            self.cgpt_screen                    = dic['cgpt_screen']
            self.cgpt_panel                     = dic['cgpt_panel']
            self.cgpt_alpha                     = dic['cgpt_alpha']

            self.cgpt_guiTheme                  = dic['cgpt_guiTheme']
            self.cgpt_keep_on_top               = dic['cgpt_keep_on_top']
            self.cgpt_secure_level              = dic['cgpt_secure_level']
            self.cgpt_addins_path               = dic['cgpt_addins_path']
            self.cgpt_functions_path            = dic['cgpt_functions_path']

            self.cgpt_engine_greeting           = dic['cgpt_engine_greeting']
            self.cgpt_engine_chat               = dic['cgpt_engine_chat']
            self.cgpt_engine_vision             = dic['cgpt_engine_vision']
            self.cgpt_engine_fileSearch         = dic['cgpt_engine_fileSearch']
            self.cgpt_engine_webSearch          = dic['cgpt_engine_webSearch']
            self.cgpt_engine_assistant          = dic['cgpt_engine_assistant']

            self.openai_api_type                = dic['openai_api_type']
            self.openai_default_gpt             = dic['openai_default_gpt']
            self.openai_organization            = dic['openai_organization']
            self.openai_key_id                  = dic['openai_key_id']
            self.azure_endpoint                 = dic['azure_endpoint']
            self.azure_version                  = dic['azure_version']
            self.azure_key_id                   = dic['azure_key_id']
            self.freeai_key_id                  = dic['freeai_key_id']
            self.ollama_server                  = dic['ollama_server']
            self.ollama_port                    = dic['ollama_port']

            self.openai_nick_name               = dic['openai_nick_name']
            self.openai_model                   = dic['openai_model']
            self.openai_token                   = dic['openai_token']
            self.openai_temperature             = dic['openai_temperature']
            self.openai_max_step                = dic['openai_max_step']
            self.openai_inpLang                 = dic['openai_inpLang']
            self.openai_outLang                 = dic['openai_outLang']

            self.freeai_nick_name               = dic['freeai_nick_name']
            self.freeai_model                   = dic['freeai_model']
            self.freeai_token                   = dic['freeai_token']
            self.freeai_temperature             = dic['freeai_temperature']
            self.freeai_max_step                = dic['freeai_max_step']
            self.freeai_inpLang                 = dic['freeai_inpLang']
            self.freeai_outLang                 = dic['freeai_outLang']

            self.ollama_nick_name               = dic['ollama_nick_name']
            self.ollama_model                   = dic['ollama_model']
            self.ollama_token                   = dic['ollama_token']
            self.ollama_temperature             = dic['ollama_temperature']
            self.ollama_max_step                = dic['ollama_max_step']
            self.ollama_inpLang                 = dic['ollama_inpLang']
            self.ollama_outLang                 = dic['ollama_outLang']

            self.restui_start                   = dic['restui_start']
            self.restui_local_ip                = dic['restui_local_ip']
            self.restui_local_port              = dic['restui_local_port']
            self.restui_allow_ip                = dic['restui_allow_ip']
            self.restui_ssl                     = dic['restui_ssl']
            self.restui_ssl_cert                = dic['restui_ssl_cert']
            self.restui_ssl_key                 = dic['restui_ssl_key']
            self.restui_auth_key                = dic['restui_auth_key']

            self.webui_start                    = dic['webui_start']
            self.webui_local_ip                 = dic['webui_local_ip']
            self.webui_local_port               = dic['webui_local_port']
            self.webui_allow_ip                 = dic['webui_allow_ip']
            self.webui_ssl                      = dic['webui_ssl']
            self.webui_ssl_cert                 = dic['webui_ssl_cert']
            self.webui_ssl_key                  = dic['webui_ssl_key']
            self.webui_multi_session            = dic['webui_multi_session']
            self.webui_admin_id                 = dic['webui_admin_id']
            self.webui_admin_pw                 = dic['webui_admin_pw']
            self.webui_guest_id                 = dic['webui_guest_id']
            self.webui_guest_pw                 = dic['webui_guest_pw']

            self.txt_input_path                 = dic['txt_input_path']
            self.txt_output_path                = dic['txt_output_path']
            self.stt_path                       = dic['stt_path']
            self.tts_path                       = dic['tts_path']
            self.tts_header                     = dic['tts_header']
            self.web_engine                     = dic['web_engine']
            self.web_home                       = dic['web_home']
            self.feedback_popup                 = dic['feedback_popup']
            self.feedback_mouse                 = dic['feedback_mouse']
            self.feedback_key                   = dic['feedback_key']
            self.feedback_sound                 = dic['feedback_sound']
            self.feedback_sound_accept_file     = dic['feedback_sound_accept_file']
            self.feedback_sound_ok_file         = dic['feedback_sound_ok_file']
            self.feedback_sound_ng_file         = dic['feedback_sound_ng_file']

            self.default_role_text              = dic['default_role_text']
            self.default_req_text1              = dic['default_req_text1']
            self.default_req_text2              = dic['default_req_text2']
            self.chatbot_role_text              = dic['chatbot_role_text']
            self.chatbot_req_text1              = dic['chatbot_req_text1']
            self.chatbot_req_text2              = dic['chatbot_req_text2']

        self.runMode                            = runMode
        if (cgpt_screen != ''):
            self.cgpt_screen                    = cgpt_screen
        if (cgpt_panel != ''):
            self.cgpt_panel                     = cgpt_panel
        if (cgpt_alpha != ''):
            self.cgpt_alpha                     = cgpt_alpha

        return True



if __name__ == '__main__':

    conf = _conf()

    # conf 初期化
    runMode   = 'debug'
    conf.init(qLog_fn='', runMode=runMode, )

    # テスト
    print(conf.runMode)


