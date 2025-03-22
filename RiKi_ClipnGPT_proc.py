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

import subprocess

from selenium.webdriver import Edge
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_input  = 'temp/input/'
qPath_output = 'temp/output/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

# 処理ルーチン
import RiKi_ClipnGPT_func
func = RiKi_ClipnGPT_func._func()



class _proc:

    def __init__(self, ):

        self.runMode            = 'debug'
        self.limit_mode         = False
        self.chatgui            = None
        self.chatgui_queue      = None
        self.chatbot            = None

        self.send_tree_null     = None
        self.send_tree_icon0    = None
        self.send_tree_icon1    = None
        self.sendFile_reset(None)
        
        self.last_history_table = []

        # Worker デーモン起動
        self.worker_queue = queue.Queue()
        worker_proc = threading.Thread(target=self.proc_worker, args=(), daemon=True, )
        worker_proc.start()

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

    def sendFile_reset(self, send_tree=None, icon0=None, icon1=None):
        if (send_tree is not None):
            self.send_tree_null  = send_tree
            self.send_tree_icon0 = icon0
            self.send_tree_icon1 = icon1
        self.sendFile_list = {}
        self.sendFile_add('_icons/dog.jpg', 'off')
        self.sendFile_add('_icons/kyoto.png', 'off')

    def sendFile_onoff(self, send_file='_', onoff='off', ):
        sendFile_dic = self.sendFile_list[send_file]
        sendFile_dic['onoff']       = onoff
        sendFile_dic['time']        = time.time()
        self.sendFile_list[send_file] = sendFile_dic

    def sendFile_off(self, ):
        for send_f in self.sendFile_list:
            sendFile_dic = self.sendFile_list[send_f]
            sendFile_dic['onoff'] = 'off'
            self.sendFile_list[send_f] = sendFile_dic

    def sendFile_add(self, send_file='_', onoff='off', ):
        if (os.path.isfile(send_file)):
            sendFile_dic = {}
            sendFile_dic['onoff']       = onoff
            sendFile_dic['name']        = send_file
            sendFile_dic['time']        = time.time()
            sendFile_dic['image']       = ''
            self.sendFile_list[send_file] = sendFile_dic

        self.sendFile_update()

    def sendFile_get(self, ):
        filePath = []
        for send_file in self.sendFile_list:
            sendFile_dic = self.sendFile_list[send_file]
            onoff        = sendFile_dic['onoff']
            if (onoff == 'on'):
                filePath.append(send_file)
                sendFile_dic['onoff'] = 'off'
                sendFile_dic['time']  = time.time()
                self.sendFile_list[send_file] = sendFile_dic
        if (filePath != []):
            self.sendFile_update()

        return filePath

    def sendFile_update(self, ):
        if (self.chatgui_queue is not None):
            if (self.send_tree_null is not None):
                send_tree = self.chatgui.get_sg_TreeData()
                for send_file in self.sendFile_list:
                    sendFile_dic = self.sendFile_list[send_file]
                    onoff       = sendFile_dic['onoff']
                    name        = sendFile_dic['name']
                    tm          = sendFile_dic['time']
                    tmx         = time.strftime('%H:%M:%S', time.localtime(tm))
                    image       = sendFile_dic['image']
                    if (onoff == 'off'):
                        send_tree.Insert('', name, name, values=[tmx, image, ],
                                        icon=self.send_tree_icon0)
                    else:
                        send_tree.Insert('', name, name, values=[tmx, image, ],
                                        icon=self.send_tree_icon1)

                self.chatgui_queue.put(['_sendfile_tree_', send_tree])

    def proc_worker(self, ):
        while True:
            if (self.worker_queue.qsize() >= 1):
                p = self.worker_queue.get()
                self.worker_queue.task_done()
                if (p is not None):
                    try:
                        p.start()
                        # ダミー１つ追加
                        self.worker_queue.put(None)
                        p.join()
                    except Exception as e:
                        print(e)
                        time.sleep(1.00)
            time.sleep(0.25)
        return True

    def txt_read(self, remove=False, path='temp/chat_input/', ):
        res_text, res_file = func.txt_read(remove=remove, path=path, )
        return res_text, res_file

    def tts_write(self, text='', ):
        res = func.tts_write(text=text, )
        return res

    def feedback_action(self, mode='ok', ):
        res = func.feedback_action(mode=mode, )
        return res

    def image_to_clipboard(self, image=None, ):
        res = func.image_to_clipboard(image=image, )
        return res

    def init(self, qLog_fn='', runMode='debug', limit_mode=False, 
             conf=None, addin=None, chatgui=None, chatgui_queue=None, chatbot=None, ):

        self.runMode       = runMode
        self.limit_mode    = limit_mode

        # ログ
        self.proc_name = 'proc'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')

        self.conf          = conf
        self.addin         = addin
        self.chatgui       = chatgui
        self.chatgui_queue = chatgui_queue
        self.chatbot       = chatbot
        
        # func 初期化
        func.init(qLog_fn=qLog_fn, runMode=runMode, conf=conf, )

        return True

    # ------------------------------
    # Clip 処理
    # ------------------------------
    def proc_clip(self, gui_queue=None, clip_queue=None, values=[], clip_text='', ):
        if (clip_text != ''):
            gui_queue.put(['_input_text_', '... Now Processing ...\n'])
            gui_queue.put(['_proc_text_',  '... Now Processing ...\n'])

            try:
                # 文書成形
                text = self.text_replace(text=clip_text, )

                if (text.strip() == '') or (text.strip() == '!'):
                    gui_queue.put(['_input_text_', '!'])
                    gui_queue.put(['_proc_text_',  '!'])
                    return False

                else:

                    # 内容判断
                    while (text[:1] == '"') and (text[-1:] == '"'):
                        text = text[1:len(text)-1]
                    if (text[:4].lower() == 'http') \
                    or (text[-4:].lower() == '.pdf') \
                    or (text[-4:].lower() == '.txt') \
                    or (text[-4:].lower() == '.jpg') \
                    or (text[-4:].lower() == '.png') \
                    or (text[-5:].lower() == '.xlsx') \
                    or (text[-5:].lower() == '.docx') \
                    or (text[-4:].lower() == '.mp3') \
                    or (text[-4:].lower() == '.mp4') \
                    or (text[-4:].lower() == '.m4a') \
                    or (text[-4:].lower() == '.m4v') \
                    or (text[-3:].lower() == '.py') \
                    or (text[-4:].lower() == '.zip'):
                        is_path = True
                        gui_queue.put(['_input_path_', text])
                        gui_queue.put(['_input_text_', ''])
                    else:
                        is_path = False
                        gui_queue.put(['_input_path_', ''])
                        gui_queue.put(['_input_text_', text + '\n'])
                    gui_queue.put(['_proc_text_', text + '\n'])

                    # path 処理(ファイルコピー)
                    if (is_path == True):
                        if (os.path.isfile(text)):
                            try:
                                basename   = os.path.basename(text)
                                input_file = qPath_input + basename
                                shutil.copyfile(text, input_file)

                                # Whisper用コピー
                                if (text[-4:].lower() == '.mp3') \
                                or (text[-4:].lower() == '.mp4') \
                                or (text[-4:].lower() == '.m4a') \
                                or (text[-4:].lower() == '.m4v'):
                                    input_file2 = qPath_input + '_whisper_input' + input_file[-4:].lower()
                                    file_list = glob.glob(input_file2[:-4] + '.*')
                                    for file in file_list:
                                        try:
                                            os.remove(file)
                                        except:
                                            pass
                                    shutil.copyfile(input_file, input_file2)

                                if  (values['_check_autoUpload_'] == True):
                                    self.sendFile_off()
                                    self.sendFile_add(input_file, 'on')
                                else:
                                    self.sendFile_add(input_file, 'off')
                            except:
                                pass

                    # path 処理
                    if (is_path == True):
                        if  (text[-4:].lower() == '.txt') \
                        and (values['_check_fileParser_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # File Parser 処理
                            proc_path = text
                            res = self.proc_file(gui_queue, clip_queue, values, proc_path, )

                        elif (text[-4:].lower() == '.pdf') \
                        and  (values['_check_pdfParser_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # File Parser 処理
                            proc_path = text
                            res = self.proc_file(gui_queue, clip_queue, values, proc_path, )

                        elif (text[:4] == 'http') \
                        and  (values['_check_htmlParser_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # Html Parser 処理
                            proc_path = text
                            res = self.proc_html(gui_queue, clip_queue, values, proc_path, )

                        elif (   (text[-4:].lower() == '.jpg')  \
                              or (text[-4:].lower() == '.png')) \
                        and  (values['_check_imageOCR_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # OCR 処理
                            proc_path = text
                            res = self.proc_ocr(gui_queue, clip_queue, values, proc_path, )
                            return res

                    # text 処理
                    if (is_path == False):

                        # GPT 実行
                        if (values['_check_toGPT_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # GPT 処理
                            gpt_sysText = str(values['_role_text_'])
                            gpt_reqText = str(values['_req_text_'])
                            gpt_inpText = text + '\n'
                            filePath    = proc.sendFile_get()
                            res = self.proc_gpt(gui_queue, clip_queue, values, 
                                                gpt_sysText, gpt_reqText, gpt_inpText, 
                                                filePath, 'gui', 'auto', 'admin', 
                                                None, )

                    return True

            except Exception as e:
                print(e)
                gui_queue.put(['_input_text_', '!'])
                gui_queue.put(['_proc_text_',  '!'])

        return False

    # ------------------------------
    # OCR 処理
    # ------------------------------
    def proc_ocr(self, gui_queue=None, clip_queue=None, values=[], proc_path=None, ):
        if (proc_path is not None):
            gui_queue.put(['_input_text_', '... Now Processing ...\n'])
            gui_queue.put(['_proc_text_',  '... Now Processing ...\n'])

            text = ''
            try:

                # 拡張アドイン image_to_text
                dic = {}
                dic['file_path'] = proc_path
                json_dump = json.dumps(dic, ensure_ascii=False, )

                res_json = None
                addin_module = self.addin.addin_modules.get('addin_ocr', None)
                if (addin_module is not None):
                    try:
                        if (addin_module['onoff'] == 'on'):
                            #func_proc = addin_module['func_proc']
                            #res_json  = func_proc(json_dump)
                            res_json  = self.addin.addin_ocr(json_dump)
                    except:
                        res_json = None

                if (res_json is not None):
                    args_dic = json.loads(res_json)
                    text = args_dic.get('result_text')

                if (text == '') or (text == '!'):
                    gui_queue.put(['_input_text_', '!'])
                    gui_queue.put(['_proc_text_',  '!'])
                    return False

                else:

                    # メモ帳転記
                    memo_msg = '[OCR] (tesseract)' + '\n' + text + '\n\n'
                    gui_queue.put(['_proc_text_', memo_msg])
                    if (values['_check_toGPT_'] != True):
                        qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                    # 内容判断
                    while (text[:1] == '"') and (text[-1:] == '"'):
                        text = text[1:len(text)-1]
                    if (text[:4].lower() == 'http') \
                    or (text[-4:].lower() == '.pdf') \
                    or (text[-4:].lower() == '.txt') \
                    or (text[-4:].lower() == '.jpg') \
                    or (text[-4:].lower() == '.png'):
                        is_path = True
                        gui_queue.put(['_input_path_', text])
                        gui_queue.put(['_input_text_', ''])
                    else:
                        is_path = False
                        #gui_queue.put(['_input_path_', ''])
                        gui_queue.put(['_input_text_', text + '\n'])

                    # path 処理
                    if (is_path == True):
                        if  (text[-4:].lower() == '.txt') \
                        and (values['_check_fileParser_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # File Parser 処理
                            proc_path = text
                            res = self.proc_file(gui_queue, clip_queue, values, proc_path, )

                        elif (text[-4:].lower() == '.pdf') \
                        and  (values['_check_pdfParser_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # File Parser 処理
                            proc_path = text
                            res = self.proc_file(gui_queue, clip_queue, values, proc_path, )

                        elif (text[:4] == 'http') \
                        and  (values['_check_htmlParser_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # Html Parser 処理
                            proc_path = text
                            res = self.proc_html(gui_queue, clip_queue, values, proc_path, )

                        elif (   (text[-4:].lower() == '.jpg')  \
                              or (text[-4:].lower() == '.png')) \
                        and  (values['_check_imageOCR_'] == True):
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', ''])

                            # OCR 処理
                            proc_path = text
                            res = self.proc_ocr(gui_queue, clip_queue, values, proc_path, )
                            return res

                        else:
                            # クリップボード書込
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', text + '\n'])

                    # text 処理
                    if (is_path == False):

                        # GPT 実行
                        if (values['_check_toGPT_'] == True):
                            gpt_sysText = str(values['_role_text_'])
                            gpt_reqText = str(values['_req_text_'])
                            gpt_inpText = text + '\n'
                            res = self.proc_gpt(gui_queue, clip_queue, values, 
                                                gpt_sysText, gpt_reqText, gpt_inpText, 
                                                [], 'gui', 'auto', 'admin', 
                                                None, )

                        else:
                            # クリップボード書込
                            if (values['_check_toClip_'] == True):
                                clip_queue.put(['text', text + '\n'])

                    return True

            except Exception as e:
                print(e)
                gui_queue.put(['_input_text_', '!'])
                gui_queue.put(['_proc_text_',  '!'])

        return False

    # ------------------------------
    # Html Parser 処理
    # ------------------------------
    def proc_html(self, gui_queue=None, clip_queue=None, values=[], proc_path='', ):
        if (proc_path[:4].lower() == 'http'):
            gui_queue.put(['_input_text_', '... Now Processing ...\n'])
            gui_queue.put(['_proc_text_',  '... Now Processing ...\n'])

            text = ''
            try:
                # なろうページ？
                narou_pages = ''
                if (proc_path[:26] == 'https://ncode.syosetu.com/'):
                    page_path = proc_path[26:]
                    page_hit  = page_path.find('/')
                    # 最初の"/"
                    if (page_hit >= 0):
                        page_str = page_path[page_hit:]
                        try:
                            # ページ番号
                            page_n = int(page_str.replace('/',''))
                            narou_pages = '[なろう] ' + page_path[:page_hit] + ' ' + str(page_n)
                        except:
                            pass

                # 拡張アドイン url_to_text
                dic = {}
                dic['url_path'] = proc_path
                json_dump = json.dumps(dic, ensure_ascii=False, )

                res_json = None
                addin_module = self.addin.addin_modules.get('addin_url', None)
                if (addin_module is not None):
                    try:
                        if (addin_module['onoff'] == 'on'):
                            #func_proc = addin_module['func_proc']
                            #res_json  = func_proc(json_dump)
                            res_json  = self.addin.addin_url(json_dump)
                    except:
                        res_json = None

                if (res_json is not None):
                    args_dic = json.loads(res_json)
                    text = args_dic.get('result_text')

                if (text == '') or (text == '!'):
                    gui_queue.put(['_input_text_', '!'])
                    gui_queue.put(['_proc_text_',  '!'])
                    return False

                else:
                    gui_queue.put(['_input_text_', text + '\n'])
                    gui_queue.put(['_proc_text_',  text + '\n'])

                    # なろう読上特別ロジック
                    if (narou_pages != ''):

                        # メモ帳転記
                        memo_msg = narou_pages + '\n\n' + text  + '\n\n'
                        gui_queue.put(['_proc_text_', memo_msg])
                        qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                        # GPT 実行無効
                        if (values['_check_toGPT_'] == False):
                            gui_queue.put(['_output_text_', narou_pages + '\n' + text + '\n'])

                            # 音声出力有効
                            if (values['_check_toSpeech_'] == True):
                                res = func.tts_write(text=text, )

                    else:

                        # メモ帳転記
                        memo_msg = '[HTML Parser] (BeautifulSoup)' + '\n' + proc_path + '\n\n'
                        if (values['_check_toGPT_'] != True):
                            memo_msg += text + '\n\n'
                        gui_queue.put(['_proc_text_', memo_msg])
                        qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                    # GPT 実行
                    if (values['_check_toGPT_'] == True):
                        gpt_sysText = str(values['_role_text_'])
                        gpt_reqText = str(values['_req_text_'])
                        gpt_inpText = text + '\n'
                        res = self.proc_gpt(gui_queue, clip_queue, values, 
                                            gpt_sysText, gpt_reqText, gpt_inpText, 
                                            [], 'gui', 'auto', 'admin', 
                                            None, )

                    else:
                        # クリップボード書込
                        if (values['_check_toClip_'] == True):
                            clip_queue.put(['text', text + '\n'])

                    return True

            except Exception as e:
                print(e)
                gui_queue.put(['_input_text_', '!'])
                gui_queue.put(['_proc_text_',  '!'])

        return False

    # ------------------------------
    # File Parser 処理
    # ------------------------------
    def proc_file(self, gui_queue=None, clip_queue=None, values=[], proc_path='', ):
        if (proc_path[-4:].lower() == '.pdf') \
        or (proc_path[-4:].lower() == '.txt'):
            gui_queue.put(['_input_text_', '... Now Processing ...\n'])
            gui_queue.put(['_proc_text_',  '... Now Processing ...\n'])

            text = ''
            try:

                # PDF
                if (proc_path[-4:].lower() == '.pdf'):

                    # 拡張アドイン pdf_to_text
                    dic = {}
                    dic['file_path'] = proc_path
                    json_dump = json.dumps(dic, ensure_ascii=False, )

                    res_json = None
                    addin_module = self.addin.addin_modules.get('addin_pdf', None)
                    if (addin_module is not None):
                        try:
                            if (addin_module['onoff'] == 'on'):
                                #func_proc = addin_module['func_proc']
                                #res_json  = func_proc(json_dump)
                                res_json  = self.addin.addin_pdf(json_dump)
                        except:
                            res_json = None

                    if (res_json is not None):
                        args_dic = json.loads(res_json)
                        text = args_dic.get('result_text')

                # TXT
                if (proc_path[-4:].lower() == '.txt'):
                    if (proc_path[-9:].lower() == '_sjis.txt'):
                        txts, text = qFunc.txtsRead(proc_path, encoding='shift_jis', exclusive=False, )
                    else:
                        txts, text = qFunc.txtsRead(proc_path, encoding='utf-8', exclusive=False, )

                if (text == '') or (text == '!'):
                    gui_queue.put(['_input_text_', '!'])
                    gui_queue.put(['_proc_text_',  '!'])
                    return False

                else:
                    gui_queue.put(['_input_text_', text + '\n'])
                    gui_queue.put(['_proc_text_',  text + '\n'])

                    # メモ帳転記
                    memo_msg = '[PDF Parser] (pdfminer)' + '\n' + proc_path + '\n\n'
                    if (values['_check_toGPT_'] != True):
                        memo_msg += text + '\n\n'
                    gui_queue.put(['_proc_text_', memo_msg])
                    qGUI.notePad(txt=memo_msg, cr=False, lf=False, )

                    # GPT 実行
                    if (values['_check_toGPT_'] == True):
                        gpt_sysText = str(values['_role_text_'])
                        gpt_reqText = str(values['_req_text_'])
                        gpt_inpText = text + '\n'
                        res = self.proc_gpt(gui_queue, clip_queue, values, 
                                            gpt_sysText, gpt_reqText, gpt_inpText, 
                                            [], 'gui', 'auto', 'admin', 
                                            None, )

                    else:
                        # クリップボード書込
                        if (values['_check_toClip_'] == True):
                            clip_queue.put(['text', text + '\n'])

                    return True

            except Exception as e:
                print(e)
                gui_queue.put(['_input_text_', '!'])
                gui_queue.put(['_proc_text_',  '!'])

        return False

    # ------------------------------
    # GPT 処理
    # ------------------------------
    def proc_gpt(self, gui_queue=None, clip_queue=None, values=[], gpt_sysText='', gpt_reqText='', gpt_inpText='', file_path=[], interface='gui', chat_class='auto', session_id='admin', gpt_history=None, ):
        # interface = ['gui', 'clip', 'text', 'web-admin', 'web-guest', ]

        if (gpt_inpText != ''):
            if (interface == 'gui') or (interface == 'clip') or (interface == 'text'):
                gui_queue.put(['_output_text_', '... Now Processing ...\n'])
                gui_queue.put(['_proc_text_',   '... Now Processing ...\n'])

            if (interface == 'text'):
                out_file  = file_path[0]
                file_path = []

            text = ''
            try:

                if (self.chatbot is not None):

                    # フィードバックアクション
                    if (interface == 'clip'):
                        res = func.feedback_action('accept')

                    # 実行制限
                    if (self.limit_mode == True):
                        wait_sec = self.chatbot.gpt_run_count * 3
                        if (wait_sec > 30):
                            wait_sec = 30
                        count_down = int(wait_sec - (time.time() - self.chatbot.gpt_run_last))

                        while (count_down > 0):
                            print('limited run mode (waitting ' + str(count_down) + 's )')
                            time.sleep(1.00)
                            count_down = int(wait_sec - (time.time() - self.chatbot.gpt_run_last))

                    self.chatbot.gpt_run_count += 1
                    self.chatbot.gpt_run_last  = time.time()

                    if (chat_class == 'auto'):
                        if (values.get('_check_debugMode_') == True):
                            chat_class = 'assistant'
                    if (self.limit_mode == True):
                        chat_class = 'chat'

                    # ChatGPT
                    if (interface != 'text'):
                        if (gpt_history is None):
                            history = self.chatbot.history
                        else:
                            history = gpt_history
                    else:
                        history = []

                    print()
                    print('### START ###', session_id)

                    if (len(file_path) > 0):
                        print(' Attach files ...', file_path)

                    function_modules = {}
                    for key, module_dic in self.chatbot.botFunc.function_modules.items():
                        if (module_dic['onoff'] == 'on'):
                            function_modules[key] = module_dic

                    # chatbot
                    text, res_path, res_files, res_name, res_api, res_history = \
                    self.chatbot.chatBot( chat_class=chat_class, model_select='auto', 
                                          session_id=session_id, history=history, function_modules=function_modules,
                                          sysText=gpt_sysText, reqText=gpt_reqText, inpText=gpt_inpText, filePath=file_path, )

                    if (interface != 'text'):
                        if (gpt_history is None):
                            self.chatbot.history = res_history

                    print('###  END  ###', session_id)

                    self.chatbot.gpt_run_last  = time.time()

                    # History
                    if (interface != 'text') and (interface[:3] != 'web'):
                        self.last_history_table = []
                        for h in range(len(res_history)):
                            seq  = res_history[h]['seq']
                            tm   = res_history[h]['time']
                            tmx  = time.strftime('%H:%M:%S', time.localtime(tm))
                            role = res_history[h]['role']
                            if (res_history[h]['name'] != ''):
                                if (role == 'function_call'):
                                    role = res_history[h]['name'] + ' (Req)'
                                else:
                                    role = res_history[h]['name'] + ' (Ans)'
                            content = res_history[h]['content']
                            content = content.replace('\n', ' / ')
                            self.last_history_table.append([ seq, tmx, role, content, ])
                        gui_queue.put(['_history_list_', self.last_history_table])

                # 注意！webとのやり取り 別のgui_queueを利用
                if (interface[:3] == 'web'):
                    gui_queue.put(['[history]', res_history])

                # エラー応答
                if (text == '') or (text == '!'):
                    if (interface == 'gui') or (interface == 'clip') or (interface == 'text'):
                        gui_queue.put(['_output_text_', '!'])
                        gui_queue.put(['_proc_text_',   '!'])
                    if (interface[:3] == 'web'):
                        gui_queue.put(['_output_text_', '!'])
                    if (clip_queue is not None):
                        clip_key='text'
                        if (interface == 'clip'):
                            clip_key='text-feedback'
                            clip_queue.put([clip_key, '!'])
                        else:
                            if (values.get('_check_toClip_') == True):
                                clip_queue.put([clip_key, '!'])
                    return False

                # 正常応答
                else:
                    text = text.rstrip()
                    if (self.chatbot is not None):
                        if (self.chatbot.openai_nick_name == ''):
                            gpt_text = '[' + res_name + '] (' + res_api + ')' + '\n' + text
                        else:
                            gpt_text = '[' + self.chatbot.openai_nick_name + ']' + '\n' + text
                    if (interface == 'gui') or (interface == 'clip') or (interface == 'text'):
                        if (res_path is not None ) and (res_path != ''):
                            gui_queue.put(['_input_path_', res_path])
                        gui_queue.put(['_output_text_', gpt_text + '\n'])
                        gui_queue.put(['_proc_text_',   gpt_text + '\n'])
                    if (interface[:3] == 'web'):
                        if (res_path is not None) and (res_path != ''):
                            gui_queue.put(['_input_path_', res_path])
                        gui_queue.put(['_output_text_', gpt_text + '\n'])

                    # メモ帳転記
                    if (interface[:3] != 'web'):
                        qGUI.notePad(txt=gpt_text + '\n\n', cr=False, lf=False, )

                        # クリップボード書込
                        if (clip_queue is not None):

                            # イメージパス
                            if (res_path is not None ) and (res_path != ''):
                                clip_key='path'
                                if (interface == 'clip'):
                                    clip_key='path-feedback'
                                elif (values.get('_check_toClip_') == True):
                                    clip_key='path-toClip'
                                clip_queue.put([clip_key, res_path])

                            # テキスト
                            else:
                                clip_key='text'
                                if (interface == 'clip'):
                                    clip_key='text-feedback'
                                    if (text.find('\n') < 0):
                                        clip_queue.put([clip_key, text])
                                    else:
                                        clip_queue.put([clip_key, gpt_text + '\n'])
                                else:
                                    if (values.get('_check_toClip_') == True):
                                        clip_queue.put([clip_key, gpt_text + '\n'])

                        # 音声出力
                        if (interface != 'text'):
                            if (values.get('_check_toSpeech_') == True):
                                res = func.tts_write(text=gpt_text, )

                        # メモ帳転記
                        if (interface == 'text'):
                            qFunc.txtsWrite(filename=out_file, txts=[text], )

                    return True

            except Exception as e:
                print(e)
                if (interface == 'gui') or (interface == 'clip') or (interface == 'text'):
                    gui_queue.put(['_output_text_', '!'])
                    gui_queue.put(['_proc_text_',   '!'])

        return False

    def proc_browser(self, http_queue=None, web_engine='firefox', web_home='https://google.com', ):

        try:
            # 起動
            if   (web_engine == 'chrome'):
                engine = Chrome()
            elif (web_engine == 'firefox'):
                engine = Firefox()
            else:
                engine = Edge()

            # 最大化
            try:
                engine.maximize_window()
            except Exception as e:
                print(e)

            # WEB ページ開く
            try:
                engine.get(web_home)

                # 全要素取得待機
                engine_wait = WebDriverWait(engine, 10)
                element = engine_wait.until(EC.visibility_of_all_elements_located)

                # 最初のページ記憶
                engine_url = engine.current_url
                last_url   = engine_url

            except Exception as e:
                print(e)
                time.sleep(1.00)
                return False

            # WEB サーフィン
            try:
                while (True):
                    time.sleep(0.50)

                    # 閉じた？
                    try:
                        size = engine.get_window_size()
                    except Exception as e:
                        break

                    # 変化？
                    engine_url = engine.current_url
                    if (engine_url != last_url):

                        # 全要素取得待機
                        engine_wait = WebDriverWait(engine, 10)
                        element = engine_wait.until(EC.visibility_of_all_elements_located)

                        # 変化有り
                        engine_url = engine.current_url
                        last_url = engine_url
                        http_queue.put(['url',last_url])
                        print(last_url)

            except Exception as e:
                print(e)
                time.sleep(1.00)
                return False

            # WEB 停止
            try:
                engine.quit()
                engine = None
            except Exception as e:
                print(e)

            return True

        except Exception as e:
            print(e)
            time.sleep(1.00)

        return False

    def proc_fileexec(self, file_path='temp/_input/etc.png', ):

        if (not os.path.isfile(file_path)):
            return False

        try:
            if (os.name == 'nt'):
                path = file_path.replace('/', '\\')
                subp = subprocess.Popen(['cmd', '/c', path, ])
            else:
                subp = subprocess.Popen(['open', file_path, ])
            return True
        except Exception as e:
            print(e)

        return False



if __name__ == '__main__':

    gui_queue   = queue.Queue()
    clip_queue  = queue.Queue()
    http_queue  = queue.Queue()

    proc = _proc()

    proc.init(qLog_fn='', runMode='debug', limit_mode=True, 
             conf=None, addin=None, chatgui=None, chatgui_queue=None, chatbot=None, )

    text = 'おはよう'
    res = proc.proc_clip(gui_queue=gui_queue, clip_queue=clip_queue, clip_text=text, )

    text = 'https://ncode.syosetu.com/'
    res = proc.proc_clip(gui_queue=gui_queue, clip_queue=clip_queue, clip_text=text, )

    path = 'https://ncode.syosetu.com/n4830bu/1/'
    res = proc.proc_html(gui_queue=gui_queue, clip_queue=clip_queue, proc_path=path, )

    path = '_icons/_test.pdf'
    res = proc.proc_file(gui_queue=gui_queue, clip_queue=clip_queue, proc_path=path, )
    path = '_icons/_test_ocr.jpg'
    res = proc.proc_file(gui_queue=gui_queue, clip_queue=clip_queue, proc_path=path, )

    inpText = 'おはよう'
    res = proc.proc_gpt(gui_queue=gui_queue, clip_queue=clip_queue, 
                        gpt_inpText=inpText, 
                        file_path=[], interface='clip', chat_class='auto', session_id='admin', 
                        gpt_history=None, )

    proc.proc_browser(http_queue=http_queue, web_engine='chrome')


