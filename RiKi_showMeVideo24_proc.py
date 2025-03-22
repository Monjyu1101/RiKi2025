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
qPath_temp = 'temp/'
qPath_log  = 'temp/_log/'
qPath_work = 'temp/_work/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



class _proc:

    def __init__(self, ):
        self.runMode = 'debug'

        self.file_seq = 0

        self.telop_path                     = 'temp/d6_7telop_txt/'
        self.tts_path                       = 'temp/s6_5tts_txt/'
        self.tts_header                     = 'ja,google,'



    def init(self, qLog_fn='', runMode='debug', conf=None, ):

        self.runMode   = runMode

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
        self.logDisp = True



    # cpuClock,saap_worker 同一ロジック
    def telopMSG(self, title='Message', txt='', ):
        if (txt == ''):
            return False
        if (self.telop_path == ''):
            return False
        if (not os.path.isdir(self.telop_path)):
            return False
        if (title.find('【') < 0):
            title = '【' + title + '】'
        txt = title + '\r\n' + txt

        now   = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d%H%M%S')
        self.file_seq += 1
        if (self.file_seq > 9999):
            self.file_seq = 1
        seq4 = '{:04}'.format(self.file_seq)

        filename = self.telop_path + stamp + '.' + seq4 + '.txt'

        res = qFunc.txtsWrite(filename, txts=[txt], mode='w', exclusive=True, )
        if (res == False):
            qLog.log('critical', self.proc_id, '★Telop書込エラー', )
            return False        

        return True        

    # cpuClock,saap_worker 同一ロジック
    def ttsMSG(self, title='Message', txt='', ):
        if (txt == ''):
            return False
        if (self.tts_path == ''):
            return False
        if (not os.path.isdir(self.tts_path)):
            return False
        txt = txt.replace('\r',' ')
        txt = txt.replace('\n',' ')
        txt = txt.replace('／','/')
        txt = txt.replace('/','スラッシュ')

        now   = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d%H%M%S')
        self.file_seq += 1
        if (self.file_seq > 9999):
            self.file_seq = 1
        seq4 = '{:04}'.format(self.file_seq)

        filename = self.tts_path + stamp + '.' + seq4 + '.txt'

        # 個人利用時のWINOSは、直接発声！
        #if  (self.runMode == 'personal') \
        #and (self.tts_header == 'ja,winos,') \
        #and (os.name == 'nt'):

        #    winosAPI = winos_api.SpeechAPI()
        #    res = winosAPI.authenticate()
        #    if (res == False):
        #        qLog.log('critical', self.proc_id, '★winosAPI(speech)認証エラー', )
        #        return False        

        #    try:
        #        filename = filename[:-4] + '.mp3'
        #        res, api = winosAPI.vocalize(outText=txt, outLang='ja', outFile=filename, )
        #        if (res != ''):

        #            sox = subprocess.Popen(['sox', filename, '-d', '-q'], )
        #            #sox.wait()
        #            #sox.terminate()
        #            #sox = None

        #    except:
        #        qLog.log('critical', self.proc_id, '★winosAPI(speech)利用エラー', )
        #        return False

        #else:
        if True:

            txt = self.tts_header + txt
            res = qFunc.txtsWrite(filename, txts=[txt], mode='w', exclusive=True, )
            if (res == False):
                qLog.log('critical', self.proc_id, '★TTS書込エラー', )
                return False        

        return True



if __name__ == '__main__':

    proc = _proc()

    proc.init(qLog_fn='', runMode='debug',  )



