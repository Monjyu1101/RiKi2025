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

import numpy as np
import cv2

import random

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
qCtrl_control_imhere = 'temp/control_ImHere.txt'
qCtrl_control_self   = qCtrl_control_imhere

qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_work   = 'temp/_work/'
qPath_rec    = 'temp/_recorder/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

import   _v6__qFFmpeg
qFFmpeg= _v6__qFFmpeg.qFFmpeg_class()

# 処理ルーチン
import      RiKi_ImHere24_conf
conf      = RiKi_ImHere24_conf._conf()
import      RiKi_ImHere24_gui
gui       = RiKi_ImHere24_gui._gui()
import      RiKi_ImHere24_proc
proc      = RiKi_ImHere24_proc._proc()
import      RiKi_ImHere24_player
player    = RiKi_ImHere24_player._player()
import      RiKi_ImHere24_camera
#camera   = RiKi_ImHere24_camera._camera()

# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



#runMode   = 'debug'
#runMode   = 'reception'
runMode   = 'personal'
#runMode   = 'camera'

p_screen  = 'auto'
p_panel   = 'auto'
p_camScan = ''



if __name__ == '__main__':
    main_name = 'imhere'
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
    qFunc.makeDirs(qPath_rec,    remove=15, )

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
        if (len(sys.argv) >= 5):
            p_camScan = str(sys.argv[4])

        qLog.log('info', main_id, 'runMode = ' + str(runMode   ))
        qLog.log('info', main_id, 'screen  = ' + str(p_screen))
        qLog.log('info', main_id, 'panel   = ' + str(p_panel ))
        qLog.log('info', main_id, 'camScan = ' + str(p_camScan ))



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
                gui_screen=p_screen, gui_panel=p_panel,
                camScan=p_camScan, 
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

        # タイトル、icon
        titlex = os.path.basename(__file__)
        titlex = titlex.replace('.py','')
        if (dateinfo_today >= dateinfo_start):
            title  = titlex + ' [ ' + runMode + ' ] (License=' + limit_date + ')'
        else:
            title  = titlex + ' [ ' + runMode + ' ]'
        #icon  = None
        icon   = './_icons/' + titlex + '.ico'

        # proc 初期化
        proc.init(qLog_fn=qLog_fn, runMode=runMode, conf=conf, )

        # player 初期化
        player.init(qLog_fn=qLog_fn, runMode=runMode, conf=conf, )

        # 画面構成初期化
        change_dev    = qFFmpeg.checkUpdateDevInfo(update=True, )
        change_screen = qGUI.checkUpdateScreenInfo(update=True, )
        while (change_dev == True) or (change_screen == True):
            time.sleep(5.00)
            change_dev    = qFFmpeg.checkUpdateDevInfo(update=True, )
            change_screen = qGUI.checkUpdateScreenInfo(update=True, )
        dev_lastCheck = time.time()
        dev_setting   = True



    # 起動
    if (True):
        qLog.log('info', main_id, 'start')

        ImHere          = True
        last_ImHere     = time.time() - float(conf.ImHere_validSec)

        cam_class       = {}
        last_img        = {}
        last_time       = {}
    
        last_action_mouse = time.time()
        (last_x, last_y)  = qGUI.position()
        last_key_time     = proc.last_key_time
        last_action_key   = time.time()

        last_sound_play   = time.time() - 60

        # ファイル連携
        filename = conf.feedback_fileYes
        if (filename != ''):
            if (qFunc.statusCheck(filename) == True):
                qFunc.statusSet(filename, False)
        filename = conf.feedback_fileNo
        if (filename != ''):
            if (qFunc.statusCheck(filename) == True):
                qFunc.statusSet(filename, False)



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
            # 変化確認
            # -----------------------
            new_ImHere = ImHere
            ImHere_hit = ''
            if (ImHere == True) and ((time.time() - last_ImHere) > float(conf.ImHere_validSec)):
                new_ImHere = False

            # -----------------------
            # マウス確認
            # -----------------------
            if (conf.mouse_check != 'no') and (conf.mouse_check != 'off'):
                (x, y) = qGUI.position()
                if (abs(last_x-x) >= 50) or (abs(last_y-y) >= 50):
                    if (new_ImHere == False) and (ImHere_hit == ''):
                        ImHere_hit = 'mouse'
                        qLog.log('debug', main_id, 'ImHere! (mouse)')
                    else:
                        ImHere_hit = 'mouse'
                last_x = x
                last_y = y

            # -----------------------
            # キーボード確認
            # -----------------------
            if (conf.keyboard_check != 'no') and (conf.keyboard_check != 'off'):
                if (proc.last_key_time != last_key_time):
                    if (new_ImHere == False) and (ImHere_hit == ''):
                        ImHere_hit = 'keyboard'
                        qLog.log('debug', main_id, 'ImHere! (keyboaed)')
                    else:
                        ImHere_hit = 'keyboard'
                last_key_time = proc.last_key_time

            # -----------------------
            # アクション
            # -----------------------
            if (ImHere_hit == ''):

                # ６０秒経過でマウスアクション
                if (conf.action60s_mouse != 'no') and (conf.action60s_mouse != 'off'):

                    if ((time.time() - last_ImHere) > 60):
                        if ((time.time() - last_action_mouse) > 15):
                            last_action_mouse = time.time()

                            l,t,w,h = qGUI.getScreenPosSize(screen=0, )
                            (x, y)  = qGUI.position()

                            # マウス移動
                            x += int(random.random() * 10) - 5
                            if (x < (l + 100)):
                                x = (l + 100)
                            if (x > (l+w-100)):
                                x = (l+w-100)
                            y += int(random.random() * 10) - 5
                            if (y < (t + 100)):
                                y = (t + 100)
                            if (y > (t+h-100)):
                                y = (t+h-100)
                            qGUI.moveTo(int(x), int(y))
        
                            qLog.log('info', main_id, 'Idol Mouse Action, Position = (' + str(last_x) + ', ' + str(last_y) + ')', )
                            (last_x, last_y) = qGUI.position()

                # ６０秒経過でキーアクション
                if (conf.action60s_key != ''):

                    if ((time.time() - last_ImHere) > 60):
                        if ((time.time() - last_action_key) > 60):
                            last_action_key = time.time()

                            # ctrlキー
                            qLog.log('info', main_id, 'Idol Key Action,   Press = "' + conf.action60s_key + '"', )
                            try:
                                qGUI.press(conf.action60s_key)
                                last_key_time = proc.last_key_time
                            except Exception as e:
                                pass

            # -----------------------
            # カメラ起動
            # -----------------------
            if  (conf.cam_check == 'yes') \
            or ((conf.cam_check == 'auto') and (new_ImHere == False) and (ImHere_hit == '')):

                # カメラ設定
                dev_change    = False

                # デバイス構成変更？
                if ((time.time()-dev_lastCheck) > float(conf.dev_intervalSec)):

                    change_dev    = qFFmpeg.checkUpdateDevInfo(update=True, )
                    change_screen = qGUI.checkUpdateScreenInfo(update=True, )
                    while (change_dev == True) or (change_screen == True):
                        dev_change   = True
                        time.sleep(5.00)
                        change_dev    = qFFmpeg.checkUpdateDevInfo(update=True, )
                        change_screen = qGUI.checkUpdateScreenInfo(update=True, )
                    dev_lastCheck = time.time()

                # カメラ終了
                if (dev_setting == True) or (dev_change == True):
                    dev_setting = False

                    if (runMode != 'reception'):
                        qLog.log('warning', main_id, 'Camera (re) Setting... ')
                    #print(cam_list)

                    # スレッド終了
                    if (len(cam_class) > 0):
                        qLog.log('info', main_id, 'Camera check end. (reset)')
                        ids = list(cam_class.keys())
                        for id in ids:
                            if (cam_class[id] is not None):
                                waitMax = 5
                                cam_class[id].abort(waitMax=waitMax, )
                                time.sleep(waitMax)
                                del cam_class[id]
                                cam_class[id] = None
                        cam_class = {}
                        last_img  = {}
                        last_time = {}

                    # ガイド消去
                    if (gui.window is not None):
                        qLog.log('info', main_id, 'Guide display end. (reset)')
                        gui.close()
                        gui.terminate()

                # カメラ開始
                if (len(cam_class) == 0):

                    # 時間帯確認
                    if  (runMode == 'personal') \
                    or  ( \
                            ((now_HHMM >= conf.cam_start) and (now_HHMM <= conf.cam_end)) \
                        and (not ((now_HHMM >= conf.silent_start) and (now_HHMM <= conf.silent_end))) \
                        and (not ((now_HHMM >= conf.lunch_start ) and (now_HHMM <= conf.lunch_end ))) \
                        ):

                        # カメラ変更
                        cam_list = qFFmpeg.dev_cam
                        cam_count = len(cam_list)

                        # カメラ指定
                        st, en = None, None
                        if   (conf.cv2_camScan == 'all'):
                            if (cam_count != 0):
                                st, en = 0, cam_count
                            else:
                                st, en = 0, 1
                        elif (conf.cv2_camScan == 'min'):
                                st, en = 0, 1
                        elif (conf.cv2_camScan == 'max'):
                            if (cam_count != 0):
                                st, en = cam_count-1, cam_count
                            else:
                                st, en = 0, 1
                        elif (str(conf.cv2_camScan).isdigit()):
                                st, en = int(conf.cv2_camScan), int(conf.cv2_camScan)+1

                        qLog.log('debug', main_id, F"Camera check range. ({ st }, { en })")

                        # スレッド起動
                        if (st is not None) and (en is not None):
                            for c in range(st, en):
                                id = str(c)
                                qLog.log('info', main_id, F"Camera check start. ({ id })")
                                cam_class[id] = RiKi_ImHere24_camera._camera()
                                cam_class[id].init(qLog_fn=qLog_fn, runMode=runMode, conf=conf,
                                                    name='camera', id=id, camDev=str(c), 
                                                    cv2_engine=conf.cv2_engine, cv2_intervalSec=float(conf.cv2_intervalSec),
                                                    cv2_sabunLimit=float(conf.cv2_sabunLimit), cv2_sometime=conf.cv2_sometime, )
                                last_img[id]  = None
                                last_time[id] = time.time()
                                cam_class[id].begin()
                                time.sleep(3.00)
                        else:
                                c  = 0
                                id = str(c)
                                qLog.log('info', main_id, F"Camera check start. ({ id })")
                                cam_class[id] = RiKi_ImHere24_camera._camera()
                                cam_class[id].init(qLog_fn=qLog_fn, runMode=runMode, conf=conf,
                                                    name='camera', id=id, camDev=str(conf.cv2_camScan),
                                                    cv2_engine=conf.cv2_engine, cv2_intervalSec=float(conf.cv2_intervalSec),
                                                    cv2_sabunLimit=float(conf.cv2_sabunLimit), cv2_sometime=conf.cv2_sometime, )
                                last_img[id]  = None
                                last_time[id] = time.time()
                                cam_class[id].begin()
                                time.sleep(3.00)

                # ガイド表示
                if (conf.cam_guide == 'yes') and (len(cam_class) > 0):
                    if (gui.window is None):
                        qLog.log('info', main_id, 'Guide display start. (reset)')
                        title = os.path.basename(__file__)
                        title = title.replace('.py','')
                        icon  = None
                        gui.init(qLog_fn=qLog_fn, runMode=runMode,
                                screen=conf.gui_screen, panel=conf.gui_panel,
                                title=title, theme=conf.gui_theme,
                                keep_on_top=conf.gui_keep_on_top, alpha_channel=conf.gui_alpha,
                                icon=icon, )
                        gui.reset()
                        gui.resize(reset=True, )
                        gui.autoFadeControl(reset=True, )

            # -----------------------
            # 画像取得
            # -----------------------
            if (len(cam_class) > 0):

                # 画像取得
                ids = list(cam_class.keys())
                for id in ids:
                    if (cam_class[id] is not None):
                        while (cam_class[id].proc_r.qsize() > 0):
                            res_data  = cam_class[id].get()
                            res_name  = res_data[0]
                            res_value = res_data[1]
                            if   (res_name == ''):
                                break

                            elif (res_name == '[img]'):
                                last_img[id]  = res_value.copy()
                                last_time[id] = time.time()

                            elif (res_name == '[person_raw]') or (res_name == '[person_img]'):
                                last_img[id]  = res_value.copy()
                                last_time[id] = time.time()
                                if (res_name == '[person_raw]'):
                                    if (new_ImHere == False) and (ImHere_hit == ''):
                                        ImHere_hit = 'person'
                                        qLog.log('debug', main_id, 'ImHere! (person:' + str(c) + ')')
                                    if  (runMode != 'personal'):
                                        proc.save_photo(res_value.copy(), hit_name='person', )

                            elif (res_name == '[face_raw]') or (res_name == '[face_img]'):
                                last_img[id]  = res_value.copy()
                                last_time[id] = time.time()
                                if (res_name == '[face_raw]'):
                                    if (new_ImHere == False) and (ImHere_hit == ''):
                                        ImHere_hit = 'face'
                                        qLog.log('debug', main_id, 'ImHere! (face:' + str(c) + ')')
                                    if  (runMode != 'personal'):
                                        proc.save_photo(res_value.copy(), hit_name='face', )

            # -----------------------
            # 画像生成
            # -----------------------
            dsp_image = None
            if (len(cam_class) > 0):

                width, height = 1280, 720

                img_onece = True 
                i = 0
                ids = list(cam_class.keys())
                for id in ids:
                    if (last_img[id] is not None):
                        if ((time.time() - last_time[id]) > 60):
                            last_img[id] = None

                    if (last_img[id] is not None):

                        if   (len(cam_class) <= 1):
                            img = cv2.resize(last_img[id], (width,height))
                            dsp_image = img
                        
                        elif (len(cam_class) == 2):
                            if (img_onece == True):
                                img_onece = False
                                dsp_image = np.zeros((height,width,3), np.uint8)

                            i += 1
                            if   ((i % 2) == 1):
                                w,h = 0,0
                            else:
                                w,h = 0,int(height/2)
                            img = cv2.resize(last_img[id], (width,int(height/2)))
                            dsp_image[h:h+int(height/2),w:w+width] = img

                        else:
                            if (img_onece == True):
                                img_onece = False
                                dsp_image = np.zeros((height,width,3), np.uint8)

                            i += 1
                            if   ((i % 4) == 1):
                                w,h = 0,0
                            elif ((i % 4) == 2):
                                w,h = int(width/2),0
                            elif ((i % 4) == 3):
                                w,h = 0,int(height/2)
                            else:
                                w,h = int(width/2),int(height/2)
                            img = cv2.resize(last_img[id], (int(width/2),int(height/2)))
                            dsp_image[h:h+int(height/2),w:w+int(width/2)] = img

            # -----------------------
            # ガイド表示
            # -----------------------
            if (dsp_image is not None):
                if (conf.cam_guide == 'yes') \
                or ((conf.cam_guide == 'auto') and (ImHere == False)):

                    # ガイド表示
                    if (gui.window is None):
                        qLog.log('info', main_id, 'Guide display start. (new image)')
                        title = os.path.basename(__file__)
                        title = title.replace('.py','')
                        icon  = None
                        gui.init(qLog_fn=qLog_fn, runMode=runMode,
                                screen=conf.gui_screen, panel=conf.gui_panel,
                                title=title, theme=conf.gui_theme,
                                keep_on_top=conf.gui_keep_on_top, alpha_channel=conf.gui_alpha,
                                icon=icon, )
                        gui.reset()
                        gui.resize(reset=True, )
                        gui.autoFadeControl(reset=True, )

                    # 画像更新
                    gui.setImage(image=dsp_image, )

            # ガイド表示
            if (gui.window is not None):

                    # GUI リサイズ
                    gui.resize(reset=False, )

                    # GUI 自動フェード
                    gui.autoFadeControl(reset=False, )

                    # イベントの読み込み                ↓　timeout値でtime.sleep代用
                    event, values = gui.read(timeout=150, )
                    # ウィンドウの×ボタンクリックで終了
                    if event == "WIN_CLOSED":
                        #break_flag = True
                        #break
                        pass

                    if event in (None, '-exit-'):
                        #break_flag = True
                        #break
                        pass

                    if (event == '-idoling-'):
                        pass
                    else:
                        print(event, values, )        

            # -----------------------
            # ImHere ?
            # -----------------------
            if (new_ImHere == False) and (ImHere_hit != ''):

                # フィードバックアクション
                if (ImHere_hit != 'mouse'):

                    if (conf.feedback_mouse != 'no') and (conf.feedback_mouse != 'off'):
                        (last_x, last_y) = qGUI.position()
                        l,t,w,h = qGUI.getScreenPosSize(screen=0, )

                        x, y  = last_x, last_y
                        while not((abs(last_x-x) >= 60) or (abs(last_y-y) >= 60)):
                            # マウス移動
                            x += int(random.random() * 60) - 30
                            if (x < (l + 100)):
                                x = (l + 100)
                            if (x > (l+w-100)):
                                x = (l+w-100)
                            y += int(random.random() * 60) - 30
                            if (y < (t+100)):
                                y = (t+100)
                            if (y > (t+h-100)):
                                y = (t+h-100)
                            #qGUI.moveTo(int(x),int(y))

                        qGUI.moveTo(int(x),int(y))
                        (last_x, last_y) = qGUI.position()
                        qLog.log('info', main_id, 'Feedback Mouse Action, Position = (' + str(last_x) + ', ' + str(last_y) + ')', )

                # サウンドフィードバック
                if (ImHere_hit != 'mouse'):
    
                    if ((time.time() - last_sound_play) > 60):

                        if  (conf.reception_sound1_file != '') \
                        and (now_HHMM >= conf.reception_sound1_sttm) \
                        and (now_HHMM <  conf.reception_sound1_entm):
                            qLog.log('info', main_id, 'Feedback Sound = ' + conf.reception_sound1_file, )
                            qFunc.guideSound(filename=conf.reception_sound1_file, sync=False, )
                            last_sound_play = time.time()

                        if  (conf.reception_sound2_file != '') \
                        and (now_HHMM >= conf.reception_sound2_sttm) \
                        and (now_HHMM <  conf.reception_sound2_entm):
                            qLog.log('info', main_id, 'Feedback Sound = ' + conf.reception_sound2_file, )
                            qFunc.guideSound(filename=conf.reception_sound2_file, sync=False, )
                            last_sound_play = time.time()

                        if  (conf.reception_sound3_file != '') \
                        and (now_HHMM >= conf.reception_sound3_sttm) \
                        and (now_HHMM <  conf.reception_sound3_entm):
                            qLog.log('info', main_id, 'Feedback Sound = ' + conf.reception_sound3_file, )
                            qFunc.guideSound(filename=conf.reception_sound3_file, sync=False, )
                            last_sound_play = time.time()

                        if  (conf.reception_sound4_file != '') \
                        and (now_HHMM >= conf.reception_sound4_sttm) \
                        and (now_HHMM <  conf.reception_sound4_entm):
                            qLog.log('info', main_id, 'Feedback Sound = ' + conf.reception_sound4_file, )
                            qFunc.guideSound(filename=conf.reception_sound4_file, sync=False, )
                            last_sound_play = time.time()

            if (ImHere_hit == ''):
                if (ImHere == True) and (new_ImHere == False):
                    qLog.log('debug', main_id, 'Where, Me ?')
                ImHere = new_ImHere
            else:
                ImHere = True
                last_ImHere = time.time()
                ## Debug! 30秒
                #last_ImHere = time.time() - float(conf.ImHere_validSec) + 30

            # -----------------------
            # 時間外？
            # -----------------------
            if  (runMode != 'personal') \
            and  ( \
                    ((now_HHMM < conf.cam_start) or (now_HHMM > conf.cam_end)) \
                or  ((now_HHMM >= conf.silent_start) and (now_HHMM <= conf.silent_end)) \
                or  ((now_HHMM >= conf.lunch_start ) and (now_HHMM <= conf.lunch_end )) \
                ):

                # スレッド終了
                if (len(cam_class) > 0):
                    qLog.log('info', main_id, 'Camera check end. (Time)')
                    ids = list(cam_class.keys())
                    for id in ids:
                        if (cam_class[id] is not None):
                            waitMax = 5
                            cam_class[id].abort(waitMax=waitMax, )
                            time.sleep(waitMax)
                            del cam_class[id]
                            cam_class[id] = None
                    cam_class = {}
                    last_img  = {}
                    last_time = {}

                # ガイド消去
                if (gui.window is not None):
                    qLog.log('info', main_id, 'Guide display end. (Time)')
                    gui.close()
                    gui.terminate()

            # -----------------------
            # ImHere = Yes!
            # -----------------------
            if (ImHere == True):

                # ファイル連携
                filename = conf.feedback_fileYes
                if (filename != ''):
                    if (qFunc.statusCheck(filename) == False):
                        qFunc.statusSet(filename, True)
                filename = conf.feedback_fileNo
                if (filename != ''):
                    if (qFunc.statusCheck(filename) == True):
                        qFunc.statusSet(filename, False)

                # スレッド終了
                if (conf.cam_check == 'auto'):
                    if (len(cam_class) > 0):
                        qLog.log('info', main_id, 'Camera check end. (ImHere!)')
                        ids = list(cam_class.keys())
                        for id in ids:
                            if (cam_class[id] is not None):
                                waitMax = 5
                                cam_class[id].abort(waitMax=waitMax, )
                                time.sleep(waitMax)
                                del cam_class[id]
                                cam_class[id] = None
                        cam_class = {}
                        last_img  = {}
                        last_time = {}

                # ガイド消去
                if (conf.cam_guide == 'auto'):
                    if (gui.window is not None):
                        qLog.log('info', main_id, 'Guide display end. (ImHere!)')
                        gui.close()
                        gui.terminate()

            # -----------------------
            # ImHere = No!
            # -----------------------
            if (ImHere == False):

                # ファイル連携
                filename = conf.feedback_fileYes
                if (filename != ''):
                    if (qFunc.statusCheck(filename) == True):
                        qFunc.statusSet(filename, False)
                filename = conf.feedback_fileNo
                if (filename != ''):
                    if (qFunc.statusCheck(filename) == False):
                        qFunc.statusSet(filename, True)

            # -----------------------
            # メインビート
            # -----------------------
            if  (runMode == 'personal'):
                    time.sleep(0.50)
            else:
                if (ImHere == True):
                    time.sleep(0.50)
                else:
                    time.sleep(0.05)

        except Exception as e:
            print(e)
            time.sleep(5.00)



    # 終了処理
    if (True):
        qLog.log('info', main_id, 'terminate')

        # スレッド終了
        if (len(cam_class) > 0):
            ids = list(cam_class.keys())
            for id in ids:
                if (cam_class[id] is not None):
                    waitMax = 5
                    cam_class[id].abort(waitMax=waitMax, )
                    time.sleep(waitMax)
                    del cam_class[id]
                    cam_class[id] = None
            cam_class = {}
            last_img  = {}
            last_time = {}

        # ガイド消去
        gui.close()
        gui.terminate()

        # 終了
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


