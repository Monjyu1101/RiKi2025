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
from PIL import Image, ImageDraw, ImageFont



# インターフェース
qPath_temp    = 'temp/'
qPath_log     = 'temp/_log/'
qPath_work    = 'temp/_work/'

qPath_d_telop = 'temp/d6_7telop_txt/'
qBusy_dev_cpu = qPath_work + 'busy_dev_cpu.txt'
qBusy_d_telop = qPath_work + 'busy_d_9telop.txt'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

import   _v6__qFFmpeg



# フォント
qPath_fonts   = '_fonts/'
#qFont_default   = {'file':qPath_fonts + 'JF-Dot-jiskan24-2000.ttf','offset':32}
qFont_default   = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':32}
font_size = 96
font_default  = ImageFont.truetype(qFont_default['file'], font_size, encoding='unic')
font_defaulty =                    qFont_default['offset']



class _telop2mov:

    def __init__(self, ):
        self.runMode = 'debug'
        self.path    = qPath_d_telop

    def init(self, qLog_fn='', runMode='debug', conf=None,
             name='thread', id='0',  
        ):

        self.runMode   = runMode
        self.name      = name
        self.id        = id

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

        self.breakFlag = threading.Event()
        self.breakFlag.clear()

        self.proc_s    = None
        self.proc_r    = None
        self.proc_main = None
        self.proc_beat = None
        self.proc_last = None
        self.proc_step = '0'
        self.proc_seq  = 0

        # テロップ配列
        self.ary_seq  = 9
        self.ary_max  = 9
        self.ary_time = {}
        self.ary_img  = {}
        self.ary_file = {}
        self.ary_play = {}
        for i in range(1, self.ary_max+1):
            self.ary_time[i] = time.time()
            self.ary_img[i]  = None
            self.ary_file[i] = ''
            self.ary_play[i] = 0

        # 規定値
        if (conf is None):
            self.video_nullSec          = '1.0'
            self.video_beforeSec        = '3.0'
            self.video_afterSec         = '1.0'
            self.video_fps              = '60'
            self.video_moveStep         = '4'
            self.telop_limitSec         = '300'
            self.telop_limitPlay        = '2'
            self.telop_bgColor          = '(0,0,0)'
            self.telop_fgColor          = '(0,165,255)'
            self.telop_bgColor_val      = eval(self.telop_bgColor)
            self.telop_fgColor_val      = eval(self.telop_fgColor)
        else:
            self.video_nullSec          = conf.video_nullSec
            self.video_beforeSec        = conf.video_beforeSec
            self.video_afterSec         = conf.video_afterSec
            self.video_fps              = conf.video_fps
            self.video_moveStep         = conf.video_moveStep
            self.telop_limitSec         = conf.telop_limitSec
            self.telop_limitPlay        = conf.telop_limitPlay
            self.telop_bgColor          = conf.telop_bgColor
            self.telop_fgColor          = conf.telop_fgColor
            self.telop_bgColor_val      = conf.telop_bgColor_val
            self.telop_fgColor_val      = conf.telop_fgColor_val




    def __del__(self, ):
        qLog.log('info', self.proc_id, 'bye!', display=self.logDisp, )

    def begin(self, ):
        #qLog.log('info', self.proc_id, 'start')

        self.fileRun = qPath_work + self.proc_id + '.run'
        self.fileRdy = qPath_work + self.proc_id + '.rdy'
        self.fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.statusSet(self.fileRun, False)
        qFunc.statusSet(self.fileRdy, False)
        qFunc.statusSet(self.fileBsy, False)

        self.proc_s = queue.Queue()
        self.proc_r = queue.Queue()
        self.proc_main = threading.Thread(target=self.main_proc, args=(self.proc_s, self.proc_r, ), daemon=True, )
        self.proc_beat = time.time()
        self.proc_last = time.time()
        self.proc_step = '0'
        self.proc_seq  = 0
        self.proc_main.start()

    def abort(self, waitMax=5, ):
        qLog.log('info', self.proc_id, 'stop', display=self.logDisp, )

        self.breakFlag.set()
        chktime = time.time()
        while (self.proc_beat is not None) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)
        chktime = time.time()
        while (os.path.exists(self.fileRun)) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)

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
        qLog.log('info', self.proc_id, 'start', display=self.logDisp, )
        qFunc.statusSet(self.fileRun, True)
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        #txts, txt = qFunc.txtsRead(qCtrl_control_self)
        #if (txts != False):
        #    if (txt == '_end_') or (txt == '_stop_'):
        #        qFunc.remove(qCtrl_control_self)

        # 待機ループ
        self.proc_step = '5'

        onece = True
        last_alive = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            #control = ''
            #txts, txt = qFunc.txtsRead(qCtrl_control_self)
            #if (txts != False):
            #    qLog.log('info', self.proc_id, '' + str(txt))
            #    if (txt == '_end_'):
            #        break
            #    else:
            #        qFunc.remove(qCtrl_control_self)
            #        control = txt

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # 活動メッセージ
            if  ((time.time() - last_alive) > 30):
                qLog.log('debug', self.proc_id, 'alive', display=True, )
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

            # レディ設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # 要求応答（デバッグ）
            if (inp_name.lower() == '[telop_txts]'):
                proc_file = ''
                work_file = ''
                proc_name = inp_name.lower()
                self.sub_proc('0000', proc_file, work_file, proc_name, inp_value, cn_s, )

            # 要求応答（次のテロップ）
            if (inp_name.lower() == '_next_'):

                # カウントアップ
                self.ary_seq += 1
                if (self.ary_seq > self.ary_max):
                    self.ary_seq = 1

                # 内容確認
                i = self.ary_seq
                #print(i)
                play = False
                if (self.ary_play[i] == 0) and (self.ary_file[i] != ''):
                    play = True
                else:
                    play = True
                    if (self.ary_file[i] == ''):
                            play = False
                    elif (int(self.telop_limitPlay) != 0):
                        if (self.ary_play[i] >= int(self.telop_limitPlay)):
                            play = False
                    elif (int(self.telop_limitSec) != 0):
                        sec = time.time() - self.ary_time[i]
                        if (sec > int(self.telop_limitSec)):
                            play = False

                # 応答
                if (play == True):
                    out_name  = '_telop_file_'
                    out_value = self.ary_file[i]
                    cn_s.put([out_name, out_value])
                    self.ary_play[i] += 1
                    #print(out_value)

            # 処理
            path = self.path
            path_files = glob.glob(path + '*.txt')
            path_files.sort()
            if (len(path_files) > 0):

                #try:
                if (True):

                    for f in path_files:

                        # 停止要求確認
                        if (self.breakFlag.is_set()):
                            self.breakFlag.clear()
                            self.proc_step = '9'
                            break

                        proc_file = f.replace('\\', '/')

                        if (proc_file[-4:].lower() == '.txt' and proc_file[-8:].lower() != '.wrk.txt'):
                            f1 = proc_file
                            f2 = proc_file[:-4] + '.wrk.txt'
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except Exception as e:
                                pass

                        if (proc_file[-8:].lower() == '.wrk.txt'):
                            f1 = proc_file
                            f2 = proc_file[:-8] + proc_file[-4:]
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except Exception as e:
                                pass

                            # 実行カウンタ
                            self.proc_last = time.time()
                            self.proc_seq += 1
                            if (self.proc_seq > 9999):
                                self.proc_seq = 1
                            seq4 = '{:04}'.format(self.proc_seq)
                            seq2 = '{:02}'.format(self.proc_seq)

                            proc_name = proc_file.replace(path, '')
                            proc_name = proc_name[:-4]

                            work_name = self.proc_id + '.' + seq2
                            work_file = qPath_work + work_name + '.txt'
                            if (os.path.exists(work_file)):
                                os.remove(work_file)

                            if (proc_file[-9:].lower() != '_sjis.txt'):
                                proc_txts, proc_text = qFunc.txtsRead(proc_file, encoding='utf-8', exclusive=False, )
                            else:
                                proc_txts, proc_text = qFunc.txtsRead(proc_file, encoding='shift_jis', exclusive=False, )

                            if (proc_txts != False):
                                if (proc_text != '') and (proc_text != '!'):
                                    qFunc.txtsWrite(work_file, txts=proc_txts, encoding='utf-8', exclusive=False, mode='w', )

                                if (os.path.exists(work_file)):

                                    qFunc.remove(proc_file)

                                    # ログ
                                    #if (self.runMode == 'debug') or (not self.micDev.isdigit()):
                                    #    qLog.log('info', self.proc_id, '' + proc_name + ' → ' + work_name, display=self.logDisp,)

                                    # 結果出力
                                    #if (cn_s.qsize() < 99):
                                    #    out_name  = '[txts]'
                                    #    out_value = proc_txts
                                    #    cn_s.put([out_name, out_value])

                                    # ビジー設定
                                    if (qFunc.statusCheck(self.fileBsy) == False):
                                        qFunc.statusSet(self.fileBsy, True)
                                        if (str(self.id) == '0'):
                                            qFunc.statusSet(qBusy_d_telop, True)

                                    # 処理
                                    self.proc_last = time.time()
                                    self.sub_proc(seq4, proc_file, work_file, proc_name, proc_txts, cn_s, )

                #except Exception as e:
                #    pass

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_telop, False)

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.50)
                else:
                    time.sleep(0.25)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qLog.log('info', self.proc_id, 'end', display=self.logDisp, )
            qFunc.statusSet(self.fileRun, False)
            self.proc_beat = None



    # 処理
    def sub_proc(self, seq4, proc_file, work_file, proc_name, txts, cn_s, ):
        #font_size = 96

        # --------------
        # テロップ画像生成
        # --------------

        # 画像サイズ計算
        title = ''
        text  = ''
        for i in range(len(txts)):
            if (i==0):
                title = txts[i]
            else:
                text += txts[i]
        title = title.replace('　', '')
        title = title.replace(' ', '')
        text  = text.replace('\r', '')
        text  = text.replace('\n', '')
        text  = text.replace('　', '')
        text  = text.replace(' ', '')
        if (text == '') or (text == '!'):
            text  = title
            title = ''

        qLog.log('info', self.proc_id, title + text, )

        title_width = int(font_size/2)
        if (len(title) > 0):
            if (qFunc.in_japanese(title) == True):
                title_width += int(len(title) * 2 * (font_size/2))
            else:
                title_width += int((len(title)+2) * 1.2 * (font_size/2))

        text_width = 0
        if (qFunc.in_japanese(text) == True):
            text_width += int(len(text) * 2 * (font_size/2) + (font_size/2))
        else:
            text_width += int((len(text)+2) * 1.2 * (font_size/2) + (font_size/2))

        out_height = int((font_defaulty/2) + font_size + (font_defaulty/2))
        out_width  = title_width + text_width

        # 文字画像作成
        base_img  = Image.new('RGB', (out_width, out_height), self.telop_bgColor_val, )
        base_draw = ImageDraw.Draw(base_img)

        if (title != ''):
            if ((self.telop_bgColor_val[0] + self.telop_bgColor_val[1] + self.telop_bgColor_val[2]) < 256):
                base_draw.text((int(font_size/2), int(font_defaulty/2)), title, font=font_default, fill=(255,255,255))
            elif ((self.telop_bgColor_val[0] + self.telop_bgColor_val[1] + self.telop_bgColor_val[2]) > 512):
                base_draw.text((int(font_size/2), int(font_defaulty/2)), title, font=font_default, fill=(0,0,0))
            else:
                base_draw.text((int(font_size/2), int(font_defaulty/2)), title, font=font_default, fill=self.telop_fgColor_val)
        if (text != ''):
            base_draw.text((title_width, int(font_defaulty/2)), text, font=font_default, fill=self.telop_fgColor_val)

        out_img = np.asarray(base_img)

        # ------------
        # ファイル名確定
        # ------------
        if (work_file == ''):
                # 実行カウンタ
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1
                seq4 = '{:04}'.format(self.proc_seq)
                seq2 = '{:02}'.format(self.proc_seq)

                work_name = self.proc_id + '.' + seq2
                work_file = qPath_work + work_name + '.txt'

        jpeg_file = work_file[:-4] + '.jpg'
        qFunc.remove(filename=jpeg_file, )
        mpeg_file = work_file[:-4] + '.mp4'
        qFunc.remove(filename=mpeg_file, )



        # ----------
        # 静止画出力
        # ----------
        try:

            cv2.imwrite(jpeg_file, out_img, )
            qLog.log('info', self.proc_id, '　->　' + jpeg_file, )

        except:
            qLog.log('critical', self.proc_id, '★静止画出力エラー　' + jpeg_file, )
            return False

        # --------
        # 動画出力
        # --------
        #try:
        if True:
            #print('output',mpeg_file,'start')
            
            fps      = int(self.video_fps)
            moveStep = int(self.video_moveStep)
            video_width  = 1280
            video_height = out_height
            video_base = np.zeros((video_height, video_width, 3), np.uint8)
            cv2.rectangle(video_base,(0,0),(video_width,video_height),self.telop_bgColor_val,-1)

            fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
            video  = cv2.VideoWriter(mpeg_file, fourcc, fps, (video_width, video_height))

            # null動画
            frame_img = video_base.copy()
            for f in range(int(fps*float(self.video_nullSec))):
                video.write(frame_img)

            # 開始動画
            for f in range(int(fps*float(self.video_beforeSec))):
                    frame_img = video_base.copy()
                    x  = int(f/int(fps*float(self.video_beforeSec))*video_width)
                    if (out_width <= video_width):
                        if (x <= out_width):
                            frame_img[ 0:out_height, 0:x ] = out_img[ 0:out_height, 0:x ]
                        else:
                            frame_img[ 0:out_height, 0:out_width ] = out_img[ 0:out_height, 0:out_width ]
                    else:
                        #frame_img[ 0:video_height, 0:video_width ] = out_img[ 0:video_height, 0:video_width ]
                        frame_img[ 0:video_height, 0:x ] = out_img[ 0:video_height, 0:x ]
                    video.write(frame_img)

            # 流れる動画
            if (out_width > video_width):
                for f in range(int((out_width - video_width)/moveStep)):
                    frame_img = video_base.copy()
                    x = int(f * moveStep)
                    frame_img[ 0:video_height, 0:video_width ] = out_img[ 0:video_height, x:x+video_width ]
                    if (title_width < (video_width/2)):
                        frame_img[ 0:video_height, 0:title_width ] = out_img[ 0:video_height, 0:title_width ]
                    video.write(frame_img)

            # 終了動画
            for f in range(int(fps*float(self.video_afterSec))):
                    frame_img = video_base.copy()
                    if (out_width <= video_width):
                        frame_img[ 0:out_height, 0:out_width ] = out_img[ 0:out_height, 0:out_width ]
                    else:
                        frame_img[ 0:video_height, 0:video_width ] = out_img[ 0:out_height, out_width-video_width:out_width ]
                    if (title_width < (video_width/2)):
                        frame_img[ 0:video_height, 0:title_width ] = out_img[ 0:video_height, 0:title_width ]
                    x  = int(f/int(fps*float(self.video_afterSec))*video_width)
                    cv2.rectangle(frame_img, (0, 0), (x, video_height), self.telop_bgColor_val, thickness=-1)
                    video.write(frame_img)

            # null動画
            frame_img = video_base.copy()
            for f in range(int(fps*float(self.video_nullSec))):
                video.write(frame_img)

            # ビデオ解放
            video.release()

            qLog.log('info', self.proc_id, '　->　' + mpeg_file, )
            time.sleep(1.00)

        #except:
        #    qLog.log('critical', self.proc_id, '★動画出力エラー　' + mpeg_file, )
        #    return False


        # Ｑ圧縮と保管
        for i in range(2, self.ary_max+1):
            self.ary_time[i-1] = self.ary_time[i]
            if (self.ary_img[i] is not None):
                self.ary_img[i-1]  = self.ary_img[i].copy()
            self.ary_file[i-1] = self.ary_file[i]
            self.ary_play[i-1] = self.ary_play[i]
            self.ary_img[i]    = None
                
        self.ary_time[self.ary_max] = time.time()
        self.ary_img[self.ary_max]  = out_img
        self.ary_file[self.ary_max] = mpeg_file
        self.ary_play[self.ary_max] = 0

        self.ary_seq = self.ary_max

        # 連携送信
        out_name  = '_telop_file_'
        out_value = mpeg_file
        cn_s.put([out_name, out_value])
        self.ary_play[self.ary_seq] += 1
        #print(out_value)

        return True
                


if __name__ == '__main__':

    sub = _telop2mov()

    sub.init(qLog_fn='', runMode='debug', conf=None,  )
    sub.begin()
    time.sleep(5.00)
    sub.abort()
    time.sleep(5.00)
    del sub


