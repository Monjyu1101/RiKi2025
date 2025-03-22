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

import numpy as np
import cv2

import keyboard



# インターフェース
qPath_temp = 'temp/'
qPath_log  = 'temp/_log/'
qPath_rec  = 'temp/_recorder/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



# 標準フォルダ
qPath_pictures   = qPath_temp
qPath_videos     = qPath_temp
if (os.name == 'nt'):
    qUSERNAME = os.environ["USERNAME"]
    qPath_pictures  = 'C:/Users/' + qUSERNAME + '/Pictures/RiKi/'
    qPath_videos    = 'C:/Users/' + qUSERNAME + '/Videos/RiKi/'
    qFunc.makeDirs(qPath_pictures, remove=False, )
    qFunc.makeDirs(qPath_videos,   remove=False, )
else:
    qUSERNAME = os.environ["USER"]



class _proc:

    def __init__(self, ):
        self.runMode   = 'debug'

        # キーボード監視 開始
        self.last_key_time = 0
        self.kb_handler_id = None
        self.start_kb_listener()

    # キーボード監視 開始
    def start_kb_listener(self, runMode='assistant',):
        # イベントハンドラの登録
        self.last_key_time = 0
        self.kb_handler_id = keyboard.hook(self._keyboard_event_handler)
    # イベントハンドラ
    def _keyboard_event_handler(self, event):
        self.last_key_time = time.time()

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



    def save_photo(self, image, hit_name='photo', ):
        nowTime  = datetime.datetime.now()
        stamp    = nowTime.strftime('%Y%m%d.%H%M%S')
        yyyymmdd = stamp[:8]

        # 写真保存
        main_file = ''
        try:
            if (image is not None):
                main_file = qPath_rec + stamp + '.' + hit_name + '.jpg'
                cv2.imwrite(main_file, image)
        except Exception as e:
            main_file = ''

        # 写真コピー保存
        if (main_file != ''):
            if (qPath_pictures != ''):
                folder = qPath_pictures + yyyymmdd + '/'
                qFunc.makeDirs(folder)
                qFunc.copy(main_file, folder + stamp + '.' + hit_name + '.jpg')

        return True



if __name__ == '__main__':

    proc = _proc()

    proc.init(qLog_fn='', runMode='debug',  )



