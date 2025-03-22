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

import numpy as np
import cv2



# インターフェース
qPath_temp = 'temp/'
qPath_log  = 'temp/_log/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

import   _v6__qFFmpeg



class _camera:

    def __init__(self, ):
        self.runMode = 'debug'

    def init(self, qLog_fn='', runMode='debug', conf=None,
             name='thread', id='0',  
             camDev='0', 
             cv2_engine='ssd', cv2_intervalSec='2', cv2_sabunLimit='1', cv2_sometime='no',
            ):

        self.runMode         = runMode
        self.name            = name
        self.id              = id
        self.camDev          = camDev
        self.cv2_engine      = cv2_engine
        self.cv2_intervalSec = float(cv2_intervalSec)
        self.cv2_sabunLimit  = float(cv2_sabunLimit)
        self.cv2_sometime    = cv2_sometime

        if (not str(camDev).isdigit()):
            self.cv2_sometime    = 'yes'

        # ログ
        self.proc_name = name
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        self.proc_id   = self.proc_id[:-2] + '_' + str(id)
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')
        self.logDisp = True

        # カメラ初期化
        self.qCV2 = _v6__qFFmpeg.qCV2_class()
        if (self.cv2_sometime != 'yes'):
            self.cam = self.qCV2.cv2open(dev=self.camDev, )
            time.sleep(0.25)

    def __del__(self):
        if (self.cv2_sometime != 'yes'):
            try:
                self.qCV2.cv2close()
                time.sleep(0.25)
            except:
                pass
        qLog.log('info', self.proc_id, 'bye!', display=self.logDisp, )

    def begin(self, ):
        self.breakFlag = threading.Event()
        self.breakFlag.clear()
        self.proc_s = queue.Queue()
        self.proc_r = queue.Queue()
        self.proc_main = threading.Thread(target=self.main_proc, args=(self.proc_s, self.proc_r, ), daemon=True, )
        self.proc_beat = time.time()
        self.proc_last = time.time()
        self.proc_seq  = 0
        self.proc_main.start()

    def abort(self, waitMax=5, ):
        qLog.log('info', self.proc_id, 'stop', display=self.logDisp, )
        chktime = time.time()
        while (self.proc_beat is not None) and ((time.time() - chktime) < waitMax):
            self.breakFlag.set()
            time.sleep(0.25)
        if (self.proc_beat is not None):
            qLog.log('debug', self.proc_id, 'abort -> break!', display=self.logDisp, )

    def put(self, data, ):
        self.proc_s.put(data)
        return True

    def checkGet(self, waitMax=5, ):
        chktime = time.time()
        while (self.proc_r.qsize() == 0) and ((time.time() - chktime) < waitMax):
            time.sleep(0.10)
        data = self.get()
        return data

    def get(self, ):
        if (self.proc_r.qsize() == 0):
            return ['', '']
        data = self.proc_r.get()
        self.proc_r.task_done()
        return data

    def main_proc(self, cn_r, cn_s, ):
        # ログ
        qLog.log('info', self.proc_id, 'start ' + self.camDev, display=self.logDisp, )
        self.proc_beat = time.time()

        last_hit   = time.time() - self.cv2_intervalSec
        last_alive = time.time()

        # 初回差分無視　(静止画対策)
        if (True):

            # オープン
            if (self.cv2_sometime == 'yes'):
                self.cam = self.qCV2.cv2open(dev=self.camDev, )
                time.sleep(0.25)

            # イメージ取得
            frame = None
            chkTime = time.time()
            while (frame is None) and ((time.time() - chkTime) < 1):
                frame = self.qCV2.cv2read()
                time.sleep(0.25)

            if (frame is not None):

                # 差分確認
                if (self.cv2_sabunLimit > 0):
                    for i in range(5): #５回転
                        _, _, _, _ = self.qCV2.cv2sabun(inp_image=frame, )

            # クローズ
            if (self.cv2_sometime == 'yes'):
                self.cam = self.qCV2.cv2close()
                #time.sleep(0.25)

        # ループ
        while (True):
            self.proc_beat = time.time()

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                break

            # 活動メッセージ
            if  ((time.time() - last_alive) > 30):
                qLog.log('debug', self.proc_id, 'alive', )
                last_alive = time.time()

            # キュー取得
            if (cn_r.qsize() > 0):
                cn_r_get  = cn_r.get()
                inp_name  = cn_r_get[0]
                inp_value = cn_r_get[1]
                cn_r.task_done()
            else:
                inp_name  = ''
                inp_value = ''

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 20):
                qLog.log('warning', self.proc_id, 'queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            # 画像処理
            if (cn_s.qsize() == 0):

                # オープン
                if (self.cv2_sometime == 'yes'):
                    self.cam = self.qCV2.cv2open(dev=self.camDev, )

                # イメージ取得
                frame = self.qCV2.cv2read()
                if (frame is None):

                    # 再取得
                    qLog.log('warning', self.proc_id, 'cam read error reopen, ' + str(self.camDev))
                    self.cam = self.qCV2.cv2close()
                    time.sleep(1.00)
                    self.cam = self.qCV2.cv2open(dev=self.camDev, )
                    time.sleep(1.00)
                    chkTime = time.time()
                    while (not self.breakFlag.is_set()) and (frame is None) and ((time.time() - chkTime) < 5):
                        frame = self.qCV2.cv2read()
                        time.sleep(0.25)

                    # 停止要求確認
                    if (self.breakFlag.is_set()):
                        self.breakFlag.clear()
                        break

                if (frame is not None):

                    # 差分確認
                    inp_image   = frame.copy()
                    out_image   = frame.copy()
                    base_image  = frame.copy()
                    sabun_image = frame.copy()
                    sabun_ritu  = 0
                    if  (self.cv2_sabunLimit > 0):
                        out_image, base_image, sabun_image, sabun_ritu = self.qCV2.cv2sabun(inp_image=inp_image, )

                    if  (self.cv2_sabunLimit > 0) \
                    and (sabun_ritu < self.cv2_sabunLimit):

                        out_name  = '[img]'
                        out_value = out_image.copy()
                        cn_s.put([out_name, out_value])

                    else:
                        if ((time.time() - last_hit) <= self.cv2_intervalSec):
                            out_name  = '[img]'
                            out_value = out_image.copy()
                            cn_s.put([out_name, out_value])

                        else:

                            # ログ
                            if (self.cv2_intervalSec >= 1):
                                qLog.log('info', self.proc_id, 'Cam Image Check', display=self.logDisp, )

                            # 人間確認
                            parson_imgs = []
                            face_imgs   = []
                            if   (self.cv2_engine=='yolov8'):
                                parson_img, parson_imgs, _, _, _ = self.qCV2.cv2detect_yolov8(inp_image=sabun_image, base_image=base_image, search='person', )
                            elif (self.cv2_engine=='yolov4'):
                                parson_img, parson_imgs, _, _, _ = self.qCV2.cv2detect_yolov4(inp_image=sabun_image, base_image=base_image, search='person', )
                            elif (self.cv2_engine=='ssd'):
                                parson_img, parson_imgs, _, _, _ = self.qCV2.cv2detect_ssd(inp_image=sabun_image, base_image=base_image, search='person', )
                            else:
                                face_img, face_imgs  = self.qCV2.cv2detect_cascade(inp_image=sabun_image, base_image=base_image, search='face', )

                            # 停止要求確認
                            if (self.breakFlag.is_set()):
                                self.breakFlag.clear()
                                break

                            # 画像返信
                            if (self.cv2_engine=='yolov8') \
                            or (self.cv2_engine=='yolov4') \
                            or (self.cv2_engine=='ssd'):
                                if (len(parson_imgs) > 0):
                                    out_name  = '[person_raw]'
                                    out_value = inp_image.copy()
                                    cn_s.put([out_name, out_value])
                                    out_name  = '[person_img]'
                                    out_value = parson_img.copy()
                                    cn_s.put([out_name, out_value])
                                else:
                                    out_name  = '[img]'
                                    out_value = out_image.copy()
                                    cn_s.put([out_name, out_value])
                            else:
                                if (len(face_imgs) > 0):
                                    out_name  = '[face_raw]'
                                    out_value = inp_image.copy()
                                    cn_s.put([out_name, out_value])
                                    out_name  = '[face_img]'
                                    out_value = face_imgs[0].copy()
                                    cn_s.put([out_name, out_value])
                                else:
                                    out_name  = '[img]'
                                    out_value = out_image.copy()
                                    cn_s.put([out_name, out_value])

                            if (len(parson_imgs) > 0) \
                            or (len(face_imgs) > 0):
                                last_hit = time.time()

                        # 画像判断時、
                        # 差分リセット
                        if  (self.cv2_sabunLimit > 0):
                            for i in range(5): #５回転
                                _, _, _, _ = self.qCV2.cv2sabun(inp_image=frame, )

                # クローズ
                if (self.cv2_sometime == 'yes'):
                    self.cam = self.qCV2.cv2close()

            # アイドリング
            if  (self.runMode == 'personal'):
                time.sleep(0.25)
            else:
                time.sleep(0.05)

        # 終了処理
        if (True):

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # 停止サイン
            self.proc_beat = None

            # ログ
            qLog.log('info', self.proc_id, 'end', display=self.logDisp, )



if __name__ == '__main__':

    sub = _camera()

    sub.init(qLog_fn='', runMode='debug', conf=None, camDev='0', )
    sub.begin()
    time.sleep(5.00)
    sub.abort()
    time.sleep(5.00)
    del sub


