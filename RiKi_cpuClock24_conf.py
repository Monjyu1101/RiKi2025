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



config_file = 'RiKi_cpuClock24_key.json'



class _conf:

    def __init__(self, ):
        self.runMode                        = 'debug'        
        self.run_priority                   = 'auto'

        self.gui_screen                     = 'auto'
        self.gui_panel                      = 'auto'
        self.gui_alpha                      = 'auto'
        self.gui_theme                      = 'Dark' # 'Default1', 'Dark',
        self.gui_keep_on_top                = 'yes'

        self.clock_design                   = 'auto'
        self.dev_intervalSec                = '5'

        self.telop_path                     = 'temp/d6_7telop_txt/'
        self.tts_path                       = 'temp/s6_5tts_txt/'
        self.tts_header                     = 'ja,google,'
        self.timeSign_sound                 = '_sounds/_sound_SeatBeltSign1.mp3'
        self.timeSign_telop                 = 'yes'
        self.timeSign_tts                   = 'no'

        self.analog_pltStyle                = 'dark_background'
        self.analog_b_fcolor                = 'white'
        self.analog_b_tcolor                = 'fuchsia'
        self.analog_b_bcolor                = 'black'
        self.analog_s_fcolor                = 'red'
        self.analog_s_bcolor1               = 'darkred'
        self.analog_s_bcolor2               = 'tomato'
        self.analog_m_fcolor                = 'cyan'
        self.analog_m_bcolor1               = 'darkgreen'
        self.analog_m_bcolor2               = 'limegreen'
        self.analog_h_fcolor                = 'cyan'
        self.analog_h_bcolor1               = 'darkblue'
        self.analog_h_bcolor2               = 'deepskyblue'
        self.digital_b_fcolor               = 'white'
        self.digital_b_tcolor               = 'fuchsia'
        self.digital_b_bcolor               = 'black'



    def init(self, qLog_fn='', runMode      = 'debug',
            gui_screen                      = 'auto',
            gui_panel                       = 'auto',
            clock_design                    = 'auto',
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
            dic['gui_theme']                = self.gui_theme
            dic['gui_keep_on_top']          = self.gui_keep_on_top

            dic['clock_design']             = self.clock_design
            dic['dev_intervalSec']          = self.dev_intervalSec

            dic['telop_path']               = self.telop_path
            dic['tts_path']                 = self.tts_path
            dic['tts_header']               = self.tts_header
            dic['timeSign_sound']           = self.timeSign_sound
            dic['timeSign_telop']           = self.timeSign_telop
            dic['timeSign_tts']             = self.timeSign_tts

            dic['analog_pltStyle']          = self.analog_pltStyle
            dic['analog_b_fcolor']          = self.analog_b_fcolor
            dic['analog_b_tcolor']          = self.analog_b_tcolor
            dic['analog_b_bcolor']          = self.analog_b_bcolor
            dic['analog_s_fcolor']          = self.analog_s_fcolor
            dic['analog_s_bcolor1']         = self.analog_s_bcolor1
            dic['analog_s_bcolor2']         = self.analog_s_bcolor2
            dic['analog_m_fcolor']          = self.analog_m_fcolor
            dic['analog_m_bcolor1']         = self.analog_m_bcolor1
            dic['analog_m_bcolor2']         = self.analog_m_bcolor2
            dic['analog_h_fcolor']          = self.analog_h_fcolor
            dic['analog_h_bcolor1']         = self.analog_h_bcolor1
            dic['analog_h_bcolor2']         = self.analog_h_bcolor2
            dic['digital_b_fcolor']         = self.digital_b_fcolor
            dic['digital_b_tcolor']         = self.digital_b_tcolor
            dic['digital_b_bcolor']         = self.digital_b_bcolor

            res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )

        if (res == True):
            self.run_priority               = dic['run_priority']

            self.gui_screen                 = dic['gui_screen']
            self.gui_panel                  = dic['gui_panel']
            self.gui_alpha                  = dic['gui_alpha']
            self.gui_theme                  = dic['gui_theme']
            self.gui_keep_on_top            = dic['gui_keep_on_top']

            self.clock_design               = dic['clock_design']
            self.dev_intervalSec            = dic['dev_intervalSec']

            self.telop_path                 = dic['telop_path']
            self.tts_path                   = dic['tts_path']
            self.tts_header                 = dic['tts_header']
            self.timeSign_sound             = dic['timeSign_sound']
            self.timeSign_telop             = dic['timeSign_telop']
            self.timeSign_tts               = dic['timeSign_tts']

            self.analog_pltStyle            = dic['analog_pltStyle']
            self.analog_b_fcolor            = dic['analog_b_fcolor']
            self.analog_b_tcolor            = dic['analog_b_tcolor']
            self.analog_b_bcolor            = dic['analog_b_bcolor']
            self.analog_s_fcolor            = dic['analog_s_fcolor']
            self.analog_s_bcolor1           = dic['analog_s_bcolor1']
            self.analog_s_bcolor2           = dic['analog_s_bcolor2']
            self.analog_m_fcolor            = dic['analog_m_fcolor']
            self.analog_m_bcolor1           = dic['analog_m_bcolor1']
            self.analog_m_bcolor2           = dic['analog_m_bcolor2']
            self.analog_h_fcolor            = dic['analog_h_fcolor']
            self.analog_h_bcolor1           = dic['analog_h_bcolor1']
            self.analog_h_bcolor2           = dic['analog_h_bcolor2']
            self.digital_b_fcolor           = dic['digital_b_fcolor']
            self.digital_b_tcolor           = dic['digital_b_tcolor']
            self.digital_b_bcolor           = dic['digital_b_bcolor']

        self.runMode                        = runMode
        if (gui_screen != ''):
            self.gui_screen                 = gui_screen
        if (gui_panel != ''):
            self.gui_panel                  = gui_panel
        if (clock_design != ''):
            self.clock_design               = clock_design

        if (runMode == 'analog'):
            if (self.gui_alpha == 'auto'):
                self.gui_alpha = '0.9'
            if (self.gui_keep_on_top == 'auto'):
                self.gui_keep_on_top = 'no'

        if (runMode == 'digital'):
            if (self.gui_alpha == 'auto'):
                self.gui_alpha = '0.9'
            if (self.gui_keep_on_top == 'auto'):
                self.gui_keep_on_top = 'no'

        if (runMode == 'personal'):
            if (self.gui_alpha == 'auto'):
                self.gui_alpha = '0.2'
            if (self.gui_keep_on_top == 'auto'):
                self.gui_keep_on_top = 'yes'

        return True



if __name__ == '__main__':

    conf = _conf()

    # conf 初期化
    runMode   = 'debug'
    conf.init(qLog_fn='', runMode=runMode, )

    # テスト
    print(conf.runMode)


