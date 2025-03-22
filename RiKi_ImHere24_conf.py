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



config_file = 'RiKi_ImHere24_key.json'



class _conf:

    def __init__(self, ):
        self.runMode                        = 'debug'        
        self.run_priority                   = 'auto'

        self.gui_screen                     = 'auto'
        self.gui_panel                      = 'auto'
        self.gui_alpha                      = 'auto'
        self.gui_theme                      = 'Dark' # 'Default1', 'Dark',
        self.gui_keep_on_top                = 'auto'

        self.dev_intervalSec                = '10'
        self.ImHere_validSec                = '90'

        self.mouse_check                    = 'yes'
        self.keyboard_check                 = 'yes'
        self.cam_check                      = 'auto'

        self.cam_start                      = '0000'
        self.cam_end                        = '2359'
        self.cam_guide                      = 'auto'
        self.silent_start                   = '0910'
        self.silent_end                     = '0950'
        self.lunch_start                    = '1200'
        self.lunch_end                      = '1300'
        self.cv2_camScan                    = 'all'
        self.cv2_engine                     = 'yolov8'
        self.cv2_intervalSec                = '1'
        self.cv2_sabunLimit                 = '1'
        self.cv2_sometime                   = 'no'

        self.action60s_mouse                = 'yes'
        self.action60s_key                  = 'ctrl'
        self.feedback_mouse                 = 'yes'
        self.feedback_fileYes               = 'temp/control_ImHere_yes.txt'
        self.feedback_fileNo                = 'temp/control_ImHere_no.txt'

        self.reception_sound1_sttm          = '0500'
        self.reception_sound1_entm          = '0900'
        self.reception_sound1_file          = '_sounds/_voice_ohayou.mp3'
        self.reception_sound2_sttm          = '0900'
        self.reception_sound2_entm          = '1600'
        self.reception_sound2_file          = '_sounds/_sound_pingpong.mp3'
        self.reception_sound3_sttm          = '1600'
        self.reception_sound3_entm          = '1700'
        self.reception_sound3_file          = '_sounds/_voice_otukare.mp3'
        self.reception_sound4_sttm          = '1700'
        self.reception_sound4_entm          = '2200'
        self.reception_sound4_file          = '_sounds/_voice_sejyou.mp3'



    def init(self, qLog_fn='', runMode      = 'debug',
            gui_screen                      = 'auto',
            gui_panel                       = 'auto',
            camScan                         = '',
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

            dic['dev_intervalSec']          = self.dev_intervalSec
            dic['ImHere_validSec']          = self.ImHere_validSec

            dic['mouse_check']              = self.mouse_check
            dic['keyboard_check']           = self.keyboard_check
            dic['cam_check']                = self.cam_check

            dic['cam_start']                = self.cam_start
            dic['cam_end']                  = self.cam_end
            dic['cam_guide']                = self.cam_guide
            dic['silent_start']             = self.silent_start
            dic['silent_end']               = self.silent_end
            dic['lunch_start']              = self.lunch_start
            dic['lunch_end']                = self.lunch_end
            dic['cv2_camScan']              = self.cv2_camScan
            dic['cv2_engine']               = self.cv2_engine
            dic['cv2_intervalSec']          = self.cv2_intervalSec
            dic['cv2_sabunLimit']           = self.cv2_sabunLimit
            dic['cv2_sometime']             = self.cv2_sometime

            dic['action60s_mouse']          = self.action60s_mouse
            dic['action60s_key']            = self.action60s_key
            dic['feedback_mouse']           = self.feedback_mouse
            dic['feedback_fileYes']         = self.feedback_fileYes
            dic['feedback_fileNo']          = self.feedback_fileNo

            dic['reception_sound1_sttm']    = self.reception_sound1_sttm
            dic['reception_sound1_entm']    = self.reception_sound1_entm
            dic['reception_sound1_file']    = self.reception_sound1_file
            dic['reception_sound2_sttm']    = self.reception_sound2_sttm
            dic['reception_sound2_entm']    = self.reception_sound2_entm
            dic['reception_sound2_file']    = self.reception_sound2_file
            dic['reception_sound3_sttm']    = self.reception_sound3_sttm
            dic['reception_sound3_entm']    = self.reception_sound3_entm
            dic['reception_sound3_file']    = self.reception_sound3_file
            dic['reception_sound4_sttm']    = self.reception_sound4_sttm
            dic['reception_sound4_entm']    = self.reception_sound4_entm
            dic['reception_sound4_file']    = self.reception_sound4_file

            res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )

        if (res == True):
            self.run_priority               = dic['run_priority']

            self.gui_screen                 = dic['gui_screen']
            self.gui_panel                  = dic['gui_panel']
            self.gui_alpha                  = dic['gui_alpha']
            self.gui_theme                  = dic['gui_theme']
            self.gui_keep_on_top            = dic['gui_keep_on_top']

            self.dev_intervalSec            = dic['dev_intervalSec']
            self.ImHere_validSec            = dic['ImHere_validSec']

            self.mouse_check                = dic['mouse_check']
            self.keyboard_check             = dic['keyboard_check']
            self.cam_check                  = dic['cam_check']

            self.cam_start                  = dic['cam_start']
            self.cam_end                    = dic['cam_end']
            self.cam_guide                  = dic['cam_guide']
            self.silent_start               = dic['silent_start']
            self.silent_end                 = dic['silent_end']
            self.lunch_start                = dic['lunch_start']
            self.lunch_end                  = dic['lunch_end']
            self.cv2_camScan                = dic['cv2_camScan']
            self.cv2_engine                 = dic['cv2_engine']
            self.cv2_intervalSec            = dic['cv2_intervalSec']
            self.cv2_sabunLimit             = dic['cv2_sabunLimit']
            self.cv2_sometime               = dic['cv2_sometime']

            self.action60s_mouse            = dic['action60s_mouse']
            self.action60s_key              = dic['action60s_key']
            self.feedback_mouse             = dic['feedback_mouse']
            self.feedback_fileYes           = dic['feedback_fileYes']
            self.feedback_fileNo            = dic['feedback_fileNo']

            self.reception_sound1_sttm      = dic['reception_sound1_sttm']
            self.reception_sound1_entm      = dic['reception_sound1_entm']
            self.reception_sound1_file      = dic['reception_sound1_file']
            self.reception_sound2_sttm      = dic['reception_sound2_sttm']
            self.reception_sound2_entm      = dic['reception_sound2_entm']
            self.reception_sound2_file      = dic['reception_sound2_file']
            self.reception_sound3_sttm      = dic['reception_sound3_sttm']
            self.reception_sound3_entm      = dic['reception_sound3_entm']
            self.reception_sound3_file      = dic['reception_sound3_file']
            self.reception_sound4_sttm      = dic['reception_sound4_sttm']
            self.reception_sound4_entm      = dic['reception_sound4_entm']
            self.reception_sound4_file      = dic['reception_sound4_file']

        self.runMode                        = runMode
        if (gui_screen != ''):
            self.gui_screen                 = gui_screen
        if (gui_panel != ''):
            self.gui_panel                  = gui_panel
        if (camScan != ''):
            self.cv2_camScan                = camScan

        if (runMode == 'reception'):
            if (self.gui_screen == 'auto'):
                self.gui_screen             = '0'
            if (self.gui_panel  == 'auto'):
                self.gui_panel              = '8-'
            if (self.gui_alpha  == 'auto'):
                self.gui_alpha              = '0.5'
            if (self.gui_keep_on_top == 'auto'):
                self.gui_keep_on_top        = 'yes'
            self.action60s_mouse            = 'no'
            self.action60s_key              = ''
            self.feedback_mouse             = 'no'

        if (runMode == 'personal'):
            if (self.gui_screen == 'auto'):
                self.gui_screen             = '0'
            if (self.gui_panel  == 'auto'):
                self.gui_panel              = '8-'
            if (self.gui_alpha  == 'auto'):
                self.gui_alpha              = '0.5'
            if (self.gui_keep_on_top == 'auto'):
                self.gui_keep_on_top        = 'yes'
            self.cam_check                  = 'auto'
            self.cam_start                  = '0000'
            self.cam_end                    = '2359'
            self.cam_guide                  = 'auto'
            self.silent_start               = '0000'
            self.silent_end                 = '0000'
            self.lunch_start                = '0000'
            self.lunch_end                  = '0000'
            self.reception_sound1_file      = ''
            self.reception_sound2_file      = ''
            self.reception_sound3_file      = ''
            self.reception_sound4_file      = ''

        if (runMode == 'camera'):
            if (self.gui_screen == 'auto'):
                self.gui_screen             = '0'
            if (self.gui_panel  == 'auto'):
                self.gui_panel              = '5+'
            if (self.gui_alpha  == 'auto'):
                self.gui_alpha              = '0.9'
            self.gui_alpha                  = '1.0'
            if (self.gui_keep_on_top == 'auto'):
                self.gui_keep_on_top        = 'no'
            self.mouse_check                = 'no'
            self.cam_check                  = 'yes'
            self.cam_start                  = '0000'
            self.cam_end                    = '2359'
            self.cam_guide                  = 'yes'
            self.silent_start               = '0000'
            self.silent_end                 = '0000'
            self.lunch_start                = '0000'
            self.lunch_end                  = '0000'
            self.action60s_mouse            = 'no'
            self.action60s_key              = ''
            self.feedback_mouse             = 'no'
            self.reception_sound1_file      = ''
            self.reception_sound3_file      = ''
            self.reception_sound4_file      = ''
            self.reception_sound2_sttm      = self.cam_start
            self.reception_sound2_entm      = self.cam_end

        return True



if __name__ == '__main__':

    conf = _conf()

    # conf 初期化
    runMode   = 'debug'
    conf.init(qLog_fn='', runMode=runMode, )

    # テスト
    print(conf.runMode)


