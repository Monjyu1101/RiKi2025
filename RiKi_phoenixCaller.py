#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
import os
import time
import datetime
import codecs
import glob

import subprocess



# パス設定
qPath_base = os.path.dirname(sys.argv[0]) + '/'
if (qPath_base == '/'):
    qPath_base = os.getcwd() + '/'
else:
    os.chdir(qPath_base)

# インターフェース
qPath_temp  = 'temp/'
qPath_log   = 'temp/_log/'
qCtrl_control_kernel = 'temp/control_kernel.txt'
qCtrl_control_self   = qCtrl_control_kernel

# 共通ルーチン
import    _v6__qFunc
qFunc   = _v6__qFunc.qFunc_class()
import    _v6__qLog
qLog    = _v6__qLog.qLog_class()

# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



runMode = 'debug'
parm    = []



if __name__ == '__main__':
    main_name = 'phoenix'
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

    # ディレクトリ作成
    qFunc.makeDirs(qPath_temp, remove=False, )
    qFunc.makeDirs(qPath_log,  remove=False, )

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
        parm = sys.argv[2:]
        if (len(sys.argv) >= 3):
            parm = sys.argv[2:]

        qLog.log('info', main_id, 'runMode = ' + str(runMode ))
    if (len(parm) >= 1):
        qLog.log('info', main_id, 'parm[0] = ' + str(parm[0] ))
    if (len(parm) >= 2):
        qLog.log('info', main_id, 'parm[1] = ' + str(parm[1] ))

    # 初期設定
    if (True):
        qFunc.remove(qCtrl_control_self)

        # ライセンス制限
        if (dateinfo_today >= dateinfo_start):
            qLog.log('warning', main_id, '利用ライセンスは、 ' + limit_date + ' まで有効です。')
        if (dateinfo_today > limit_date):
            time.sleep(60)
            sys.exit(0)

        # プロセス
        process_pool = {}
        process_pid  = {}
        process_parm = {}
        process_boot = {}
        for p in range(1): # 1 task
            process_pool[p] = None
            process_pid[p]  = None
            process_parm[p] = parm
            process_boot[p] = time.time()

        # 開始時間
        main_start = time.time()



    # 無限ループ
    break_flag = False
    while (break_flag == False):
        reboot_flag = False

        # 終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            qLog.log('info', main_id, '' + str(txt))
            # 終了
            if (txt == '_end_'):
                break_flag  = True
                reboot_flag = True

        # # リブート時間経過 ! 2024/03/17時点、terminate 出来ない！
        # if ((runMode == 'reboot15')  and ((time.time() - main_start) >  15*60)) \
        # or ((runMode == 'reboot60')  and ((time.time() - main_start) >  60*60)) \
        # or ((runMode == 'reboot120') and ((time.time() - main_start) > 120*60)) \
        # or ((runMode == 'reboot180') and ((time.time() - main_start) > 180*60)):
        #     reboot_flag = True

        # 全終了
        if (reboot_flag == True):
            time.sleep(5.00)
            p_keys = list(process_pool.keys())
            for p in p_keys:
                if (process_pool[p] is not None):

                    # 終了処理 ! 2024/03/17時点、terminate 出来ない！
                    qLog.log('info', main_id, 'terminate! ' + str(process_parm[p][0]))
                    try:
                        process_pool[p].terminate()
                        process_pool[p] = None
                    except:
                        process_pool[p] = None
                    if (process_pid[p] is not None):
                        qFunc.kill_pid(process_pid[p])
                    process_pid[p] = None

                    #qLog.log('info', main_id, 'kill ' + str(parm[0]), )
                    #qFunc.kill(str(parm[0]))
                    #if (p == 0):
                    #    qLog.log('info', main_id, 'kill ffplay', )
                    #    qFunc.kill('ffplay')

        # 個別終了
        p_keys = list(process_pool.keys())
        for p in p_keys:
            if (process_pool[p] is not None):

                if   ((runMode == 'reload15')  and ((time.time() - process_boot[p]) >  15*60)) \
                or   ((runMode == 'reload60')  and ((time.time() - process_boot[p]) >  60*60)) \
                or   ((runMode == 'reload120') and ((time.time() - process_boot[p]) > 120*60)) \
                or   ((runMode == 'reload180') and ((time.time() - process_boot[p]) > 180*60)):

                    # 終了処理 ! 2024/03/17時点、terminate 出来ない！
                    qLog.log('info', main_id, 'terminate! ' + str(process_parm[p][0]))
                    try:
                        process_pool[p].terminate()
                        process_pool[p] = None
                    except:
                        process_pool[p] = None
                    if (process_pid[p] is not None):
                        qFunc.kill_pid(process_pid[p])
                    process_pid[p] = None

                    #qLog.log('info', main_id, 'kill ' + str(parm[0]), )
                    #qFunc.kill(str(parm[0]))
                    #if (p == 0):
                    #    qLog.log('info', main_id, 'kill ffplay', )
                    #    qFunc.kill('ffplay')

        # リブート (windows)
        #if (break_flag == False) and (reboot_flag == True):
        #    if (os.name == 'nt'):
        #
        #        # 起動処理
        #        cmd = []
        #        cmd.append(basename)
        #        cmd = cmd + sys.argv[1:]
        #        #print(cmd)
        #        qLog.log('info', main_id, 'reboot ' + cmd[2] + ', ' + cmd[3] + ', ' + cmd[4] + ', ...')
        #        x = subprocess.Popen(['cmd.exe', '/c', 'start', '/min'] + cmd)
        #
        #        # 終了
        #        break

        # ブレーク
        if (break_flag == True):
            break

        # 状態確認
        p_keys = list(process_pool.keys())
        for p in p_keys:
            if (process_pool[p] is not None):

                # 稼働確認
                if (process_pool[p].poll() is None):
                    time.sleep(1.00)
                
                else:

                    # 終了処理
                    qLog.log('info', main_id, 'ended. ' + str(process_parm[p][0]))
                    try:
                        process_pool[p].terminate()
                        process_pool[p] = None
                    except:
                        process_pool[p] = None
                    if (process_pid[p] is not None):
                        qFunc.kill_pid(process_pid[p])
                    process_pid[p] = None
                    #qLog.log('info', main_id, 'kill ' + str(parm[0]), )
                    #qFunc.kill(str(parm[0]))

        # 再起動処理
        p_keys = list(process_pool.keys())
        for p in p_keys:
            if (process_pool[p] is None):
                time.sleep(5.00)

                # 再起動
                qLog.log('info', main_id, '(re)start ' + str(process_parm[p][0]) + ' ' + str(process_parm[p][1]))
                if (os.name == 'nt'):
                    process_pool[p] = subprocess.Popen(['cmd.exe', '/c'] + process_parm[p])
                    #process_pool[p] = subprocess.Popen(process_parm[p])
                else:
                    process_pool[p] = subprocess.Popen(process_parm[p])
                process_pid[p]  = process_pool[p].pid
                process_boot[p] = time.time()



        time.sleep(1.00)



    # 終了処理
    if (True):
        qLog.log('info', main_id, 'terminate')

        # 終了
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


