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

from playsound3 import playsound

import io
if (os.name == 'nt'):
    import win32clipboard

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



class _func:

    def __init__(self, ):

        self.runMode                    = 'debug'

        self.txt_input_path             = 'temp/chat_input/'
        self.txt_output_path            = 'temp/chat_output/'
        self.stt_path                   = 'temp/s6_4stt_txt/'
        self.tts_path                   = 'temp/s6_5tts_txt/'
        self.tts_header                 = 'ja,free,' 

        self.feedback_popup             = 'no'
        self.feedback_mouse             = 'yes'
        self.feedback_key               = 'ctrl'
        self.feedback_sound             = 'yes'
        self.feedback_sound_accept_file = '_sounds/_sound_accept.mp3'
        self.feedback_sound_ok_file     = '_sounds/_sound_ok.mp3'
        self.feedback_sound_ng_file     = '_sounds/_sound_ng.mp3'

        self.tts_file_seq               = 0

    def init(self, qLog_fn='', runMode='debug', conf=None, ):

        self.runMode                        = runMode
        self.conf                           = conf

        # ログ
        self.proc_name = 'func'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')

        if (conf is not None):
            self.txt_input_path             = conf.txt_input_path
            self.txt_output_path            = conf.txt_output_path
            self.stt_path                   = conf.stt_path
            self.tts_path                   = conf.tts_path
            self.tts_header                 = conf.tts_header

            self.feedback_popup             = conf.feedback_popup
            self.feedback_mouse             = conf.feedback_mouse
            self.feedback_key               = conf.feedback_key
            self.feedback_sound             = conf.feedback_sound
            self.feedback_sound_accept_file = conf.feedback_sound_accept_file
            self.feedback_sound_ok_file     = conf.feedback_sound_ok_file
            self.feedback_sound_ng_file     = conf.feedback_sound_ng_file

        return True

    def txt_read(self, remove=True, path='temp/chat_input/', ):
        res_text = ''
        res_file = None

        #path = self.stt_path
        path_files = glob.glob(path + '*.txt')
        path_files.sort()
        if (len(path_files) > 0):

            for f in path_files:

                try:

                    proc_file = f.replace('\\', '/')

                    if (proc_file[-4:].lower() == '.txt' and proc_file[-8:].lower() != '.wrk.txt'):
                        f1 = proc_file
                        f2 = proc_file[:-4] + '.wrk.txt'
                        try:
                            os.rename(f1, f2)
                            proc_file = f2
                        except Exception as e:
                            pass

                    if (proc_file[-8:].lower() == '.wrk.txt'):
                        f1 = proc_file
                        f2 = proc_file[:-8] + proc_file[-4:]
                        try:
                            os.rename(f1, f2)
                            proc_file = f2
                        except Exception as e:
                            pass

                        if (proc_file[-9:].lower() != '_sjis.txt'):
                            txts, _ = qFunc.txtsRead(proc_file, encoding='utf-8', exclusive=False, )
                        else:
                            txts, _ = qFunc.txtsRead(proc_file, encoding='shift_jis', exclusive=False, )

                        text = ''
                        for t in txts:
                            t = str(t).rstrip()
                            if (t != ''):
                                text += t + '\n'

                        if (remove == True):
                            qFunc.remove(proc_file)

                        if (text != '') and (text != '!'):
                            res_text = text
                            res_file = proc_file
                            break;

                except Exception as e:
                    print(e)

        return res_text, res_file

    def tts_write(self, text='', ):
        res = False

        text = text.replace('\r','\n')
        text = text.replace('／','/')
        text = text.replace('/','スラッシュ')
        hit = True
        while (hit == True):
            if (text.find('\n\n')>0):
                hit = True
                text = text.replace('\n\n', '\n')
            else:
                hit = False
        #text = text.strip()

        if (text.strip() == '') or (text.strip() == '!'):
            return False

        else:

            txts = text.splitlines()
            if (len(txts) >= 2):
                if (txts[0][:1] == '['):
                    x = txts.pop(0)

            for text in txts:
                if (text != ''):

                    now   = datetime.datetime.now()
                    stamp = now.strftime('%Y%m%d%H%M%S')
                    self.tts_file_seq += 1
                    if (self.tts_file_seq > 9999):
                        self.tts_file_seq = 1
                    seq4 = '{:04}'.format(self.tts_file_seq)
                    filename = self.tts_path + stamp + '.' + seq4 + '.txt'

                    # TTS
                    # 標準出力先の場合
                    if (self.tts_path == 'temp/s6_5tts_txt/'):
                        text = self.tts_header + text
                        res = qFunc.txtsWrite(filename, txts=[text], mode='w', exclusive=True, )

                    # 標準以外の出力先の場合
                    else:
                        text = text
                        res = qFunc.txtsWrite(filename, txts=[text], mode='w', exclusive=True, )

        return True

    def feedback_action(self, mode='ok', ):

        if (mode == 'accept'):
            #if (self.feedback_key != ''):
            #    try:
            #        qGUI.press(self.feedback_key)
            #    except:
            #        pass
            if (self.feedback_sound.lower() != 'no'):
                if (self.feedback_sound_accept_file != ''):
                    if (os.path.isfile(self.feedback_sound_accept_file)):
                        try:
                            # 再生
                            playsound(sound=self.feedback_sound_accept_file, block=False, )
                        except Exception as e:
                            print(e)
        
        elif (mode == 'ok'):
            if (str(self.feedback_popup).lower() == 'no'):
                if (self.feedback_popup.lower() == 'no'):
                    if (self.feedback_key != ''):
                        try:
                            qGUI.press(self.feedback_key)
                        except:
                            pass
                if (self.feedback_sound.lower() != 'no'):
                    if (self.feedback_sound_ok_file != ''):
                        if (os.path.isfile(self.feedback_sound_ok_file)):
                            try:
                                # 再生
                                playsound(sound=self.feedback_sound_ok_file, block=False, )
                            except Exception as e:
                                print(e)

        else: # ng
            if (str(self.feedback_popup).lower() == 'no'):
                if (self.feedback_key != ''):
                    try:
                        qGUI.press(self.feedback_key)
                    except:
                        pass
                if (self.feedback_sound.lower() != 'no'):
                    if (self.feedback_sound_ng_file != ''):
                        if (os.path.isfile(self.feedback_sound_ng_file)):
                            try:
                                # 再生
                                playsound(sound=self.feedback_sound_ng_file, block=False, )
                            except Exception as e:
                                print(e)
                if (self.feedback_key != ''):
                    try:
                        time.sleep(0.50)
                        qGUI.press(self.feedback_key)
                    except:
                        pass
 
        return True

    def image_to_clipboard(self, image=None, ):
        if (os.name != 'nt'):
            return False
        if (image is None):
            return False

        # メモリストリームにBMP形式で保存する
        bitmap = io.BytesIO()
        image.convert('RGB').save(bitmap, 'BMP')
        data = bitmap.getvalue()[14:]
        bitmap.close()

        # クリップボードにデータをセットする
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

        return True



if __name__ == '__main__':

    func = _func()

    func.init(qLog_fn='', runMode='debug', conf=None, )

    res = func.stt_read(remove=False, )
    print(res)

    res = func.tts_write(text='テスト')
    print(res)

    res = func.feedback_action('accept')
    print(res)
    time.sleep(2)
    res = func.feedback_action('ok')
    print(res)
    time.sleep(2)
    res = func.feedback_action('ng')
    print(res)
    time.sleep(2)

