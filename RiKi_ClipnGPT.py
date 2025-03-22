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

import json

import queue
import threading

#import PySimpleGUI_key
#PySimpleGUI_License=PySimpleGUI_key.PySimpleGUI_License
import PySimpleGUI as sg
from PIL import ImageGrab, Image
from io import BytesIO

import numpy as np
import cv2

import pyperclip
import pandas as pd

import requests
# SSLエラーを無視するための処理
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# ------------
# Dummy import
# ------------
#import pip
import keyboard
import screeninfo
from playsound3 import playsound
import pandas
import openpyxl
import pyodbc
import sqlalchemy
import matplotlib
import seaborn
import gtts
try:
    import googletrans
except:
    pass
import pyaudio
import speech_recognition as sr

import urllib
import ssl
# SSLエラーを無視するための処理
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

from bs4 import BeautifulSoup

# google
from google import genai
from google.genai import types

# win32/OCR
import pytesseract
if (os.name == 'nt'):
    from io import StringIO
    import win32clipboard
    import comtypes.client
    import comtypes.stream
    import winocr

# seleniumモジュールのインポート
from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver import Safari
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import webdriver_manager.chrome
import webdriver_manager.firefox
if (os.name == 'nt'):
    import webdriver_manager.microsoft

# PDF解析用モジュールのインポート
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage



# パス設定
qPath_base = os.path.dirname(sys.argv[0]) + '/'
if (qPath_base == '/'):
    qPath_base = os.getcwd() + '/'
else:
    os.chdir(qPath_base)

# インターフェース
qCtrl_control_gpt   = 'temp/control_gpt.txt'
qCtrl_control_self  = qCtrl_control_gpt

qPath_temp    = 'temp/'
qPath_log     = 'temp/_log/'
qPath_work    = 'temp/_work/'
qPath_input   = 'temp/input/'
qPath_output  = 'temp/output/'
qPath_sandbox = 'temp/sandbox/'
qPath_icons   = '_icons/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

# 処理ルーチン
import      RiKi_ClipnGPT_conf
conf      = RiKi_ClipnGPT_conf._conf()
import      RiKi_ClipnGPT_addin
addin     = RiKi_ClipnGPT_addin._addin()
import      RiKi_ClipnGPT_gui
gui       = RiKi_ClipnGPT_gui._gui()
import      RiKi_ClipnGPT_bot
bot       = RiKi_ClipnGPT_bot._bot()
import      RiKi_ClipnGPT_proc
proc      = RiKi_ClipnGPT_proc._proc()
import      RiKi_ClipnGPT_restui
restui    = RiKi_ClipnGPT_restui._restui()
import      RiKi_ClipnGPT_webui
webui     = RiKi_ClipnGPT_webui._webui()

# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



#runMode  = 'debug'
runMode  = 'assistant'
p_screen = 'auto'
p_panel  = 'auto'
p_alpha  = '0.2'



