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

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# 共通ルーチン
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

import _v6__qRiKi_key
qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()



config_file = 'RiKi_halloTelop24_key.json'



class _conf:

    def __init__(self, ):
        self.runMode                        = 'debug'        
        self.run_priority                   = 'auto'

        self.gui_screen                     = 'auto'
        self.gui_panel                      = 'auto'
        self.gui_alpha                      = '1.0'
        self.gui_keep_on_top                = 'yes'

        self.mouse_check                    = 'auto'
        self.video_nullSec                  = '1.0'
        self.video_beforeSec                = '3.0'
        self.video_afterSec                 = '1.0'
        self.video_fps                      = '60'
        self.video_moveStep                 = '4'
        self.telop_limitSec                 = '300'
        self.telop_limitPlay                = '2'
        self.telop_bgColor                  = '(0,0,0)'
        self.telop_fgColor                  = '(0,165,255)'

    def init(self, qLog_fn='', runMode      = 'debug',
             screen                         = 'auto',
             panel                          = 'auto',
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
            dic['_crypt_']                  = 'none'
            dic['run_priority']             = self.run_priority

            dic['gui_screen']               = self.gui_screen
            dic['gui_panel']                = self.gui_panel
            dic['gui_alpha']                = self.gui_alpha
            dic['gui_keep_on_top']          = self.gui_keep_on_top

            dic['mouse_check']              = self.mouse_check
            dic['video_nullSec']            = self.video_nullSec
            dic['video_beforeSec']          = self.video_beforeSec
            dic['video_afterSec']           = self.video_afterSec
            dic['video_fps']                = self.video_fps
            dic['video_moveStep']           = self.video_moveStep
            dic['telop_limitSec']           = self.telop_limitSec
            dic['telop_limitPlay']          = self.telop_limitPlay
            dic['telop_bgColor']            = self.telop_bgColor
            dic['telop_fgColor']            = self.telop_fgColor

            res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )

        if (res == True):
            self.run_priority               = dic['run_priority']

            self.gui_screen                 = dic['gui_screen']
            self.gui_panel                  = dic['gui_panel']
            self.gui_alpha                  = dic['gui_alpha']
            self.gui_keep_on_top            = dic['gui_keep_on_top']

            self.mouse_check                = dic['mouse_check']
            self.video_nullSec              = dic['video_nullSec']
            self.video_beforeSec            = dic['video_beforeSec']
            self.video_afterSec             = dic['video_afterSec']
            self.video_fps                  = dic['video_fps']
            self.video_moveStep             = dic['video_moveStep']
            self.telop_limitSec             = dic['telop_limitSec']
            self.telop_limitPlay            = dic['telop_limitPlay']
            self.telop_bgColor              = dic['telop_bgColor']
            self.telop_fgColor              = dic['telop_fgColor']

            self.telop_bgColor_val          = eval(self.telop_bgColor)
            self.telop_fgColor_val          = eval(self.telop_fgColor)

        self.runMode = runMode
        if (screen != ''):
            self.gui_screen = screen
        if (panel != ''):
            self.gui_panel  = panel

        if (runMode == 'personal'):
            if (self.gui_panel == 'auto'):
                self.gui_panel = '1t'
            if (self.mouse_check == 'auto'):
                self.mouse_check   = 'no'
        else:
            if (self.gui_screen == 'auto'):
                self.gui_screen = '0'
            if (self.gui_panel == 'auto'):
                self.gui_panel = '789t'
            if (self.mouse_check == 'auto'):
                self.mouse_check   = 'yes'

        return True



if __name__ == '__main__':

    conf = _conf()

    # conf 初期化
    runMode   = 'debug'
    conf.init(qLog_fn='', runMode=runMode, )

    # テスト
    print(conf.runMode)
    print(conf.telop_bgColor, conf.telop_bgColor_val)
    print(conf.telop_fgColor, conf.telop_fgColor_val)


