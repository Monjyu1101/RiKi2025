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

# dummy import
if (os.name == 'nt'):
    import comtypes.client
    import comtypes.stream

# パス設定
qPath_base = os.path.dirname(sys.argv[0]) + '/'
if (qPath_base == '/'):
    qPath_base = os.getcwd() + '/'
else:
    os.chdir(qPath_base)

# インターフェース
qCtrl_control_telop = 'temp/control_halloTelop.txt'
qCtrl_control_self  = qCtrl_control_telop

qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_work   = 'temp/_work/'
qPath_d_telop= 'temp/d6_7telop_txt/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

import   _v6__qFFmpeg
qFFmpeg= _v6__qFFmpeg.qFFmpeg_class()
qFFplay= _v6__qFFmpeg.qFFplay_class()

# 処理ルーチン
import      RiKi_halloTelop24_conf
conf      = RiKi_halloTelop24_conf._conf()
import      RiKi_halloTelop24_proc
proc      = RiKi_halloTelop24_proc._proc()
import      RiKi_halloTelop24_telop2mov
telop2mov = RiKi_halloTelop24_telop2mov._telop2mov()

# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



#runMode   = 'debug'
runMode   = 'personal'
p_screen  = 'auto'
p_panel   = 'auto'



if __name__ == '__main__':
    main_name = 'telop'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # ライセンス設定
    limit_date     = '2026/12/31'
    dt = datetime.datetime.now()
    dateinfo_today = dt.strftime('%Y/%m/%d')
    dt = datetime.datetime.strptime(limit_date, '%Y/%m/%d') + datetime.timedelta(days=-365)
    dateinfo_start = dt.strftime('%Y/%m/%d')
    main_start = time.time()

    # ディレクトリ作成(基本用)
    qFunc.makeDirs(qPath_temp,   remove=False, )
    qFunc.makeDirs(qPath_log,    remove=False, )
    qFunc.makeDirs(qPath_work,   remove=False, )
    qFunc.makeDirs(qPath_d_telop,remove=False, )

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
            runMode   = str(sys.argv[1]).lower()
        if (len(sys.argv) >= 3):
            p_screen  = str(sys.argv[2])
        if (len(sys.argv) >= 4):
            p_panel   = str(sys.argv[3])

        qLog.log('info', main_id, 'runMode = ' + str(runMode   ))
        qLog.log('info', main_id, 'screen  = ' + str(p_screen  ))
        qLog.log('info', main_id, 'panel   = ' + str(p_panel   ))



    # 初期設定
    if (True):

         # ライセンス制限
        if (dateinfo_today >= dateinfo_start):
            qLog.log('warning', main_id, '利用ライセンスは、 ' + limit_date + ' まで有効です。')
        if (dateinfo_today > limit_date):
            time.sleep(60)
            sys.exit(0)

        # conf 初期化
        conf.init(qLog_fn=qLog_fn, runMode=runMode, 
                screen=p_screen, panel=p_panel,
                )
        
        # コントロールリセット
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_') or (txt == '_stop_'):
                qFunc.remove(qCtrl_control_self)

        # 実行優先設定
        nice = conf.run_priority
        if (nice == 'auto'):
            nice = 'below'
        qFunc.setNice(nice, )

        # proc 初期化
        proc.init(qLog_fn=qLog_fn, runMode=runMode, conf=conf, )

        # 画面構成初期化
        change_screen = qGUI.checkUpdateScreenInfo(update=True, )
        while (change_screen == True):
            time.sleep(5.00)
            change_screen = qGUI.checkUpdateScreenInfo(update=True, )
        dev_lastCheck = time.time()
        dev_setting   = True



    # 起動
    if (True):
        qLog.log('info', main_id, 'start')

        # telop2mov 開始
        name = 't2movie'
        id   = '0'
        telop2mov.init(qLog_fn=qLog_fn, runMode=runMode, conf=conf, name=name, id=id, )
        telop2mov.begin()

        main_start = time.time()
        onece      = True

        last_play = time.time()
        (x, y) = qGUI.position()
        last_mouse_x = x
        last_mouse_y = y

    # 待機ループ
    break_flag = False
    while (break_flag == False):

        try:
            now_dt   = datetime.datetime.now()
            now_HHMM = now_dt.strftime('%H%M')

            # -----------------------
            # 終了確認
            # -----------------------
            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                if (txt == '_end_'):
                    break_flag = True
                    break

            # -----------------------
            # 処理
            # -----------------------

            # 再生はマウス操作により強制終了
            if (conf.mouse_check != 'no') and (conf.mouse_check != 'off'):
                (x, y) = qGUI.position()
                if (qFFplay.is_alive() == True):
                    if (abs(last_mouse_x-x) >= 50) or (abs(last_mouse_y-y) >= 50):

                        # 再生終了
                        qFFplay.abort()

                        last_play = time.time() + 60
                        qLog.log('info', main_id, '☆マウス操作により６０秒テロップ表示を停止しました。')
                last_mouse_x = x
                last_mouse_y = y

            # 起動通知
            if (onece == True):
                onece = False
                telop2mov.put(['[telop_txts]', ['【通知】', 'テロップ表示機能が起動しました。']])

            # 最終再生から5秒経過したら、次のテロップ要求
            if (qFFplay.is_alive() == False):
                if ((time.time() - last_play) >= 5):
                    telop2mov.put(['_next_', ''])
                    last_play = time.time() - 4

            # 処理
            res_data  = telop2mov.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name != ''):

                # テロップ再生
                if (res_name == '_telop_file_'):
                    qLog.log('info', main_id, '　　　' + res_value + '　->　Telop', )
                    filename = res_value
                    filename = filename.replace('/','\\')

                    # 再生中は5秒待機して強制終了
                    if (qFFplay.is_alive() == True):

                        delaySec = 5
                        qFFplay.delayAbort(delaySec=delaySec, )

                        check_time = time.time()
                        while (qFFplay.is_alive() == True) and ((time.time() - check_time) < delaySec):
                            time.sleep(0.50)

                    # 画面構成変更？
                    if (dev_setting == True) or ((time.time()-dev_lastCheck) > 5):

                        dev_change    = False
                        change_screen = qGUI.checkUpdateScreenInfo(update=True, )
                        while (change_screen == True):
                            dev_change   = True
                            time.sleep(5.00)
                            change_screen = qGUI.checkUpdateScreenInfo(update=True, )
                        dev_lastCheck = time.time()

                        if (dev_setting == True) or (dev_change == True):
                            dev_setting = False

                            qLog.log('info', main_id, 'Screen (re) Setting... ')

                            screen = qGUI.getCornerScreen(rightLeft='left', topBottom='top', checkPrimary=False, )
                            if (str(conf.gui_screen) != 'auto'):
                                try:
                                    screen = int(conf.gui_screen)
                                except:
                                    pass
                            panel  = conf.gui_panel

                    # テロップ再生
                    title     = 'Telop'
                    play_file = res_value
                    #limitSec  = 500 #最大５分
                    limitSec  = 0
                    qFFplay.begin(delaySec=0, fadeSec=0, screen=screen, panel=panel,
                                  title=title, play_file=play_file, vol=0, fps=30, order='top',
                                  overlayTime='', overlayDate='', startSec=0, limitSec=limitSec, )

                    # 最前面面
                    time.sleep(1.00)
                    qGUI.setForegroundWindow(winTitle=title, )

                    last_play = time.time()

                #else:
                #    print(res_name, res_value, )

            # -----------------------
            # メインビート
            # -----------------------
            if (qFFplay.is_alive() == True):
                time.sleep(0.25)
            else:
                time.sleep(0.50)

        except Exception as e:
            print(e)
            time.sleep(5.00)



    # 終了処理
    if (True):
        qLog.log('info', main_id, 'terminate')

        telop2mov.abort()
        del telop2mov

        # 終了
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


