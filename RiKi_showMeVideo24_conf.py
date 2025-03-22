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



config_file = 'RiKi_showMeVideo24_key.json'



class _conf:

    def __init__(self, ):
        self.runMode                        = 'debug'        
        self.run_priority                   = 'auto'
        self.run_limitSec                   = 'auto'

        self.engine                         = 'ffplay'
        self.telop_path                     = 'temp/d6_7telop_txt/'
        self.shuffle_play                   = 'yes'
        self.img2mov_play                   = 'yes'
        self.img2mov_sec                    = 60
        self.img2mov_zoom                   = 'yes'

        self.play_screen                    = 'auto'
        self.play_panel                     = 'auto'
        self.play_path_winos                = 'C:/Users/Public/'
        self.play_path_macos                = '/Users/Shared/'
        self.play_path_linux                = '/users/kondou/Documents/'
        self.play_folder                    = '_m4v__Clip/Perfume/'
        self.play_volume                    = 100
        self.play_fadeActionSec             = 0
        self.play_file_telop                = 'no'
        self.play_changeSec                 = 0
        self.play_stopByMouseSec            = 0

        self.bgm_screen                     = 'auto'
        self.bgm_panel                      = 'auto'
        self.bgm_folder                     = 'BGM/'
        self.bgm_volume                     = 20
        self.bgm_fadeActionSec              = 0
        self.bgm_file_telop                 = 'yes'
        self.bgm_changeSec                  = 600
        self.bgm_stopByMouseSec             = 180

        self.bgv_screen                     = 'auto'
        self.bgv_panel                      = 'auto'
        self.bgv_folder                     = 'BGV/'
        self.bgv_volume                     = 0
        self.bgv_fadeActionSec              = 0
        self.bgv_file_telop                 = 'no'
        self.bgv_changeSec                  = 300
        self.bgv_stopByMouseSec             = 180
        self.bgv_overlayTime                = 'yes'
        self.bgv_overlayDate                = 'yes'

        self.day_control                    = 'yes'
        self.day_start                      = '06:25:00'
        self.day_end                        = '18:35:00'
        self.silent_control                 = 'yes'
        self.silent_start                   = '09:10:00'
        self.silent_end                     = '09:50:00'
        self.lunch_control                  = 'yes'
        self.lunch_start                    = '12:00:00'
        self.lunch_end                      = '13:00:00'



    def init(self, qLog_fn='', runMode      = 'debug',
             screen                         = '',
             panel                          = '',
             path                           = '',
             folder                         = '',
             volume                         = '', 
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
            dic['run_limitSec']             = self.run_limitSec

            dic['engine']                   = self.engine
            dic['telop_path']               = self.telop_path
            dic['shuffle_play']             = self.shuffle_play
            dic['img2mov_play']             = self.img2mov_play
            dic['img2mov_sec']              = self.img2mov_sec
            dic['img2mov_zoom']             = self.img2mov_zoom

            dic['play_screen']              = self.play_screen
            dic['play_panel']               = self.play_panel
            dic['play_path_winos']          = self.play_path_winos
            dic['play_path_macos']          = self.play_path_macos
            dic['play_path_linux']          = self.play_path_linux
            dic['play_folder']              = self.play_folder
            dic['play_volume']              = self.play_volume
            dic['play_fadeActionSec']       = self.play_fadeActionSec
            dic['play_file_telop']          = self.play_file_telop
            dic['play_changeSec']           = self.play_changeSec
            dic['play_stopByMouseSec']      = self.play_stopByMouseSec

            dic['bgm_screen']               = self.bgm_screen
            dic['bgm_panel']                = self.bgm_panel
            dic['bgm_folder']               = self.bgm_folder
            dic['bgm_volume']               = self.bgm_volume
            dic['bgm_fadeActionSec']        = self.bgm_fadeActionSec
            dic['bgm_file_telop']           = self.bgm_file_telop
            dic['bgm_changeSec']            = self.bgm_changeSec
            dic['bgm_stopByMouseSec']       = self.bgm_stopByMouseSec

            dic['bgv_screen']               = self.bgv_screen
            dic['bgv_panel']                = self.bgv_panel
            dic['bgv_folder']               = self.bgv_folder
            dic['bgv_volume']               = self.bgv_volume
            dic['bgv_fadeActionSec']        = self.bgv_fadeActionSec
            dic['bgv_file_telop']           = self.bgv_file_telop
            dic['bgv_changeSec']            = self.bgv_changeSec
            dic['bgv_stopByMouseSec']       = self.bgv_stopByMouseSec
            dic['bgv_overlayTime']          = self.bgv_overlayTime
            dic['bgv_overlayDate']          = self.bgv_overlayDate

            dic['day_control']              = self.day_control
            dic['day_start']                = self.day_start
            dic['day_end']                  = self.day_end
            dic['silent_control']           = self.silent_control
            dic['silent_start']             = self.silent_start
            dic['silent_end']               = self.silent_end
            dic['lunch_control']            = self.lunch_control
            dic['lunch_start']              = self.lunch_start
            dic['lunch_end']                = self.lunch_end

            res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )

        if (res == True):
            self.run_priority               = dic['run_priority']
            self.run_limitSec               = dic['run_limitSec']

            self.engine                     = dic['engine']
            self.telop_path                 = dic['telop_path']
            self.shuffle_play               = dic['shuffle_play']
            self.img2mov_play               = dic['img2mov_play']
            self.img2mov_sec                = dic['img2mov_sec']
            self.img2mov_zoom               = dic['img2mov_zoom']

            self.play_screen                = dic['play_screen']
            self.play_panel                 = dic['play_panel']
            self.play_path_winos            = dic['play_path_winos']
            self.play_path_macos            = dic['play_path_macos']
            self.play_path_linux            = dic['play_path_linux']
            self.play_folder                = dic['play_folder']
            self.play_volume                = dic['play_volume']
            self.play_fadeActionSec         = dic['play_fadeActionSec']
            self.play_file_telop            = dic['play_file_telop']
            self.play_changeSec             = dic['play_changeSec']
            self.play_stopByMouseSec        = dic['play_stopByMouseSec']

            self.bgm_screen                 = dic['bgm_screen']
            self.bgm_panel                  = dic['bgm_panel']
            self.bgm_folder                 = dic['bgm_folder']
            self.bgm_volume                 = dic['bgm_volume']
            self.bgm_fadeActionSec          = dic['bgm_fadeActionSec']
            self.bgm_file_telop             = dic['bgm_file_telop']
            self.bgm_changeSec              = dic['bgm_changeSec']
            self.bgm_stopByMouseSec         = dic['bgm_stopByMouseSec']

            self.bgv_screen                 = dic['bgv_screen']
            self.bgv_panel                  = dic['bgv_panel']
            self.bgv_folder                 = dic['bgv_folder']
            self.bgv_volume                 = dic['bgv_volume']
            self.bgv_fadeActionSec          = dic['bgv_fadeActionSec']
            self.bgv_file_telop             = dic['bgv_file_telop']
            self.bgv_changeSec              = dic['bgv_changeSec']
            self.bgv_stopByMouseSec         = dic['bgv_stopByMouseSec']
            self.bgv_overlayTime            = dic['bgv_overlayTime']
            self.bgv_overlayDate            = dic['bgv_overlayDate']

            self.day_control                = dic['day_control']
            self.day_start                  = dic['day_start']
            self.day_end                    = dic['day_end']
            self.silent_control             = dic['silent_control']
            self.silent_start               = dic['silent_start']
            self.silent_end                 = dic['silent_end']
            self.lunch_control              = dic['lunch_control']
            self.lunch_start                = dic['lunch_start']
            self.lunch_end                  = dic['lunch_end']

        # 実行時間
        if (self.run_limitSec == 'auto'):
            self.run_limitSec = 0
            if (runMode == 'bgm') or (runMode == 'bgmusic') \
            or (runMode == 'bgmdrive') \
            or (runMode == 'bgv') or (runMode == 'bgvideo'):
                self.run_limitSec = 3600 * 3 #3時間
        self.run_limitSec = int(self.run_limitSec)

        # 日時表示
        self.play_overlayTime = 'no'
        self.play_overlayDate = 'no'
        if   (runMode == 'bgm') or (runMode == 'bgmusic') \
        or   (runMode == 'bgmdrive'):
            self.play_screen         = self.bgm_screen
            self.play_panel          = self.bgm_panel
            #self.play_path           = self.bgm_path
            self.play_folder         = self.bgm_folder
            self.play_volume         = self.bgm_volume
            self.play_fadeActionSec  = self.bgm_fadeActionSec
            self.play_file_telop     = self.bgm_file_telop
            self.play_changeSec      = self.bgm_changeSec
            self.play_stopByMouseSec = self.bgm_stopByMouseSec
            self.play_overlayTime    = 'no'
            self.play_overlayDate    = 'no'

        elif (runMode == 'bgv') or (runMode == 'bgvideo'):
            self.play_screen         = self.bgv_screen
            self.play_panel          = self.bgv_panel
            #self.play_path           = self.bgv_path
            self.play_folder         = self.bgv_folder
            self.play_volume         = self.bgv_volume
            self.play_fadeActionSec  = self.bgv_fadeActionSec
            self.play_file_telop     = self.bgv_file_telop
            self.play_changeSec      = self.bgv_changeSec
            self.play_stopByMouseSec = self.bgv_stopByMouseSec
            self.play_overlayTime    = self.bgv_overlayTime
            self.play_overlayDate    = self.bgv_overlayDate

        self.runMode         = runMode
        if (screen != ''):
            self.play_screen = screen
        if (panel != ''):
            self.play_panel  = panel
        if (path != ''):
            self.play_path   = path
        if (folder != ''):
            self.play_folder = folder
        if (volume != ''):
            self.play_volume = int(volume)

        if (runMode == 'bgmusic'):
            self.play_stopByMouseSec = 0

        if (runMode == 'bgmdrive'):
            self.play_stopByMouseSec = 30

        return True



if __name__ == '__main__':

    conf = _conf()

    # conf 初期化
    runMode   = 'debug'
    conf.init(qLog_fn='', runMode=runMode, )

    # テスト
    print(conf.runMode)


