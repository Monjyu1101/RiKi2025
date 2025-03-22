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

import psutil
import random

import numpy as np
import cv2

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
qCtrl_control_video = 'temp/control_showMeVideo.txt'
qCtrl_control_self  = qCtrl_control_video

qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_work   = 'temp/_work/'

# 共通ルーチン
import    _v6__qFunc
qFunc   = _v6__qFunc.qFunc_class()
import    _v6__qGUI
qGUI    = _v6__qGUI.qGUI_class()
import    _v6__qLog
qLog    = _v6__qLog.qLog_class()

import   _v6__qFFmpeg
qFFmpeg= _v6__qFFmpeg.qFFmpeg_class()
qCV2   = _v6__qFFmpeg.qCV2_class()

# 処理ルーチン
import      RiKi_showMeVideo24_conf
conf      = RiKi_showMeVideo24_conf._conf()
import      RiKi_showMeVideo24_proc
proc      = RiKi_showMeVideo24_proc._proc()
import      RiKi_showMeVideo24_gui
gui       = RiKi_showMeVideo24_gui._gui()

# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



#runMode   = 'debug'
#runMode = 'bgmusic'
runMode = 'bgmdrive'
#runMode = 'bgvideo'
#runMode = 'bgm'
#runMode = 'bgv'

p_screen = ''
p_panel  = ''
p_path   = ''
#p_path   = 'C:/_共有/'
p_folder = ''
#p_folder = 'BGV/'
p_volume = ''



