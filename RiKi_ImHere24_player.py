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

import queue
import threading

from playsound3 import playsound



# インターフェース
qPath_temp = 'temp/'
qPath_log  = 'temp/_log/'

# 共通ルーチン
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



class _player:

    def __init__(self, ):
        self.runMode = 'debug'
        self.file_seq = 0

        # Worker デーモン起動
        self.player_queue = queue.Queue()
        worker_player = threading.Thread(target=self.player_worker, args=(), daemon=True, )
        worker_player.start()



    # Worker デーモン
    def player_worker(self, ):
        while True:
            if (self.player_queue.qsize() >= 1):
                p = self.player_queue.get()
                self.player_queue.task_done()
                if (p is not None):
                    try:
                        p.start()
                        # ダミー１つ追加
                        self.player_queue.put(None)
                        p.join()
                    except Exception as e:
                        print(e)
                        time.sleep(1.00)
            time.sleep(0.10)
        return True

    # file再生（バッチ投入）
    def batch_play(self, sounds_file=None, ):
        if (sounds_file is None) or (not os.path.isfile(sounds_file)):
            return False
        # バッチ投入
        play_proc = threading.Thread(target=self.play, args=(
                                    sounds_file,
                                    ), daemon=True, )
        self.player_queue.put(play_proc)
        return True

    # file再生
    def play(self, outFile='temp/_work/sound.mp3', ):
        if (outFile is None) or (outFile == ''):
            return False
        if (not os.path.isfile(outFile)):
            return False
        try:
            # 再生
            playsound(sound=outFile, block=True, )
            return True
        except Exception as e:
            print(e)
        return False



    def init(self, qLog_fn='', runMode='debug', conf=None, ):

        self.runMode   = runMode

        # ログ
        self.proc_name = 'player'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')
        self.logDisp = True



if __name__ == '__main__':

    player = _player()

    player.init(qLog_fn='', runMode='debug',  )

    player.batch_play(sounds_file = '_sounds/_sound_pingpong.mp3')

    time.sleep(10.00)