if __name__ == '__main__':
    main_name = 'ClipnGPT'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 制限設定
    limit_date = '{:1d}{:1d}'.format(int(float(3.0)), int(float(1.0)))
    limit_date = '{:1d}{:1d}'.format(int(float(1.0)), int(float(2.0))) + '/' + limit_date
    limit_date = '/' + limit_date
    limit_date = '{:3d}{:1d}'.format(int(float(202.0)), int(float(6.0))) + limit_date
    main_start = time.time()

    # ディレクトリ作成(基本用)
    qFunc.makeDirs(qPath_temp,    remove=False, )
    qFunc.makeDirs(qPath_log,     remove=False, )
    qFunc.makeDirs(qPath_work,    remove=False, )
    qFunc.makeDirs(qPath_input,   remove=False, )
    qFunc.makeDirs(qPath_output,  remove=False, )
    qFunc.makeDirs(qPath_sandbox, remove=False, )

    # ログ
    nowTime  = datetime.datetime.now()
    basename = os.path.basename(__file__)
    basename = basename.replace('.py', '')
    qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + basename + '.log'
    qLog.init(mode='logger', filename=qLog_fn, )
    qLog.log('info', main_id, 'init')
    qLog.log('info', main_id, basename + ' runMode, ... ')

    # パラメータ
    if (True):
        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()
        if (len(sys.argv) >= 3):
            p_screen = str(sys.argv[2])
        if (len(sys.argv) >= 4):
            p_panel  = str(sys.argv[3])
        if (len(sys.argv) >= 5):
            p_alpha  = str(sys.argv[4])

        qLog.log('info', main_id, 'runMode = ' + str(runMode ))
        qLog.log('info', main_id, 'screen  = ' + str(p_screen))
        qLog.log('info', main_id, 'panel   = ' + str(p_panel ))
        qLog.log('info', main_id, 'alpha   = ' + str(p_alpha ))

    # 初期設定
    if (True):

        # GUI 専用キュー
        log_queue   = queue.Queue()
        gui_queue   = queue.Queue()

        # その他キュー
        clip_queue  = queue.Queue()
        http_queue  = queue.Queue()

        # conf 初期化
        conf.init(qLog_fn=qLog_fn, runMode=runMode, 
                  cgpt_screen=p_screen, cgpt_panel=p_panel, cgpt_alpha=p_alpha, )
        
        # 環境変数設定
        if  (conf.openai_organization[:1] != '<'):
            os.environ['OPENAI_ORGANIZATION'] = conf.openai_organization
        if  (conf.openai_key_id[:1] != '<'):
            os.environ['OPENAI_API_KEY'] = conf.openai_key_id
        if  (conf.freeai_key_id[:1] != '<'):
            os.environ['FREEAI_API_KEY'] = conf.freeai_key_id
            os.environ['GOOGLE_API_KEY'] = conf.freeai_key_id
            os.environ['REACT_APP_GEMINI_API_KEY'] = conf.freeai_key_id

        # 実行優先設定
        nice = conf.run_priority
        if (nice == 'auto'):
            nice = 'below'
        qFunc.setNice(nice, )

        # コントロールリセット
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_') or (txt == '_stop_'):
                qFunc.remove(qCtrl_control_self)

        # テキスト・音声入出力リセット
        if (conf.txt_input_path != ''):
            qFunc.makeDirs(conf.txt_input_path,  remove=True, )
        if (conf.txt_output_path != ''):
            qFunc.makeDirs(conf.txt_output_path, remove=True, )
        if (conf.stt_path != ''):
            if (os.path.isdir(conf.stt_path)):
                qFunc.makeDirs(conf.stt_path, remove=True, )
        if (conf.tts_path != ''):
            if (os.path.isdir(conf.tts_path)):
                qFunc.makeDirs(conf.tts_path, remove=True, )
                if (conf.tts_path == 'temp/s6_5tts_txt/'):
                    if (os.path.isdir('temp/s6_7play/')):
                        qFunc.makeDirs('temp/s6_7play/', remove=True, )

        # ライセンス確認
        limit_mode = True
        if  (conf.openai_key_id != '< your openai key >') \
        and (conf.openai_key_id != ''):
            limit_mode = False
            limit_sec  = 0
        if  (conf.azure_key_id != '< your azure key >') \
        and (conf.azure_key_id != ''):
            limit_mode = False
            limit_sec  = 0
        if  (conf.freeai_key_id != '< your freeai key >') \
        and (conf.freeai_key_id != ''):
            limit_mode = False
            limit_sec  = 0

        # ライセンス制限
        # ・稼働時間の制限1200s
        # ・実行ステップが5回
        # ・実行モデル指定不可
        # ・徐々に遅くなる呪い、30秒
        # ・restui機能は使えない
        # ・Webui機能は使えない
        if (limit_mode == True):
            limit_sec  = int(float(12) * float(100))
            conf.openai_max_step    = int(float(5))
            conf.openai_model       = ''
            conf.openai_token       = ''
            conf.freeai_max_step    = int(float(5))
            conf.freeai_model       = ''
            conf.freeai_token       = ''
            conf.ollama_max_step    = int(float(5))
            conf.ollama_model       = ''
            conf.ollama_token       = ''

        # addin 初期化
        addin.init(qLog_fn=qLog_fn, runMode=runMode,
                   addins_path=conf.cgpt_addins_path, secure_level='medium',
                   organization_auth='', )
        res, msg = addin.addins_load()
        if (res != True) or (msg != ''):
            qLog.log('warning', main_id, msg)
        #res, msg = addin.addins_reset()
        #if (res != True) or (msg != ''):
        #    qLog.log('warning', main_id, msg)

        # bot 初期化
        bot.init(qLog_fn=qLog_fn, runMode=runMode, limit_mode=limit_mode, 
                 conf=conf, addin=addin, log_queue=log_queue, )

        # 拡張ファンクション 読込
        bot.gpt_functions_enable = False
        if (bot.gpt_enable == True):
            if (conf.cgpt_functions_path != ''):
                if (os.path.isdir(conf.cgpt_functions_path)):
                    bot.gpt_functions_enable = True
                    res, msg = bot.gpt_functions_load()
                    if (res != True) or (msg != ''):
                        msg  = '【ご注意】' + '\n\n' + msg + '\n'
                        gui.popup_text(title='Attension', text=msg, auto_close=False, size=(60,12), )

        # タイトル、icon
        titlex = os.path.basename(__file__)
        titlex = titlex.replace('.py','')
        title  = titlex + ' [ ' + runMode + ' ] (License=' + limit_date + ')'
        #icon  = None
        icon   = './_icons/' + titlex + '.ico'

        # GUI 表示位置
        screen = conf.cgpt_screen
        if (screen == 'auto'):
            screen = qGUI.getCornerScreen(rightLeft='left', topBottom='top', checkPrimary=False, )
        panel = conf.cgpt_panel
        if (panel == 'auto'):
            panel  = '5+'

        # GUI 初期化
        gui.init(qLog_fn=qLog_fn, runMode=runMode,
                 screen=conf.cgpt_screen, panel=conf.cgpt_panel,
                 title=title, theme=conf.cgpt_guiTheme,
                 keep_on_top=conf.cgpt_keep_on_top, alpha_channel=conf.cgpt_alpha,
                 icon=icon, )
        gui.bind()

        # ボタン有効化 (リセットは最後に)
        if (bot.openai_enable != True):
            gui.window['_check_openai_'].update(False, visible=False)
        if (bot.freeai_enable != True):
            gui.window['_check_freeai_'].update(False, visible=False)
        if (bot.ollama_enable != True):
            gui.window['_check_ollama_'].update(False, visible=False)

        addin_module = addin.addin_modules.get('addin_pdf', None)
        if (addin_module is None):
            gui.window['_check_pdfParser_'].update(False, visible=False)
        else:
            if (addin_module['onoff'] == 'on'):
                gui.window['_check_pdfParser_'].update(True)
            else:
                gui.window['_check_pdfParser_'].update(False)

        addin_module = addin.addin_modules.get('addin_url', None)
        if (addin_module is None):
            gui.window['_check_htmlParser_'].update(False, visible=False)
        else:
            if (addin_module['onoff'] == 'on'):
                gui.window['_check_htmlParser_'].update(True)
            else:
                gui.window['_check_htmlParser_'].update(False)

        addin_module = addin.addin_modules.get('addin_ocr', None)
        if (addin_module is None):
            gui.window['_check_imageOCR_'].update(False, visible=False)
        else:
            #if (addin_module['onoff'] == 'on'):
            #    gui.window['_check_imageOCR_'].update(True)
            #else:
            gui.window['_check_imageOCR_'].update(False)

        addin_module = addin.addin_modules.get('addin_autoSandbox', None)
        if (addin_module is None):
            gui.window['_check_autoSandbox_'].update(False, visible=False)
        else:
            if (addin_module['onoff'] == 'on'):
                gui.window['_check_autoSandbox_'].update(True)
            else:
                gui.window['_check_autoSandbox_'].update(False)

        gui.window['-exec-parser-'].update(visible=True)
        if (conf.cgpt_functions_path != ''):
            if (os.path.isdir(conf.cgpt_functions_path)):
                gui.window['_check_useFunctions_'].update(visible=True)
        if (conf.stt_path != ''):
            if (os.path.isdir(conf.stt_path)):
                gui.window['_check_fromSpeech_'].update(visible=True)
                addin_module = addin.addin_modules.get('addin_UI_key2STT', None)
                if (addin_module is not None):
                    if (addin_module['onoff'] == 'on'):
                        gui.window['_check_fromSpeech_'].update(True)
        if (conf.tts_path != ''):
            if (os.path.isdir(conf.tts_path)):
                gui.window['_check_toSpeech_'].update(visible=True)
                gui.window['-exec-toSpeech-'].update(visible=True)
                gui.window['-proc-toSpeech-'].update(visible=True)
                #addin_module = addin.addin_modules.get('addin_UI_TTS', None)
                #if (addin_module is not None):
                #    if (addin_module['onoff'] == 'on'):
                #        gui.window['_check_toSpeech_'].update(True)
        gui.window['-clear-'].update(visible=True)
        gui.window['-reset-'].update(visible=True)

        # proc 初期化
        proc.init(qLog_fn=qLog_fn, runMode=runMode, limit_mode=limit_mode,
                  conf=conf, addin=addin, chatgui=gui, chatgui_queue=gui_queue, chatbot=bot, )

        # restui 初期化
        restui.init(qLog_fn=qLog_fn, runMode=runMode, limit_mode=limit_mode,
                   conf=conf, chatbot=bot, chatproc=proc, 
                   flask_base=qPath_base, )

        # restui 起動 (機能制限時は利用不可！)
        if (limit_mode == False):
            if (conf.restui_start == 'yes') or (conf.restui_start == 'auto'):
                restui.flask_start()
                time.sleep(1.00)

        # webui 初期化
        webui.init(qLog_fn=qLog_fn, runMode=runMode, limit_mode=limit_mode,
                   conf=conf, chatbot=bot, chatproc=proc, 
                   flask_base=qPath_base, )

        # webui 起動 (機能制限時は利用不可！)
        if (limit_mode == False):
            if (conf.webui_start == 'yes') or (conf.webui_start == 'auto'):
                webui.flask_start()
                time.sleep(1.00)

        # ライセンス制限
        qLog.log('warning', main_id, '利用ライセンスは、 ' + limit_date + ' まで有効です。')

        seigen = ''
        if (limit_mode == True):
            msg     = 'このシステムは、実行制限された状態で動作開始しました。'
            seigen += msg + '\n'
            qLog.log('warning', main_id, msg)
            msg     = 'これは、利用者様がOpenAIで取得したキー情報を登録するまでは、API利用料金が当事務局の負担となるため、'
            msg    += '以下の制御を行っています。※反響によっては無料利用中止となりますこともご理解いただければ幸いです。'
            seigen += msg + '\n'
            qLog.log('warning', main_id, msg)
            msg    = '・連続したChatGPTのご利用を抑制しています。（徐々に遅くなり最大30秒間隔）'
            seigen += msg + '\n'
            qLog.log('warning', main_id, msg)
            msg    = '・利用モデルも約' + str(bot.openaiAPI.gpt_a_token1) + 'トークンまでに抑制しています。（' + bot.openaiAPI.gpt_a_model1 + '）'
            seigen += msg + '\n'
            qLog.log('warning', main_id, msg)
        if (limit_sec != 0):
            msg    = 'このシステムは、起動から約' + str(int(limit_sec/60)) + '分間ご利用いただけます。'
            seigen += msg + '\n'
            qLog.log('warning', main_id, msg)
        if (seigen != ''):
            seigen  = '【ご注意】' + '\n\n' + seigen + '\n'
            seigen += '※実行制限を解除するには、OpenAIで取得したキー情報を、' + '\n'
            seigen += '　"_config/RiKi_ClipnGPT_key.json"に書き込んで（登録）くださいね。' + '\n'
            seigen += '※多くの利用者にClipnGPTを体験いただきたいので、ご協力お願いします。' + '\n'
            gui.popup_text(title='Attension', text=seigen, auto_close=30, size=(80,14), )

    # 起動
    if (True):
        qLog.log('info', main_id, 'start')

    # GUI 表示ループ
    reset_flag   = True
    refresh_flag = True
    break_flag   = False
    values       = None
    while (break_flag == False):

        # コントロール終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                break_flag = True
                break

        # 実行制限
        if (limit_date != ''):
            nowTime = datetime.datetime.now()
            nowDate = nowTime.strftime('%Y/%m/%d')
            if (nowDate > limit_date):
                qLog.log('critical', main_id, 'Check license [over limit date] ! (' + str(limit_date) + ')')
                break_flag = True
                break
        if (limit_sec != 0):
            if ((time.time() - main_start) > limit_sec):
                qLog.log('critical', main_id, 'Check license [over limit sec] ! (' + str(limit_sec) + ')')
                break_flag = True
                break

        # GUI リセット
        if (reset_flag == True):
            reset_flag   = False
            refresh_flag = True

            # GUI 画面リセット
            role_text = str(conf.default_role_text).strip()
            req_text  = str(conf.default_req_text1 + '\n' + conf.default_req_text2).strip()
            gui.reset(role_text=role_text, req_text=req_text, web_home=conf.web_home, )

            # GUI 自動フェードリセット
            gui.autoFadeControl(reset=True, )

            # GUI 画面リサイズリセット
            gui.resize(reset=True, )

            # フォルダリセット
            #qFunc.makeDirs(qPath_input,   remove=True, )
            #qFunc.makeDirs(qPath_output,  remove=True, )
            #qFunc.makeDirs(qPath_sandbox, remove=True, )

            # クリップボードリセット
            pyperclip.copy('')
            last_clipText  = pyperclip.paste()
            last_userText  = []
            if (last_clipText != ''):
                last_userText.append(last_clipText)
            last_clipImage = ImageGrab.grabclipboard()
            last_userImage = []
            if (last_clipImage is not None):
                last_userImage.append(last_clipImage)

            # 処理Ｑリセット
            while (proc.worker_queue.qsize() >= 1):
                try:
                    p = proc.worker_queue.get()
                    proc.worker_queue.task_done()
                except:
                    break

            # 拡張アドイン リセット
            res, msg = addin.addins_reset()
            if (res != True) or (msg != ''):
                qLog.log('warning', main_id, msg)

            # 拡張アドイン Tree
            addin_tree = gui.get_sg_TreeData()
            for module_dic in addin.addin_modules.values():
                onoff       = module_dic['onoff']
                name        = module_dic['script'] + ' (' + module_dic['func_name'] + ')'
                ver         = module_dic['func_ver']
                description = module_dic['function']['description']
                if (onoff == 'off'):
                    addin_tree.Insert('', name, name, values=[ver, description],
                                    icon=gui.check_box[0])
                else:
                    addin_tree.Insert('', name, name, values=[ver, description],
                                    icon=gui.check_box[1])
            gui.window['_addin_tree_'].update(addin_tree)

            # 拡張ファンクション リセット
            res, msg = bot.gpt_functions_reset()
            if (res != True) or (msg != ''):
                msg  = '【ご注意】' + '\n\n' + msg + '\n'
                gui.popup_text(title='Attension', text=msg, auto_close=10, size=(60,12), )

            # 拡張ファンクション Tree
            func_tree = gui.get_sg_TreeData()
            for module_dic in bot.botFunc.function_modules.values():
                onoff       = module_dic['onoff']
                name        = module_dic['script'] + ' (' + module_dic['func_name'] + ')'
                ver         = module_dic['func_ver']
                description = module_dic['function']['description']
                if (onoff == 'off'):
                    func_tree.Insert('', name, name, values=[ver, description],
                                    icon=gui.check_box[0])
                else:
                    func_tree.Insert('', name, name, values=[ver, description],
                                    icon=gui.check_box[1])
            gui.window['_function_tree_'].update(func_tree)

            # 送信ファイル リセット
            send_tree = gui.get_sg_TreeData()
            proc.sendFile_reset(send_tree=send_tree, icon0=gui.check_box[0], icon1=gui.check_box[1], )
            
            # 送信ファイル Tree
            proc.sendFile_update()

            # GPT リセット
            bot.gpt_history_reset()
            gui.window['_history_list_'].update([])

            # テキスト・音声入出力リセット
            if (conf.txt_input_path != ''):
                qFunc.makeDirs(conf.txt_input_path,  remove=True, )
            if (conf.txt_output_path != ''):
                qFunc.makeDirs(conf.txt_output_path, remove=True, )
            if (conf.stt_path != ''):
                if (os.path.isdir(conf.stt_path)):
                    qFunc.makeDirs(conf.stt_path, remove=True, )
            if (conf.tts_path != ''):
                if (os.path.isdir(conf.tts_path)):
                    qFunc.makeDirs(conf.tts_path, remove=True, )
                    if (conf.tts_path == 'temp/s6_5tts_txt/'):
                        if (os.path.isdir('temp/s6_7play/')):
                            qFunc.makeDirs('temp/s6_7play/', remove=True, )

        # GUI 項目更新
        if (gui_queue.qsize() >= 1):
            while (gui_queue.qsize() >= 1):
                [res_name, res_value] = gui_queue.get()
                gui_queue.task_done()
                if (res_name == '_output_text_') \
                or (res_name == '_proc_text_'):
                    if (res_value[-1] == '\n'):
                        res_value += '\n( ^ ^; )'
                    gui.window[res_name].update(res_value)
                else:
                    gui.window[res_name].update(res_value)

                if (res_name == '_history_list_'):
                    gui.window['_history_list_'].set_vscroll_position(1)

                elif (res_name == '_output_text_'):
                    if (str(conf.feedback_popup).lower() != 'no'):
                        if (res_value[:5]=='[GPT]'):
                            gui.popup_text(title='Chat-GPT', text=res_value, auto_close=conf.feedback_popup, )

                elif (res_name == '_input_path_'):
                    if (res_value.lower()[-4:] == '.zip'):
                        if  (values['_check_autoSandbox_'] == True):
                            # 自動サンドボックス
                            addin_module = addin.addin_modules.get('addin_autoSandbox', None)
                            if (addin_module is not None):
                                res_json = None
                                try:
                                    if (addin_module['onoff'] == 'on'):
                                        dic = {}
                                        dic['file_path'] = res_value
                                        dic['browser'] = "yes"
                                        json_dump = json.dumps(dic, ensure_ascii=False, )
                                        #func_proc = addin_module['func_proc']
                                        #res_json  = func_proc(json_dump)
                                        res_json  = addin.addin_autoSandbox(json_dump)
                                except Exception as e:
                                    print(e)
                                    res_json = None

            # 消去
            while (log_queue.qsize() >= 1):
                [res_name, res_value] = log_queue.get()
                log_queue.task_done()

        # GUI 自動フェード
        gui.autoFadeControl(reset=False, )

        # GUI 画面リサイズ
        gui.resize(reset=False, )

        # GUI 画面更新
        if (refresh_flag == True):
            refresh_flag = False
            gui.refresh()

        # Clip cueue 更新
        while (clip_queue.qsize() >= 1):
            res_data  = clip_queue.get()
            clip_queue.task_done()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name == 'text') or (res_name == 'text-feedback'):
                pyperclip.copy(res_value)
                last_clipText = res_value
                if (last_clipText != ''):
                    last_userText.append(res_value)
                # フィードバックアクション
                if (res_name == 'text-feedback'):
                    if (last_clipText != '') and (last_clipText != '!'):
                        res = proc.feedback_action('ok')
                    else:
                        res = proc.feedback_action('ng')

            elif (res_name == 'image') or (res_name == 'image-feedback') or (res_name == 'image-toClip'):
                    try:
                        img = res_value
                        # イメージセット
                        gui.pil2guiImage(pil_image=img)
                        # クリップボード処理
                        if (res_name == 'image-feedback') or (res_name == 'image-toClip'):
                            if (os.name == 'nt'):
                                proc.image_to_clipboard(img)
                                now_clipImage = ImageGrab.grabclipboard()
                                last_clipImage = now_clipImage
                                if (last_clipImage is not None):
                                    last_userImage.append(now_clipImage)
                        # フィードバックアクション
                        if (res_name == 'image-feedback'):
                            res = proc.feedback_action('ok')
                    except:
                        # フィードバックアクション
                        if (res_name == 'image-feedback'):
                            res = proc.feedback_action('ng')

            elif (res_name == 'path') or (res_name == 'path-feedback') or (res_name == 'path-toClip'):
                img = None
                if (res_value[:4] == 'http'):
                    try:
                        response = requests.get(url=res_value, timeout=10, )
                        img = Image.open(BytesIO(response.content))
                    except:
                        pass
                elif (os.path.isfile(res_value)):
                    try:
                        img = Image.open(res_value)
                    except:
                        pass
                
                if (img is not None):
                    # イメージセット
                    gui.pil2guiImage(pil_image=img)
                    # クリップボード処理
                    if (res_name == 'path-feedback') or (res_name == 'path-toClip'):
                        if (os.name == 'nt'):
                            proc.image_to_clipboard(img)
                            now_clipImage = ImageGrab.grabclipboard()
                            last_clipImage = now_clipImage
                            if (last_clipImage is not None):
                                last_userImage.append(now_clipImage)
                        else:
                            pyperclip.copy(res_value)
                            last_clipText = res_value
                            if (last_clipText != ''):
                                last_userText.append(res_value)
                    # フィードバックアクション
                    if (res_name == 'path-feedback'):
                        res = proc.feedback_action('ok')
                else:
                    if (os.path.isfile(res_value)):
                        # フィードバックアクション
                        if (res_name == 'path-feedback'):
                            res = proc.feedback_action('ok')
                    else:
                        # フィードバックアクション
                        if (res_name == 'path-feedback'):
                            res = proc.feedback_action('ng')

            else:
                print(res_name, res_value)

        # GUI イベント確認                 ↓　timeout値でtime.sleep代用
        event, values = gui.read(timeout=150, timeout_key='-idoling-')

        # GUI 終了イベント処理
        if event == sg.WIN_CLOSED:
            gui.window = None
            break_flag = True
            break
        if event in (None, '-exit-'):
            break_flag = True
            break

        try:
            # ------------------------------
            # アイドリング時の処理
            # ------------------------------
            if (event == '-idoling-'):

                # ------------------------------
                # 処理中表示
                # ------------------------------

                # ステータスバー
                tm     = time.time()
                tm     = tm % 9
                r   = int(abs(np.sin((tm+0)/ 9 * np.pi * 2))*255)
                g   = int(abs(np.sin((tm+3)/ 9 * np.pi * 2))*255)
                b   = int(abs(np.sin((tm+6)/ 9 * np.pi * 2))*255)

                # 処理中
                queue_count = proc.worker_queue.qsize()
                if (queue_count > 0):
                    if (limit_mode == False):

                        if (gui_queue.qsize() == 0):
                            val = values['_proc_text_']
                            if (val[-9:] == '\n( ^ ^; )'):
                                val = val[:-9]

                            hit = 0
                            while (log_queue.qsize() >= 1) and (hit <= 99):
                                [res_name, res_value] = log_queue.get()
                                log_queue.task_done()
                                sts_text = res_value
                                if (sts_text != ''):
                                    val += str(sts_text)
                                    hit += 1
                                    if (sts_text[-1] == '\n'):
                                        break

                            if (hit > 0):
                                txts = val.splitlines()
                                sts_text = txts[-1]
                                if (val[-1] == '\n'):
                                    val += '\n( ^ ^; )'

                                if (len(txts) <= 10):
                                    val2 = val
                                else:
                                    val2 = txts[0] + '\n'
                                    for i in range(9):
                                        if (i != 8):
                                            val2 += txts[len(txts)-9+i] + '\n'
                                        else:
                                            val2 += txts[len(txts)-9+i]
                                            if (val[-1] == '\n'):
                                                val2 += '\n\n( ^ ^; )'

                                gui.window['_proc_text_'].update(val)
                                gui.window['_output_text_'].update(val2)

                        gui.window['_status_bar_'].update(sts_text, background_color=gui.rgb2hex(r,0,0))

                    else:
                        wait_sec = bot.gpt_run_count * 3
                        if (wait_sec > 30):
                            wait_sec = 30
                        count_down = int(wait_sec - (time.time() - bot.gpt_run_last))
                        gui.window['_status_bar_'].update('実行制限('+str(count_down)+'s)', background_color=gui.rgb2hex(r,0,0))

                else:
                    sts_text = ''
    
                    # 通常
                    if (limit_mode == False):
                        gui.window['_status_bar_'].update('', background_color=gui.rgb2hex(0,b,b))

                    else:
                        wait_sec = bot.gpt_run_count * 3
                        if (wait_sec > 30):
                            wait_sec = 30
                        count_down = int(wait_sec - (time.time() - bot.gpt_run_last))

                        # 10秒制限中
                        if (count_down > 0):
                            gui.window['_status_bar_'].update('実行制限('+str(count_down)+'s)', background_color=gui.rgb2hex(r,r,0))
                        # 解除
                        else:
                            gui.window['_status_bar_'].update(sts_text, background_color=gui.rgb2hex(0,b,b))

                # ------------------------------
                # クリップボードからテキスト取得
                # ------------------------------
                excel_data   = False
                now_clipText = pyperclip.paste()
                if (now_clipText != ''):
                    if (now_clipText != last_clipText):
                        last_clipText = now_clipText

                        # テキストデータ処理
                        try:
                            pandas_df = pd.read_clipboard()
                            y,x = pandas_df.shape
                            # 表データならexcel出力
                            if (y>2 and x>2):
                                #print(pandas_df)
                                
                                # 保管
                                nowTime  = datetime.datetime.now()
                                #filename = qPath_input + nowTime.strftime('%Y%m%d.%H%M%S') + '.fromclip.json'
                                #pandas_df.to_json(filename, force_ascii=False)
                                filename = qPath_input + nowTime.strftime('%Y%m%d.%H%M%S') + '.fromclip.xlsx'
                                pandas_df.to_excel(filename, sheet_name='Sheet1', index=False, )
                                if  (values['_check_autoUpload_'] == True):
                                    proc.sendFile_off()
                                    proc.sendFile_add(filename, 'on')
                                else:
                                    proc.sendFile_add(filename, 'off')

                                excel_data = True
                                qLog.log('info', main_id, 'detect clipboard data.')
                        except:
                            pass

                        if  (excel_data == False) \
                        and (now_clipText not in last_userText):
                            qLog.log('info', main_id, 'detect clipboard text.')

                            while (len(last_userText) > 5):
                                del last_userText[0]

                            if (now_clipText != ''):
                                last_userText.append(now_clipText)

                            text = now_clipText
                            text = text.replace('\r', '')

                            hit = True
                            while (hit == True):
                                if (text.find('\n\n')>0):
                                    hit = True
                                    text = text.replace('\n\n', '\n')
                                else:
                                    hit = False

                            text = text.rstrip()

                            # スペシャル判断
                            res_special = False

                            # 拡張アドイン 指示文チェック
                            addin_module = addin.addin_modules.get('addin_directive', None)
                            if (addin_module is not None):
                                res_json = None
                                try:
                                    if (addin_module['onoff'] == 'on'):
                                        dic = {}
                                        dic['original_text']            = text
                                        dic['openai_nick_name']         = conf.openai_nick_name
                                        dic['freeai_nick_name']         = conf.freeai_nick_name
                                        dic['gpt_a_nick_name']          = bot.openaiAPI.gpt_a_nick_name
                                        dic['gpt_b_nick_name']          = bot.openaiAPI.gpt_b_nick_name
                                        dic['gpt_v_nick_name']          = bot.openaiAPI.gpt_v_nick_name
                                        dic['gpt_x_nick_name']          = bot.openaiAPI.gpt_x_nick_name
                                        dic['freeai_a_nick_name']       = bot.freeaiAPI.freeai_a_nick_name
                                        dic['freeai_b_nick_name']       = bot.freeaiAPI.freeai_b_nick_name
                                        dic['freeai_v_nick_name']       = bot.freeaiAPI.freeai_v_nick_name
                                        dic['freeai_x_nick_name']       = bot.freeaiAPI.freeai_x_nick_name
                                        dic['ollama_a_nick_name']       = bot.ollamaAPI.ollama_a_nick_name
                                        dic['ollama_b_nick_name']       = bot.ollamaAPI.ollama_b_nick_name
                                        dic['ollama_v_nick_name']       = bot.ollamaAPI.ollama_v_nick_name
                                        dic['ollama_x_nick_name']       = bot.ollamaAPI.ollama_x_nick_name
                                        json_dump = json.dumps(dic, ensure_ascii=False, )

                                        #func_proc = addin_module['func_proc']
                                        #res_json  = func_proc(json_dump)
                                        res_json  = addin.addin_directive(json_dump)
                                except Exception as e:
                                    print(e)
                                    res_json = None

                                if (res_json is not None):
                                    args_dic = json.loads(res_json)
                                    res_text = args_dic.get('result_text')
                                    if (res_text is not None) and (res_text != ''):
                                        res_special = True
                                    
                            # スペシャル実行
                            if (res_special == True):
                                gui.autoFadeControl(reset=True, )
                                text = str(res_text)

                                text = text.strip()
                                gui.window['_input_text_'].update(text + '\n')

                                # メモ帳転記
                                memo_msg = '[Request] (Clip)' + '\n' + text + '\n\n'
                                qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                                # バッチ投入(スペシャル実行)
                                gpt_sysText = str(values['_role_text_']).strip()
                                gpt_reqText = ''
                                gpt_inpText = text
                                filePath = proc.sendFile_get()
                                
                                gpt_proc = threading.Thread(target=proc.proc_gpt, args=(
                                                            gui_queue, clip_queue, values, 
                                                            gpt_sysText, gpt_reqText, gpt_inpText, 
                                                            filePath, 'clip', 'auto', 'admin',
                                                            None,
                                                            ), daemon=True, )
                                proc.worker_queue.put(gpt_proc)
                                time.sleep(2.00)

                            else:

                                # Clip 処理

                                if (values['_check_fromClip_'] == True):
                                    gui.autoFadeControl(reset=True, )

                                    gui.window['_input_img_'].update(data=gui.gpt_img_null)

                                    # メモ帳転記
                                    if (values['_check_toGPT_'] == True):
                                        memo_msg = '[Request] (Clip)' + '\n' + text + '\n\n'
                                        qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                                    # バッチ投入
                                    clip_proc = threading.Thread(target=proc.proc_clip, args=(
                                                                gui_queue, clip_queue, values, text,
                                                                ), daemon=True, )
                                    proc.worker_queue.put(clip_proc)
                                    time.sleep(2.00)

                # ------------------------------
                # クリップボードから画像取得
                # ------------------------------
                clip_files    = False
                now_clipImage = ImageGrab.grabclipboard()
                if (now_clipImage is not None):
                    if (now_clipImage != last_clipImage):
                        last_clipImage = now_clipImage

                        try:
                            check = last_clipImage[0]
                            if (os.path.isfile(check)):
                                clip_files = True
                                qLog.log('info', main_id, 'detect clipboard files.')

                                proc.sendFile_off()
                                for text in last_clipImage:
                                    basename = os.path.basename(text)
                                    filename = qPath_input + basename
                                    print(filename)
                                    shutil.copyfile(text, filename)
                                    proc.sendFile_add(filename, 'on')
                        except:
                            pass

                        if  (clip_files == False) \
                        and (now_clipImage not in last_userImage):
                            qLog.log('info', main_id, 'detect clipboard image.')

                            while (len(last_userImage) > 5):
                                del last_userImage[0]

                            if (last_clipImage is not None):
                                last_userImage.append(now_clipImage)

                            image = now_clipImage

                            # イメージセット
                            gui.pil2guiImage(pil_image=image)

                            if  (excel_data == False):

                                # 保管
                                nowTime  = datetime.datetime.now()
                                filename = qPath_input + nowTime.strftime('%Y%m%d.%H%M%S') + '.fromclip.jpg'
                                print('error? start')
                                now_clipImage.convert('RGB').save(filename)
                                print('error? end')
                                if  (values['_check_autoUpload_'] == True):
                                    proc.sendFile_off()
                                    proc.sendFile_add(filename, 'on')
                                else:
                                    proc.sendFile_add(filename, 'off')

                                # OCR 処理
                                if (values['_check_imageOCR_'] == True):
                                    gui.autoFadeControl(reset=True, )

                                    if (values['_check_toClip_'] == True):
                                        clip_queue.put(['text', ''])

                                    # バッチ投入
                                    ocr_proc = threading.Thread(target=proc.proc_ocr, args=(
                                                                gui_queue, clip_queue, values, filename,
                                                                ), daemon=True, )
                                    proc.worker_queue.put(ocr_proc)
                                    time.sleep(2.00)

                # ------------------------------
                # ブラウザからURL取得
                # ------------------------------
                while (http_queue.qsize() >= 1):
                    res_data  = http_queue.get()
                    http_queue.task_done()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == 'url'):

                        text = res_value.strip()
                        gui.window['_input_path_'].update(text)

                        gui.autoFadeControl(reset=True, )

                        # メモ帳転記
                        memo_msg = '[Request] (Browser)' + '\n' + text + '\n\n'
                        qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                        # Html 処理
                        if (values['_check_htmlParser_'] == True):
                            gui.autoFadeControl(reset=True, )

                            gui.window['_input_img_'].update(data=gui.gpt_img_null)

                            # バッチ投入
                            clip_proc = threading.Thread(target=proc.proc_clip, args=(
                                                        gui_queue, clip_queue, values, text,
                                                        ), daemon=True, )
                            proc.worker_queue.put(clip_proc)
                            time.sleep(2.00)

                # ------------------------------
                # gpt テキスト フォルダから会話取得
                # ------------------------------
                if (conf.txt_input_path != ''):
                    text, res_file = proc.txt_read(remove=True, path=conf.txt_input_path)
                    if (text != '') and (text != '!'):

                        text = text.strip()
                        gui.window['_input_text_'].update(text + '\n')

                        if (text != '') and (text != '!'):
                            gui.autoFadeControl(reset=True, )

                            # メモ帳転記
                            #memo_msg = '[Request] (STT)' + '\n' + text + '\n\n'
                            #qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                            # バッチ投入
                            gpt_sysText = str(values['_role_text_']).strip()
                            gpt_reqText = ''
                            gpt_inpText = text
                            res_file = res_file.replace(conf.txt_input_path, conf.txt_output_path)
                            filePath = [res_file]

                            gpt_proc = threading.Thread(target=proc.proc_gpt, args=(
                                                        gui_queue, clip_queue, values, 
                                                        gpt_sysText, gpt_reqText, gpt_inpText, 
                                                        filePath, 'text', 'auto', 'text',
                                                        [], 
                                                        ), daemon=True, )
                            proc.worker_queue.put(gpt_proc)
                            time.sleep(2.00)

                # ------------------------------
                # STT フォルダから会話取得
                # ------------------------------
                if (values['_check_fromSpeech_'] == True):
                    text, res_file = proc.txt_read(remove=True, path=conf.stt_path)
                    if (text != '') and (text != '!'):

                        text = text.strip()
                        gui.window['_input_text_'].update(text + '\n')

                        if (text != '') and (text != '!'):
                            gui.autoFadeControl(reset=True, )

                            # メモ帳転記
                            #memo_msg = '[Request] (STT)' + '\n' + text + '\n\n'
                            #qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                            # バッチ投入
                            gpt_sysText = str(values['_role_text_']).strip()
                            gpt_reqText = ''
                            gpt_inpText = text
                            filePath = proc.sendFile_get()

                            gpt_proc = threading.Thread(target=proc.proc_gpt, args=(
                                                        gui_queue, clip_queue, values, 
                                                        gpt_sysText, gpt_reqText, gpt_inpText, 
                                                        filePath, 'gui', 'auto', 'admin',
                                                        None,
                                                        ), daemon=True, )
                            proc.worker_queue.put(gpt_proc)
                            time.sleep(2.00)

            # ------------------------------
            # ボタンイベント処理
            # ------------------------------
            # クリア
            elif (event == '-clear-'):
                print(event, )
                gui.window['_req_text_'].update('')
                gui.window['_input_text_'].update('')
                gui.window['_output_text_'].update('')
                gui.window['_proc_text_'].update('')

            # リセット
            elif (event == '-reset-'):
                print(event, )
                reset_flag = True
                # 手動リセット時の処理
                qFunc.makeDirs(qPath_input,   remove=True, )
                qFunc.makeDirs(qPath_output,  remove=True, )
                qFunc.makeDirs(qPath_sandbox, remove=True, )

            # Path オープン
            elif (event == '-open-path-'):
                print(event, )

                if (values['_input_path_'] != ''):
                    proc_path = str(values['_input_path_']).strip()

                    if (proc_path[:4].lower() == 'http'):

                            # スレッド投入
                            blowser_proc = threading.Thread(target=proc.proc_browser, args=(
                                                        http_queue, conf.web_engine, proc_path,
                                                        ), daemon=True, )
                            blowser_proc.start()
                            #blowser_proc.join()

                    elif (os.path.isfile(proc_path)):

                            # ファイル開く
                            proc.proc_fileexec(file_path=proc_path, )

            # Parser 実行
            elif (event == '-exec-parser-'):
                print(event, )

                if (values['_input_path_'] != ''):
                    proc_path = str(values['_input_path_']).strip()
                    gui.window['_input_text_'].update('')

                    if (proc_path[-4:].lower() == '.txt'):

                            # バッチ投入
                            file_proc = threading.Thread(target=proc.proc_file, args=(
                                                        gui_queue, clip_queue, values, proc_path,
                                                        ), daemon=True, )
                            proc.worker_queue.put(file_proc)
                            time.sleep(2.00)

                    elif (proc_path[-4:].lower() == '.pdf') \
                    and  (values['_check_pdfParser_'] == True):

                            # バッチ投入
                            file_proc = threading.Thread(target=proc.proc_file, args=(
                                                        gui_queue, clip_queue, values, proc_path,
                                                        ), daemon=True, )
                            proc.worker_queue.put(file_proc)
                            time.sleep(2.00)

                    elif (proc_path[:4].lower() == 'http') \
                    and  (values['_check_htmlParser_'] == True):

                            # バッチ投入
                            html_proc = threading.Thread(target=proc.proc_html, args=(
                                                        gui_queue, clip_queue, values, proc_path,
                                                        ), daemon=True, )
                            proc.worker_queue.put(html_proc)
                            time.sleep(2.00)

                    elif (proc_path[-4:].lower() == '.jpg') \
                    or   (proc_path[-4:].lower() == '.png'):

                        image = Image.open(proc_path)
                        gui_img = gui.pil2cv(pil_image=image)
                        h, w = gui_img.shape[:2]
                        if (w > gui.gpt_img_xy):
                            h = int(h * (gui.gpt_img_xy/w))
                            w = gui.gpt_img_xy
                        if (h > gui.gpt_img_xy):
                            w = int(w * (gui.gpt_img_xy/h))
                            h = gui.gpt_img_xy
                        gui_img   = cv2.resize(gui_img, (w,h))
                        png_bytes = cv2.imencode('.png', gui_img)[1].tobytes()
                        gui.window['_input_img_'].update(data=png_bytes)

                        # OCR 処理
                        if (values['_check_imageOCR_'] == True):
                            gui.autoFadeControl(reset=True, )

                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # バッチ投入
                            ocr_proc = threading.Thread(target=proc.proc_ocr, args=(
                                                        gui_queue, clip_queue, values, proc_path,
                                                        ), daemon=True, )
                            proc.worker_queue.put(ocr_proc)
                            time.sleep(2.00)

            # exec GPT 実行
            elif (event == '-exec-toGPT-'):
                print(event, )
 
                if (values['_input_text_'].strip() != ''):
                    sysText = str(values['_role_text_']).strip()
                    reqText = str(values['_req_text_']).strip()
                    inpText = str(values['_input_text_']).strip()
                    gui.window['_output_text_'].update('')
                    gui.window['_proc_text_'].update('')
                    filePath = proc.sendFile_get()

                    # バッチ投入
                    gpt_proc = threading.Thread(target=proc.proc_gpt, args=(
                                                gui_queue, clip_queue, values, 
                                                sysText, reqText, inpText, 
                                                filePath, 'gui', 'auto', 'admin',
                                                None,
                                                ), daemon=True, )
                    proc.worker_queue.put(gpt_proc)
                    time.sleep(2.00)

            # exec クリップボードコピー
            elif (event == '-exec-toClip-'):
                print(event, )
 
                outText = str(values['_output_text_']).strip() + '\n'
                clip_queue.put(['text', outText])

            # exec 音声出力
            elif (event == '-exec-toSpeech-'):
                print(event, )

                text = values['_output_text_'].strip()
                if (text != ''): 
                    res = proc.tts_write(text=text, )
                    if (res == False):
                        qLog.log('critical', main_id, '★TTS書込エラー', )

            # proc GPT 実行
            elif (event == '-proc-toGPT-'):
                print(event, )
 
                if (values['_proc_text_'].strip() != ''):
                    sysText = str(values['_role_text_']).strip()
                    reqText = ''
                    inpText = str(values['_proc_text_']).strip()
                    gui.window['_output_text_'].update('')
                    gui.window['_proc_text_'].update('')

                    # バッチ投入
                    gpt_proc = threading.Thread(target=proc.proc_gpt, args=(
                                                gui_queue, clip_queue, values, 
                                                sysText, reqText, inpText, 
                                                [], 'gui', 'auto', 'admin',
                                                None,
                                                ), daemon=True, )
                    proc.worker_queue.put(gpt_proc)
                    time.sleep(2.00)

            # proc クリップボードコピー
            elif (event == '-proc-toClip-'):
                print(event, )
 
                outText = str(values['_proc_text_']).strip() + '\n'
                clip_queue.put(['text', outText])

            # proc 音声出力
            elif (event == '-proc-toSpeech-'):
                print(event, )

                text = values['_proc_text_'].strip()
                if (text != ''): 
                    res = proc.tts_write(text=text, )
                    if (res == False):
                        qLog.log('critical', main_id, '★TTS書込エラー', )

            # ------------------------------
            # チェックボックス処理
            # ------------------------------
            elif (event == '_check_fromClip_') \
            or   (event == '_check_htmlParser_') \
            or   (event == '_check_fileParser_') \
            or   (event == '_check_toGPT_') \
            or   (event == '_check_toClip_') \
            or   (event == '_check_autoUpload_') \
            or   (event == '_check_autoSandbox_') \
            or   (event == '_check_debugMode_'):
                refresh_flag = True

            elif (event == '_check_openai_'):
                refresh_flag = True
                if (values['_check_openai_'] == True):
                    bot.openai_exec = True
                else:
                    bot.openai_exec = False

            elif (event == '_check_freeai_'):
                refresh_flag = True
                if (values['_check_freeai_'] == True):
                    bot.freeai_exec = True
                else:
                    bot.freeai_exec = False

            elif (event == '_check_ollama_'):
                refresh_flag = True
                if (values['_check_ollama_'] == True):
                    bot.ollama_exec = True
                else:
                    bot.ollama_exec = False

            elif (event == '_check_imageOCR_'):
                refresh_flag = True
                if (values['_check_imageOCR_'] == True):
                    addin_module = addin.addin_modules.get('addin_ocr', None)
                    if (addin_module is not None):
                        if (addin_module['onoff'] != 'on'):
                            gui.window['_check_imageOCR_'].update(False)

            elif (event == '_check_toGPT_'):
                refresh_flag = True

                if (values['_check_toGPT_'] == True):
                    if (bot.gpt_enable != True):
                        qLog.log('critical', main_id, 'GPT api not enabled.', )
                        gui.window['_check_toGPT_'].update(False)

            elif (event == '_check_useFunctions_'):
                refresh_flag = True
                if (values['_check_useFunctions_'] != True):
                    res, msg = bot.gpt_functions_unload()
                else:
                    res, msg = bot.gpt_functions_load()
                    if (res != True) or (msg != ''):
                        msg  = '【ご注意】' + '\n\n' + msg + '\n'
                        gui.popup_text(title='Attension', text=msg, auto_close=False, size=(60,12), )
                # Tree
                func_tree = gui.get_sg_TreeData()
                for module_dic in bot.botFunc.function_modules.values():
                    onoff       = module_dic['onoff']
                    name        = module_dic['script'] + ' (' + module_dic['func_name'] + ')'
                    ver         = module_dic['func_ver']
                    description = module_dic['function']['description']
                    if (onoff == 'off'):
                        func_tree.Insert('', name, name, values=[ver, description],
                                        icon=gui.check_box[0])
                    else:
                        func_tree.Insert('', name, name, values=[ver, description],
                                        icon=gui.check_box[1])
                gui.window['_function_tree_'].update(func_tree)

            elif (event == '_check_fromSpeech_'):
                refresh_flag = True

                change_ok = False
                if (conf.stt_path != ''):
                    if (os.path.isdir(conf.stt_path)):
                        change_ok = True
                if (change_ok == False):
                    if (values['_check_fromSpeech_'] == True):
                        qLog.log('critical', main_id, 'fromSpeech(STT) not enabled.', )
                        gui.window['_check_fromSpeech_'].update(False)

                if (change_ok == True):
                    qFunc.makeDirs(conf.stt_path, remove=True, )

            elif (event == '_check_toSpeech_'):
                refresh_flag = True

                change_ok = False
                if (conf.tts_path != ''):
                    if (os.path.isdir(conf.tts_path)):
                        change_ok = True
                if (change_ok == False):
                    if (values['_check_toSpeech_'] == True):
                        qLog.log('critical', main_id, 'toSpeech(TTS) not enabled.', )
                        gui.window['_check_toSpeech_'].update(False)

                if (change_ok == True):
                    qFunc.makeDirs(conf.tts_path, remove=True, )
                    if (conf.tts_path == 'temp/s6_5tts_txt/'):
                        if (os.path.isdir('temp/s6_7play/')):
                            qFunc.makeDirs('temp/s6_7play/', remove=True, )

            #elif (event == '_addin_tree_'):
            #    addin_name = values['_addin_tree_'][0]
            #    #print(addin_name)
            #    if addin_name in gui.window['_addin_tree_'].metadata:
            #        gui.window['_addin_tree_'].metadata.remove(addin_name)
            #        gui.window['_addin_tree_'].update(key=addin_name, icon=gui.check_box[0])
            #        script_name = addin_name[:addin_name.find(' ')]
            #        for key, module_dic in addin.addin_modules.items():
            #            if (script_name == module_dic['script']):
            #                module_dic['onoff'] = 'off'
            #                addin.addin_modules[key] = module_dic
            #    else:
            #        gui.window['_addin_tree_'].metadata.append(addin_name)
            #        gui.window['_addin_tree_'].update(key=addin_name, icon=gui.check_box[1])
            #        script_name = addin_name[:addin_name.find(' ')]
            #        for key, module_dic in addin.addin_modules.items():
            #            if (script_name == module_dic['script']):
            #                module_dic['onoff'] = 'on'
            #                addin.addin_modules[key] = module_dic

            elif (event == '_function_tree_'):
                func_name = values['_function_tree_'][0]
                #print(func_name)
                if func_name in gui.window['_function_tree_'].metadata:
                    gui.window['_function_tree_'].metadata.remove(func_name)
                    gui.window['_function_tree_'].update(key=func_name, icon=gui.check_box[0])
                    script_name = func_name[:func_name.find(' ')]
                    for key in bot.botFunc.function_modules.keys():
                        module_dic = bot.botFunc.function_modules[key]
                        if (script_name == module_dic['script']):
                            module_dic['onoff'] = 'off'
                            bot.botFunc.function_modules[key] = module_dic
                else:
                    gui.window['_function_tree_'].metadata.append(func_name)
                    gui.window['_function_tree_'].update(key=func_name, icon=gui.check_box[1])
                    script_name = func_name[:func_name.find(' ')]
                    for key in bot.botFunc.function_modules.keys():
                        module_dic = bot.botFunc.function_modules[key]
                        if (script_name == module_dic['script']):
                            module_dic['onoff'] = 'on'
                            bot.botFunc.function_modules[key] = module_dic

            elif (event == '_sendfile_tree_'):
                send_file = values['_sendfile_tree_'][0]
                #print(send_file)
                if send_file in gui.window['_sendfile_tree_'].metadata:
                    gui.window['_sendfile_tree_'].metadata.remove(send_file)
                    gui.window['_sendfile_tree_'].update(key=send_file, icon=gui.check_box[0])
                    proc.sendFile_onoff(send_file=send_file, onoff='off')
                else:
                    gui.window['_sendfile_tree_'].metadata.append(send_file)
                    gui.window['_sendfile_tree_'].update(key=send_file, icon=gui.check_box[1])
                    proc.sendFile_onoff(send_file=send_file, onoff='on')

            # ------------------------------
            # キーボードイベント処理
            # ------------------------------
            elif (event == '_input_path_') \
            or   (event == '_role_text_') \
            or   (event == '_req_text_') \
            or   (event == '_input_text_') \
            or   (event == '_output_text_') \
            or   (event == '_proc_text_'):
                # GUI 自動フェードリセット
                gui.autoFadeControl(reset=True, )

            # ------------------------------
            # POPUP 処理
            # ------------------------------
            elif (event == '_input_text_ double'):
                gui.popup_text(title='Input Text', text=values['_input_text_'], )
            elif (event == '_output_text_ double'):
                gui.popup_text(title='Output Text', text=values['_output_text_'], )
            elif (event == '_proc_text_ double'):
                gui.popup_text(title='Proc Text', text=values['_proc_text_'], )
            elif (event == '_history_list_ double'):
                try:
                    row = values['_history_list_'][0]
                    text = proc.last_history_table[row][3]
                    try:
                        wk_dic  = json.loads(text)
                        wk_text = json.dumps(wk_dic, indent=2, ensure_ascii=False, )
                        text    = wk_text
                    except:
                        pass
                    gui.popup_text(title='Content', text=text, )
                except:
                    pass

            else:
                print(event, values, )
        except Exception as e:
            print(e)
            time.sleep(5.00)

    # 終了処理
    if (True):
        qLog.log('info', main_id, 'terminate')

        # 拡張アドイン 解放！
        res, msg = addin.addins_unload()

        # 拡張ファンクション 解放！
        res, msg = bot.gpt_functions_unload()

        # GUI 画面消去
        try:
            gui.close()
            gui.terminate()
        except:
            pass

        # 終了
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