if __name__ == '__main__':
    main_name = 'player0'
    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
        if (runMode == 'bgm') or (runMode == 'bgmusic') \
        or (runMode == 'bgmdrive') \
        or (runMode == 'bgv') or (runMode == 'bgvideo'):
            main_name = runMode + '0'
    if (len(sys.argv) >= 3):
        if (str(sys.argv[2]).isdigit()):
            main_name = main_name[:-1] + str(sys.argv[2])
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
            runMode  = str(sys.argv[1]).lower()
        if (len(sys.argv) >= 3):
            p_screen = str(sys.argv[2])
        if (len(sys.argv) >= 4):
            p_panel  = str(sys.argv[3])
        if (len(sys.argv) >= 5):
            p_path   = str(sys.argv[4])
        if (len(sys.argv) >= 6):
            p_folder = str(sys.argv[5])
        if (len(sys.argv) >= 7):
            p_volume = str(sys.argv[6])

        qLog.log('info', main_id, 'runMode = ' + str(runMode ))
        qLog.log('info', main_id, 'screen  = ' + str(p_screen))
        qLog.log('info', main_id, 'panel   = ' + str(p_panel ))
        qLog.log('info', main_id, 'path    = ' + str(p_path  ))
        qLog.log('info', main_id, 'folder  = ' + str(p_folder))
        qLog.log('info', main_id, 'volume  = ' + str(p_volume))



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
                path=p_path, folder=p_folder,
                volume=p_volume, 
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

        # 再生リスト
        path = conf.play_path + conf.play_folder
        play_files = []
        if   (os.path.isfile(path)):
            play_files.append(path)
        elif (os.path.isdir(path)):
            play_files = glob.glob(path + '/*.*')
            if (conf.shuffle_play == 'yes'):
                random.shuffle(play_files)
        qLog.log('info', main_id, f"loading ... (play_files={ len(play_files) })")

        # CPU 使用率
        cpu_max  = 40
        cpu_data = []
        for x in range(cpu_max):
            cpu_data.append(float(0))



    # 起動
    if (True):
        qLog.log('info', main_id, 'start')

        setting         = True
        last_setting    = time.time() 

        file_index      = 0

        name = 'play0'
        if ((conf.play_screen).isdigit()):
            name = name[:-1] + str(conf.play_screen)

        thread_max      = 5
        thread_pool     = {}
        thread_start    = {}
        thread_limitSec = {}

        old_thread2 = 0
        old_thread  = 1
        last_thread = 2
        next_thread = 3
        for t in range(0, thread_max):
            thread_pool[t]       = _v6__qFFmpeg.qFFplay_class()
            thread_start[t]      = time.time()
            thread_limitSec[t]   = 0

        # スクリーン
        screen = 0
        try:
            screen = int(conf.play_screen)
            if (screen > (qGUI.screen_count-1)):
                qLog.log('error', main_id, f"screen={ screen } is error. ")
                screen = None
        except:
            pass
        if (str(conf.play_screen) == 'auto'):
            if   (runMode == 'bgm') or (runMode == 'bgmusic') \
            or   (runMode == 'bgmdrive'):
                screen = qGUI.getCornerScreen(rightLeft='right', topBottom='bottom', checkPrimary=False, )
            elif (runMode == 'bgv') or (runMode == 'bgvideo'):
                pass
            else:
                pass

        # マウス位置
        if ((runMode == 'bgmusic') or (runMode == 'bgmdrive') or (runMode == 'bgvideo')) and (screen is not None):
            (x, y), s = qGUI.screenPosition(screen=screen)
        else:
            (x, y) = qGUI.position()
        last_mouse_x    = x
        last_mouse_y    = y
        last_mouse_time = time.time() - conf.play_stopByMouseSec #即開始を計算

        if (runMode == 'bgm') or (runMode == 'bgv'):
            if (conf.play_stopByMouseSec != 0):
                last_mouse_time = time.time() - conf.play_stopByMouseSec + 60 #残り60秒を計算
                qLog.log('info', main_id, 'mouse move check, play waiting 60sec. ')



    # 待機ループ
    break_flag = False
    while (break_flag == False):

        if True:
        #try:
            about_play = False
            new_play   = False

            # -------------
            # CPU 使用率
            # -------------
            cpu  = psutil.cpu_percent(interval=None, percpu=False)
            del cpu_data[0]
            cpu_data.append(float(cpu))
            cpu_ave = np.mean(cpu_data)

            # -----------------------
            # 終了確認
            # -----------------------
            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                if (txt == '_end_'):
                    break_flag = True
                    qLog.log('info', main_id, f"run stop! { qCtrl_control_self }")

            if (conf.run_limitSec != 0):
                if ((time.time() - main_start) > conf.run_limitSec):
                    break_flag = True
                    qLog.log('info', main_id, f"run stop! limitSec={ conf.run_limitSec }")

            # 画面構成変更？
            if ((time.time() - dev_lastCheck) > 5):
                dev_lastCheck = time.time()
                change_screen = qGUI.checkUpdateScreenInfo(update=True, )
                if (change_screen == True):
                    break_flag = True
                    qLog.log('info', main_id, 'run stop! screenInfo changed.')

            # -------------
            # 再生終了？
            # -------------
            if (break_flag != True):
                if (thread_pool[last_thread].is_alive() == True):

                    # マウス操作による再生キャンセル
                    if (conf.play_stopByMouseSec != 0):
                        if ((runMode == 'bgmusic') or (runMode == 'bgmdrive') or (runMode == 'bgvideo')) and (screen is not None):
                            (x, y),s = qGUI.screenPosition(screen=screen)
                        else:
                            (x, y) = qGUI.position()
                        if (abs(last_mouse_x-x) < 50) and (abs(last_mouse_y-y) < 50):
                            last_mouse_x = x
                            last_mouse_y = y
                        else:
                            last_mouse_x = x
                            last_mouse_y = y
                            last_mouse_time = time.time()

                            # 再生キャンセル
                            qLog.log('info', main_id, f"Play Stop! By Mouse Move. (screen={ screen }) Waiting sec = { conf.play_stopByMouseSec }s. ")
                            about_play = True

                    #再生可以外の時間帯は再生キャンセル
                    if (runMode == 'bgm') or (runMode == 'bgv'):
                        if (about_play == False):
                            nowTime = datetime.datetime.now()
                            HHMMSS  = nowTime.strftime('%H:%M:%S')
                            YOUBI   = nowTime.strftime('%a').lower()

                        # 曜日チェック
                        if (about_play == False):
                            if (conf.day_control == 'week'):
                                if (YOUBI not in ['mon','tue','wed','thu','fri']):
                                    qLog.log('info', main_id, 'Play Stop! By day check. (day_control=' + conf.day_control + ')' )
                                    about_play = True
                            elif (conf.day_control != 'yes') and (conf.day_control != 'no'):
                                if (YOUBI != conf.day_control):
                                    qLog.log('info', main_id, 'Play Stop! By day check. (day_control=' + conf.day_control + ')' )
                                    about_play = True

                        # 時間チェック
                        if (about_play == False):
                            if (conf.day_control != 'no'):
                                if (HHMMSS < conf.day_start) or (HHMMSS > conf.day_end):
                                    qLog.log('info', main_id, 'Play Stop! By time check. (' + conf.day_start + ' - ' + conf.day_end + ')' )
                                    about_play = True

                        # サイレントチェック
                        if (about_play == False):
                            if (conf.silent_control != 'no'):
                                if (HHMMSS >= conf.silent_start) and (HHMMSS <= conf.silent_end):
                                    qLog.log('info', main_id, 'Play Stop! By silent check. (' + conf.silent_start + ' - ' + conf.silent_end + ')' )
                                    about_play = True

                        # ランチチェック
                        if (about_play == False):
                            if (conf.lunch_control != 'no'):
                                if (HHMMSS >= conf.lunch_start) and (HHMMSS <= conf.lunch_end):
                                    qLog.log('info', main_id, 'Play Stop! By lunch check. (' + conf.lunch_start + ' - ' + conf.lunch_end + ')' )
                                    about_play = True

                        # # 連続再生制限(2時間)
                        # if ((time.time() - main_start) > 3600*2):
                        #    qLog.log('info', main_id, 'Play Stop! By running time check. ( 2h )' )
                        #    about_play = True

                    # 再生終了
                    if  (about_play == True):

                        # フェード停止 1
                        if (conf.play_fadeActionSec != 0):
                            fadeSec = conf.play_fadeActionSec
                            thread_pool[last_thread].delayAbort(delaySec=fadeSec, )

                            # フェード処理(out)
                            outSec = fadeSec / 4
                            qLog.log('info', main_id, f"Cancel fadeOut ( { outSec :.1f}s )" )
                            gui.fadeOut(screen=screen, panel=panel, mask='white', outSec=outSec, )

                        # 再生停止
                        fadeSec = conf.play_fadeActionSec
                        #waitMax = fadeSec / 4
                        waitMax = 5
                        thread_pool[last_thread].abort(waitMax=waitMax, )

                        # フェード停止 2
                        if (conf.play_fadeActionSec != 0):
                            fadeSec = conf.play_fadeActionSec

                            # フェード処理(in)
                            inSec = fadeSec / 4
                            qLog.log('info', main_id, f"Cancel fadeIn  ( { inSec :.1f}s )" )
                            gui.fadeIn(inSec=inSec, )



            # -------------
            # 再生開始判断
            # -------------
            if (break_flag != True) and (about_play != True):

                # 前の再生無し
                if (thread_pool[last_thread].is_alive() == False):
                    new_play = True

                # 前の再生の終了または play_fadeActionSec +【30】+2秒前
                if (thread_pool[last_thread].is_alive() == True) \
                and ((thread_limitSec[last_thread] - (time.time() - thread_start[last_thread])) < (conf.play_fadeActionSec + 30 + 3)):
                    # 180 - (02:37 - 00:00) < (1 + 30 + 3)
                    new_play = True

                # マウス操作？
                if (new_play == True):
                    if (conf.play_stopByMouseSec != 0):

                        if ((runMode == 'bgmusic') or (runMode == 'bgmdrive') or (runMode == 'bgvideo')) and (screen is not None):
                            (x, y),s = qGUI.screenPosition(screen=screen)
                        else:
                            (x, y) = qGUI.position()
                        if (abs(last_mouse_x-x) < 50) and (abs(last_mouse_y-y) < 50):
                            last_mouse_x = x
                            last_mouse_y = y
                        else:
                            last_mouse_x = x
                            last_mouse_y = y
                            last_mouse_time = time.time()

                            new_play = False

                # マウス操作の停止秒数による再生スキップ
                if (new_play == True):
                    if ((time.time() - last_mouse_time) < conf.play_stopByMouseSec):
                        sec = int(conf.play_stopByMouseSec - (time.time() - last_mouse_time))
                        if (sec > 1):
                            time.sleep(1.00)
                        new_play = False

                #再生可以外の時間帯は再生スキップ
                if (new_play == True):
                    if (runMode == 'bgm') or (runMode == 'bgv'):
                        nowTime = datetime.datetime.now()
                        HHMMSS  = nowTime.strftime('%H:%M:%S')
                        YOUBI   = nowTime.strftime('%a').lower()

                        # 曜日チェック
                        if (conf.day_control == 'week'):
                            if (YOUBI not in ['mon','tue','wed','thu','fri']):
                                time.sleep(1.00)
                                new_play = False
                        elif (conf.day_control != 'yes') and (conf.day_control != 'no'):
                            if (YOUBI != conf.day_control):
                                time.sleep(1.00)
                                new_play = False

                        # 時間チェック
                        if (new_play == True):
                            if (conf.day_control != 'no'):
                                if (HHMMSS < conf.day_start) or (HHMMSS > conf.day_end):
                                    time.sleep(1.00)
                                    new_play = False

                        # サイレントチェック
                        if (new_play == True):
                            if (conf.silent_control != 'no'):
                                if (HHMMSS >= conf.silent_start) and (HHMMSS <= conf.silent_end):
                                    time.sleep(1.00)
                                    new_play = False

                        # ランチチェック
                        if (new_play == True):
                            if (conf.lunch_control != 'no'):
                                if (HHMMSS >= conf.lunch_start) and (HHMMSS <= conf.lunch_end):
                                    time.sleep(1.00)
                                    new_play = False



            # -------------
            # スクリーン設定
            # -------------
            if (new_play == True):

                if (setting == True):
                    qLog.log('info', main_id, 'Screen Setting... ')

                    # スクリーン
                    screen = 0
                    try:
                        screen = int(conf.play_screen)
                        if (screen > (qGUI.screen_count-1)):
                            qLog.log('error', main_id, f"screen={ screen } is error. ")
                            break_flag = True
                            break
                    except:
                        pass
                    if (str(conf.play_screen) == 'auto'):
                        if   (runMode == 'bgm') or (runMode == 'bgmusic') \
                        or   (runMode == 'bgmdrive'):
                            screen = qGUI.getCornerScreen(rightLeft='right', topBottom='bottom', checkPrimary=False, )
                        elif (runMode == 'bgv') or (runMode == 'bgvideo'):
                            pass
                        else:
                            pass

                    # パネル
                    panel = conf.play_panel
                    if (str(conf.play_panel) == 'auto'):
                        if   (runMode == 'bgm') or (runMode == 'bgmusic') \
                        or   (runMode == 'bgmdrive'):
                            panel = '9-'
                        elif (runMode == 'bgv') or (runMode == 'bgvideo'):
                            panel = '0'
                        else:
                            panel = '5+'

                    # 初回設定終了
                    setting = False
                    last_setting = time.time()



            # -------------
            # 再生開始
            # -------------
            if (new_play == True):

                # 起点時間
                chkTime = time.time()

                # 再生終了？
                file_index += 1
                if (file_index > (len(play_files))):

                    if   (runMode != 'bgm') and (runMode != 'bgmusic') \
                    and  (runMode != 'bgmdrive') \
                    and  (runMode != 'bgv') and (runMode != 'bgvideo'):
                        qLog.log('info', main_id, 'play folder complite! ')
                        break_flag = True
                        break
                    else:
                        file_index = 1
                        if (conf.shuffle_play == 'yes'):
                            random.shuffle(play_files)

                # 再生ファイル
                f = file_index - 1
                play_file = play_files[f]
                proc_file = play_file
                #proc_file = proc_file.replace('/', '\\')

                # 静止画→動画変換
                if (play_file[-4:].lower() == '.jpg') \
                or (play_file[-4:].lower() == '.png'):
                    if (conf.img2mov_play == 'no'):
                        proc_file = ''
                    else:
                        out_file = qPath_work + main_name + '.' + '{:04}'.format(f) + '.mp4'
                        #res = qCV2.cv2img2mov(inp_file=play_file, out_file=out_file, sec=play_changeSec, fps=15, zoom=True, )
                        if (conf.img2mov_zoom == 'yes'):
                            fps = 5
                            zoom = True
                        else:
                            fps = 1
                            zoom = False
                        res = qCV2.cv2img2mov(inp_file=play_file, out_file=out_file, sec=conf.img2mov_sec, fps=fps, zoom=zoom, )
                        if (res == False):
                            proc_file = ''
                        else:
                            proc_file = res
                        
                # 再生ファイル有効？
                if (proc_file != ''):

                    # 再生時間計算
                    limitSec = conf.play_changeSec
                    startSec = 0
                    if  (proc_file[-4:].lower() != '.jpg') \
                    and (proc_file[-4:].lower() != '.png') \
                    and (proc_file[-4:].lower() != '.wav') \
                    and (proc_file[-4:].lower() != '.mp3') \
                    and (proc_file[-4:].lower() != '.m4a'):
                        try:
                            cap = cv2.VideoCapture(proc_file)                       # 動画を読み込む
                            video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)   # フレーム数を取得する
                            video_fps = cap.get(cv2.CAP_PROP_FPS)                   # フレームレートを取得する
                            video_len_sec = video_frame_count / video_fps
                            if (video_len_sec > 0):
                                if (limitSec == 0) or (video_len_sec < limitSec):
                                    limitSec = video_len_sec
                            if (conf.shuffle_play == 'yes'):
                                if (video_len_sec > limitSec):
                                    startSec = int((video_len_sec - limitSec) * random.random())
                        except:
                            pass
                    if (limitSec == 0):
                        limitSec = 3600 * 4 # 同一ファイル最大4時間まで再生

                    # 投入スレッド計算
                    old_thread2 = old_thread
                    old_thread  = last_thread
                    last_thread = next_thread
                    next_thread = (last_thread + 1) % thread_max

                    # 再生スレッド開始
                    title    = os.path.basename(play_file)
                    winTitle = str(screen) + ':' + title
                    fps = 30
                    if   (runMode == 'bgm') or (runMode == 'bgmusic') \
                    or   (runMode == 'bgmdrive'):
                        fps = 5
                    elif (runMode == 'bgv') or (runMode == 'bgvideo'):
                        if (qGUI.screen_count > 1):
                            if (screen == 0):
                                if (cpu_ave <= 50):
                                    fps = 15
                                else:
                                    fps = 10
                            else:
                                if (cpu_ave <= 50):
                                    fps = 10
                                else:
                                    fps = 0.2
                                
                    #order = 'top'
                    order = 'normal'
                    #if (runMode == 'bgm') or (runMode == 'bgmusic'):
                    #    order = 'normal'

                    # 再生 play_fadeActionSec +【30】秒待機
                    delaySec = (conf.play_fadeActionSec + 30 + 1) - (time.time() - chkTime)
                    if (delaySec < 0):
                        delaySec = 1
                    #if (play_file[-4:].lower() == '.jpg') \
                    #or (play_file[-4:].lower() == '.png'):
                    #    delaySec = 0
                    qLog.log('info', main_id, f"Play '{ play_file }' (delay={ delaySec :.1f}s, limit={ limitSec :.1f}s, )")

                    fadeSec  = conf.play_fadeActionSec
                    thread_pool[last_thread].begin(
                        delaySec, fadeSec, screen, panel,
                        winTitle, proc_file, conf.play_volume, fps, order,
                        conf.play_overlayTime, conf.play_overlayDate, startSec, limitSec, )
                    thread_start[last_thread] = time.time() + delaySec
                    thread_limitSec[last_thread] = limitSec

                    # time.sleep(delaySec - conf.play_fadeActionSec - 1)
                    if (about_play == False):
                        waitSec = delaySec - conf.play_fadeActionSec - 1
                        qLog.log('info', main_id, f"Play Wait   ( { waitSec :.1f}s )" )

                        chkTime = time.time()
                        while ((time.time() - chkTime) < waitSec):
                            time.sleep(0.20)

                            # マウス操作？
                            if (conf.play_stopByMouseSec != 0):
                                if ((runMode == 'bgmusic') or (runMode == 'bgmdrive') or (runMode == 'bgvideo')) and (screen is not None):
                                    (x, y),s = qGUI.screenPosition(screen=screen)
                                else:
                                    (x, y) = qGUI.position()
                                if (abs(last_mouse_x-x) < 50) and (abs(last_mouse_y-y) < 50):
                                    last_mouse_x = x
                                    last_mouse_y = y
                                else:
                                    last_mouse_x = x
                                    last_mouse_y = y
                                    last_mouse_time = time.time()

                                    # 再生停止
                                    qLog.log('info', main_id, f"Play '{ play_file }' (Wait) Cancel !!!")
                                    about_play = True

                                    waitMax = 0
                                    thread_pool[old_thread2].abort(waitMax=waitMax, )
                                    waitMax = 5
                                    thread_pool[old_thread ].abort(waitMax=waitMax, )
                                    thread_pool[last_thread].abort(waitMax=waitMax, )
                                    break

                    # フェード処理 (1)
                    if (about_play == False):
                        if (conf.play_fadeActionSec == 0):
                            time.sleep(3.00)
                        else:
                            fadeSec = conf.play_fadeActionSec

                            # フェード処理(out)
                            outSec = fadeSec / 2
                            qLog.log('info', main_id, f"Play fadeOut ( { outSec :.1f}s )" )
                            gui.fadeOut(screen=screen, panel=panel, mask='black', outSec=outSec, )

                    # 新しいスレッド開始（最大5秒待機）
                    if (about_play == False):
                        chkTime = time.time()
                        while (thread_pool[last_thread].is_alive() == False) and ((time.time() - chkTime) < 5):
                            time.sleep(0.20)

                            # マウス操作？
                            if (conf.play_stopByMouseSec != 0):
                                if ((runMode == 'bgmusic') or (runMode == 'bgmdrive') or (runMode == 'bgvideo')) and (screen is not None):
                                    (x, y),s = qGUI.screenPosition(screen=screen)
                                else:
                                    (x, y) = qGUI.position()
                                if (abs(last_mouse_x-x) < 50) and (abs(last_mouse_y-y) < 50):
                                    last_mouse_x = x
                                    last_mouse_y = y
                                else:
                                    last_mouse_x = x
                                    last_mouse_y = y
                                    last_mouse_time = time.time()

                                    # 再生停止
                                    qLog.log('info', main_id, f"Play '{ play_file }' (play) Cancel !!! (1)")
                                    about_play = True

                                    waitMax = 0
                                    thread_pool[old_thread2].abort(waitMax=waitMax, )
                                    waitMax = 5
                                    thread_pool[old_thread ].abort(waitMax=waitMax, )
                                    thread_pool[last_thread].abort(waitMax=waitMax, )

                                    if (conf.play_fadeActionSec >= 1):
                                       gui.fadeIn(inSec=0, ) 
                                    break

                    # 古いスレッド終了（最大５秒待機）
                    waitMax = 5
                    thread_pool[old_thread].delayAbort(delaySec=waitMax, )

                    if (about_play == False):
                        chkTime = time.time()
                        while (thread_pool[old_thread].is_alive() == True) and ((time.time() - chkTime) < 5):
                            time.sleep(0.20)

                            # マウス操作？
                            if (conf.play_stopByMouseSec != 0):
                                if ((runMode == 'bgmusic') or (runMode == 'bgmdrive') or (runMode == 'bgvideo')) and (screen is not None):
                                    (x, y),s = qGUI.screenPosition(screen=screen)
                                else:
                                    (x, y) = qGUI.position()
                                if (abs(last_mouse_x-x) < 50) and (abs(last_mouse_y-y) < 50):
                                    last_mouse_x = x
                                    last_mouse_y = y
                                else:
                                    last_mouse_x = x
                                    last_mouse_y = y
                                    last_mouse_time = time.time()

                                    # 再生停止
                                    qLog.log('info', main_id, f"Play '{ play_file }' (play) Cancel !!! (2)")
                                    about_play = True

                                    waitMax = 0
                                    thread_pool[old_thread2].abort(waitMax=waitMax, )
                                    waitMax = 5
                                    thread_pool[old_thread ].abort(waitMax=waitMax, )
                                    thread_pool[last_thread].abort(waitMax=waitMax, )

                                    if (conf.play_fadeActionSec >= 1):
                                       gui.fadeIn(inSec=0, ) 
                                    break

                    # 古いスレッド終了（強制終了）
                    waitMax = 5
                    thread_pool[old_thread].abort(waitMax=waitMax, )

                    # フェード処理 (2)
                    if (about_play == False):
                        if (conf.play_fadeActionSec != 0):
                            fadeSec = conf.play_fadeActionSec

                            # フェード処理(in)
                            inSec = fadeSec / 2
                            qLog.log('info', main_id, f"Play fadeIn  ( { inSec :.1f}s )" )
                            gui.fadeIn(inSec=inSec, )
 
                    # 最前面へ
                    if (runMode != 'bgm') and (runMode != 'bgmusic'):
                        time.sleep(1.00)
                        qGUI.setForegroundWindow(winTitle=winTitle, )

                    # テロップ
                    if (about_play == False):
                        if (conf.play_file_telop == 'yes'):

                            header = 'Play'
                            if   (runMode == 'bgm') or (runMode == 'bgmusic') \
                            or   (runMode == 'bgmdrive'):
                                header = 'BGM'
                                proc.telopMSG(title=header, txt=title, )
                            elif (runMode == 'bgv') or (runMode == 'bgvideo'):
                                header = 'BGV'
                                proc.telopMSG(title=header, txt=winTitle, )
                            else:
                                proc.telopMSG(title=header, txt=title, )

                    # 古いスレッド終了（破棄）
                    waitMax = 5
                    thread_pool[old_thread2].abort(waitMax=waitMax, )
                    #del thread_pool[old_thread2]
                    #thread_pool[old_thread2] = None

                    # # 古いスレッド終了（停止）
                    # thread_pool[old_thread].delayAbort(delaySec=waitMax, )

                    # 次のスレッド用意
                    try:
                        waitMax = 0
                        thread_pool[next_thread].abort(waitMax=waitMax, )
                    except:
                        pass
                    #del thread_pool[next_thread]
                    #thread_pool[next_thread]     = _v6__qFFmpeg.qFFplay_class()
                    #thread_start[next_thread]    = time.time()
                    #thread_limitSec[next_thread] = 0

                    #gc.collect()



            # -----------------------
            # 終了処理
            # -----------------------
            if (break_flag == True) or (about_play == True):

                # 全再生停止
                for t in range(thread_max):
                    try:
                        waitMax = 5
                        thread_pool[t].abort(waitMax=waitMax, )
                    except:
                        pass
                    #del thread_pool[old_thread2]
                    #thread_pool[old_thread2] = None

            if (about_play == True):
                if (runMode == 'bgm') or (runMode == 'bgmusic') \
                or (runMode == 'bgmdrive') \
                or (runMode == 'bgv') or (runMode == 'bgvideo'):
                    break_flag = True

                    # 終了待機
                    if (conf.play_stopByMouseSec != 0):
                        qLog.log('warning', main_id, f"screen({ screen }) is about!  Waiting sec = { conf.play_stopByMouseSec }s. ")

                        chkTime = time.time()
                        while ((time.time() - chkTime) < conf.play_stopByMouseSec):
                            time.sleep(1.00)

                            # 画面構成変更？
                            change_screen = qGUI.checkUpdateScreenInfo(update=True, )
                            if (change_screen == True):
                                break

                            # マウス操作？
                            if ((runMode == 'bgmusic') or (runMode == 'bgmdrive') or (runMode == 'bgvideo')) and (screen is not None):
                                (x, y),s = qGUI.screenPosition(screen=screen)
                            else:
                                (x, y) = qGUI.position()
                            if (abs(last_mouse_x-x) < 50) and (abs(last_mouse_y-y) < 50):
                                last_mouse_x = x
                                last_mouse_y = y
                            else:
                                last_mouse_x = x
                                last_mouse_y = y
                                last_mouse_time = time.time()

                                # 終了待機　時間リセット
                                qLog.log('info', main_id, f"(re)Waiting sec = { conf.play_stopByMouseSec }s. ")
                                chkTime = time.time()

            if (break_flag == True):

                # 終了
                qLog.log('error', main_id, f"screen({ screen }) is ended. ")
                time.sleep(5.00)
                break



            # -------------
            # メインビート
            # -------------
            # 再生中
            if (thread_pool[last_thread].is_alive() == True):
                time.sleep(0.50)
            # アイドル中
            else:
                time.sleep(1.00)



        #except Exception as e:
        #    print(e)
        #    time.sleep(5.00)



    # 終了処理
    if (True):
        qLog.log('info', main_id, 'terminate')

        # 終了
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


