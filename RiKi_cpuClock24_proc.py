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

import numpy as np
import cv2

import io

import matplotlib      #エラー対策
matplotlib.use('Agg')  #エラー対策
from matplotlib import pyplot as plt

from PIL import Image, ImageDraw, ImageFont

import psutil



# インターフェース
qPath_temp  = 'temp/'
qPath_log   = 'temp/_log/'

qPath_fonts = '_fonts/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



class _proc:

    def __init__(self, ):
        self.runMode  = 'debug'
        self.file_seq = 0

        # Worker デーモン起動
        self.worker_queue = queue.Queue()
        worker_proc = threading.Thread(target=self.proc_worker, args=(), daemon=True, )
        worker_proc.start()



    # Worker デーモン
    def proc_worker(self, ):
        while True:
            if (self.worker_queue.qsize() >= 1):
                p = self.worker_queue.get()
                self.worker_queue.task_done()
                if (p is not None):
                    try:
                        p.start()
                        # ダミー１つ追加
                        self.worker_queue.put(None)
                        p.join()
                    except Exception as e:
                        print(e)
                        time.sleep(1.00)
            time.sleep(0.25)
        return True

    # file再生（バッチ投入）
    def batch_play(self, sounds_file=None, ):
        if (sounds_file is None) or (not os.path.isfile(sounds_file)):
            return False
        # バッチ投入
        play_proc = threading.Thread(target=self.play, args=(
                                    sounds_file,
                                    ), daemon=True, )
        self.worker_queue.put(play_proc)
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
        self.proc_name = 'proc'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')
        self.logDisp = True
        
        # フォント
        self.font_dseg7 = {'file':qPath_fonts + 'DSEG7Classic-Bold.ttf','offset':8}
        try:
            self.font32_dseg7 = ImageFont.truetype(self.font_dseg7['file'], 32, encoding='unic')
            self.font32_dseg7y =                   self.font_dseg7['offset']
            self.font99_dseg7 = ImageFont.truetype(self.font_dseg7['file'], 192, encoding='unic')
            self.font99_dseg7y =                   self.font_dseg7['offset']
            self.font88_dseg7 = ImageFont.truetype(self.font_dseg7['file'], 288, encoding='unic')
            self.font88_dseg7y =                   self.font_dseg7['offset']
        except:
            self.font32_dseg7  = None
            self.font32_dseg7y = 0
            self.font99_dseg7  = None
            self.font99_dseg7y = 0
            self.font88_dseg7  = None
            self.font88_dseg7y = 0

        # 規定値
        if (conf is None):
            self.telop_path             = 'temp/d6_7telop_txt/'
            self.tts_path               = 'temp/s6_5tts_txt/'
            self.tts_header             = 'ja,google,'
            self.timeSign_sound         = '_sounds/_sound_SeatBeltSign1.mp3'
            self.timeSign_telop         = 'yes'
            self.timeSign_tts           = 'no'
        else:
            self.telop_path             = conf.telop_path
            self.tts_path               = conf.tts_path
            self.tts_header             = conf.tts_header
            self.timeSign_sound         = conf.timeSign_sound
            self.timeSign_telop         = conf.timeSign_telop
            self.timeSign_tts           = conf.timeSign_tts

        # 配色
        if (conf is None):
            self.analog_pltStyle        = 'dark_background'
            self.analog_b_fcolor        = 'white'
            self.analog_b_tcolor        = 'fuchsia'
            self.analog_b_bcolor        = 'black'
            self.analog_s_fcolor        = 'red'
            self.analog_s_bcolor1       = 'darkred'
            self.analog_s_bcolor2       = 'tomato'
            self.analog_m_fcolor        = 'cyan'
            self.analog_m_bcolor1       = 'darkgreen'
            self.analog_m_bcolor2       = 'limegreen'
            self.analog_h_fcolor        = 'cyan'
            self.analog_h_bcolor1       = 'darkblue'
            self.analog_h_bcolor2       = 'deepskyblue'
            self.digital_b_fcolor       = 'white'
            self.digital_b_tcolor       = 'fuchsia'
            self.digital_b_bcolor       = 'black'
        else:
            self.analog_pltStyle        = conf.analog_pltStyle
            self.analog_b_fcolor        = conf.analog_b_fcolor
            self.analog_b_tcolor        = conf.analog_b_tcolor
            self.analog_b_bcolor        = conf.analog_b_bcolor
            self.analog_s_fcolor        = conf.analog_s_fcolor
            self.analog_s_bcolor1       = conf.analog_s_bcolor1
            self.analog_s_bcolor2       = conf.analog_s_bcolor2
            self.analog_m_fcolor        = conf.analog_m_fcolor
            self.analog_m_bcolor1       = conf.analog_m_bcolor1
            self.analog_m_bcolor2       = conf.analog_m_bcolor2
            self.analog_h_fcolor        = conf.analog_h_fcolor
            self.analog_h_bcolor1       = conf.analog_h_bcolor1
            self.analog_h_bcolor2       = conf.analog_h_bcolor2
            self.digital_b_fcolor       = conf.digital_b_fcolor
            self.digital_b_tcolor       = conf.digital_b_tcolor
            self.digital_b_bcolor       = conf.digital_b_bcolor


        # -------------
        # デジタル時計盤
        # -------------
        width  = 750
        height = 270
        self.digital_base = np.zeros((height,width,3), np.uint8)
        if (self.digital_b_bcolor == 'white'):
            cv2.rectangle(self.digital_dseg7_0,(0,0),(width,height),(255,255,255),thickness=-1,)
        if (self.font32_dseg7 is None):
            pass
        else:
            hhmm = '{:02d}:{:02d}'.format(int(88), int(88))
            pil_image = self.cv2pil(self.digital_base)
            text_draw = ImageDraw.Draw(pil_image)
            if (self.digital_b_bcolor == 'white'):
                text_draw.text((int(width*0.05),int(height*0.25)), hhmm, font=self.font99_dseg7, fill=(232,232,232))
            else:
                text_draw.text((int(width*0.05),int(height*0.25)), hhmm, font=self.font99_dseg7, fill=(24,24,24))
            self.digital_base = self.pil2cv(pil_image)
            self.digital_height = height
            self.digital_width  = width

        # -------------
        # アナログ時計盤
        # -------------
        plt.cla()
        plt.style.use(self.analog_pltStyle)
        self.fig = plt.figure(figsize=(10,10))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-1.05,1.05)
        self.ax.set_ylim(-1.05,1.05)
        self.ax.axis('off')
        self.ax_last_hh = 24
        # 外周
        vals = np.array([100,])
        colors = [self.analog_b_fcolor,]
        self.ax.pie(vals,colors=colors,counterclock=False, startangle=90, radius=1, wedgeprops=dict(width=0.02), )
        # 目盛
        for t in range(1,60):
            t_x1 = np.sin(np.radians(t/60*360)) * 0.95
            t_x2 = np.sin(np.radians(t/60*360)) * 0.98
            t_y1 = np.cos(np.radians(t/60*360)) * 0.95
            t_y2 = np.cos(np.radians(t/60*360)) * 0.98
            self.ax.plot([t_x1,t_x2],[t_y1,t_y2],color=self.analog_b_fcolor, lw=1,)
        for t in range(1,13):
            t_x1 = np.sin(np.radians((t % 12)/12*360)) * 0.90
            t_x2 = np.sin(np.radians((t % 12)/12*360)) * 0.98
            t_y1 = np.cos(np.radians((t % 12)/12*360)) * 0.90
            t_y2 = np.cos(np.radians((t % 12)/12*360)) * 0.98
            self.ax.plot([t_x1,t_x2],[t_y1,t_y2],color=self.analog_b_fcolor, lw=3,)
        # 画像保存
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, )
        enc = np.frombuffer(buf.getvalue(), dtype=np.uint8)
        self.analog_base   = cv2.imdecode(enc, 1)
        self.analog_height = self.analog_base.shape[0]
        self.analog_width  = self.analog_base.shape[1]
        
        # -------------
        # CPU data
        # -------------
        if (runMode != 'analog'):
            n = int(self.digital_width / 5)
        else:
            n = int(self.analog_width / 5)

        self.cpu_data  = []
        self.mem_data  = []
        self.disk_data = []
        for x in range(n):
            self.cpu_data.append(float(0))
            self.mem_data.append(float(0))
            self.disk_data.append(float(0))
        self.disk_max  = 1
        disk = psutil.disk_io_counters(perdisk=False)
        self.last_disk_write = disk.write_bytes
        self.last_disk_read  = disk.read_bytes

        self.last_hhmm = ''
        self.last_s    = 0
        self.cpu_ave   = 0
        self.mem_ave   = 0
        self.disk_ave  = 0
        self.cpu_freq  = 0



    def bytes2str(self, bytes, units=[' Byte', ' KByte', ' MByte', ' GByte', ' TByte', ' PByte', ' EByte']):
        if (bytes < 1024):
            return '{:4d}'.format(bytes) + units[0]
        else:
            return self.bytes2str(int(bytes) >> 10, units[1:])

    def cv2pil(self, cv2_image=None):
        try:
            wrk_image = cv2_image.copy()
            if (wrk_image.ndim == 2):  # モノクロ
                pass
            elif (wrk_image.shape[2] == 3):  # カラー
                wrk_image = cv2.cvtColor(wrk_image, cv2.COLOR_BGR2RGB)
            elif (wrk_image.shape[2] == 4):  # 透過
                wrk_image = cv2.cvtColor(wrk_image, cv2.COLOR_BGRA2RGBA)
            pil_image = Image.fromarray(wrk_image)
            return pil_image
        except:
            pass
        return None

    def pil2cv(self, pil_image=None):
        try:
            cv2_image = np.array(pil_image, dtype=np.uint8)
            if (cv2_image.ndim == 2):  # モノクロ
                pass
            elif (cv2_image.shape[2] == 3):  # カラー
                cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)
            elif (cv2_image.shape[2] == 4):  # 透過
                cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGBA2BGRA)
            return cv2_image
        except:
            pass
        return None



    def update_graphData(self, ):
        cpu  = psutil.cpu_percent(interval=None, percpu=False)
        mem  = psutil.virtual_memory().percent
        disk = psutil.disk_io_counters(perdisk=False)
        disk_io = (disk.write_bytes - self.last_disk_write) + (disk.read_bytes - self.last_disk_read)
        self.last_disk_write = disk.write_bytes
        self.last_disk_read  = disk.read_bytes
        del self.cpu_data[0]
        del self.mem_data[0]
        del self.disk_data[0]
        self.cpu_data.append(float(cpu))
        self.mem_data.append(float(mem))
        self.disk_data.append(float(disk_io))



    def get_graphImage(self, width=320, height=240, s=0, ):
        graph_ymin  = 60
        graph_ymax  = height - 2
        base_img    = np.zeros((height,width,3), np.uint8)
        cpu_color   = (0,255,0)
        cpu_color1  = (0,197,0)
        cpu_color2  = (0,255,0)
        mem_color   = (255,127,0)
        mem_color1  = (63,0,0)
        mem_color2  = (163,95,0)
        disk_color  = (0,239,255)
        disk_color1 = (0,95,127)
        disk_color2 = (0,163,197)

        polly   = np.array([[width-1, graph_ymax+1], [0, graph_ymax+1]], dtype=np.int64, )
        max_val = 100
        for x in range(len(self.cpu_data)):
            val = int((1 - self.cpu_data[x]/max_val) * (graph_ymax-graph_ymin)) + graph_ymin 
            add_polly = np.array([x*5, val], dtype=np.int64, )
            polly = np.append(polly, [add_polly], axis=0, )
        cpu_fill  = cv2.fillPoly(base_img.copy(), pts=[polly], color=cpu_color1, )
        cpu_img   = cv2.polylines(cpu_fill.copy(), pts=[polly], isClosed=True, color=cpu_color2, thickness=2, )

        polly   = np.array([[width-1, graph_ymax+1], [0, graph_ymax+1]], dtype=np.int64, )
        max_val = 100
        for x in range(len(self.mem_data)):
            val = int((1 - self.mem_data[x]/max_val) * (graph_ymax-graph_ymin)) + graph_ymin 
            add_polly = np.array([x*5, val], dtype=np.int64, )
            polly = np.append(polly, [add_polly], axis=0, )
        mem_fill = cv2.fillPoly(base_img.copy(), pts=[polly], color=mem_color1, )
        mem_img  = cv2.polylines(mem_fill.copy(), pts=[polly], isClosed=True, color=mem_color2, thickness=2, )

        polly = np.array([[width-1, graph_ymax+1], [0, graph_ymax+1]], dtype=np.int64, )
        max_val = max(self.disk_data)
        if (max_val > self.disk_max):
            self.disk_max = max_val
        max_val = self.disk_max
        for x in range(len(self.disk_data)):
            val = int((1 - self.disk_data[x]/max_val) * (graph_ymax-graph_ymin)) + graph_ymin 
            add_polly = np.array([x*5, val], dtype=np.int64, )
            polly = np.append(polly, [add_polly], axis=0, )
        disk_fill = cv2.fillPoly(base_img.copy(), pts=[polly], color=disk_color1, )
        disk_img  = cv2.polylines(disk_fill.copy(), pts=[polly], isClosed=True, color=disk_color2, thickness=2, )

        base = cv2.addWeighted(mem_img, 1.0, disk_img, 1.0, 0.0)
        graph_img = cv2.addWeighted(base, 1.0, cpu_img, 1.0, 0.0)

        if (s != self.last_s):
            self.last_s   = s
            self.cpu_ave  = np.mean(self.cpu_data[-10:])
            self.mem_ave  = np.mean(self.mem_data[-10:])
            self.disk_ave = int(np.mean(self.disk_data[-10:]))
            self.cpu_freq = psutil.cpu_freq().current #Mhz

        txt = 'CPU  : {:4.1f} %'.format(self.cpu_ave) + ' ({:.1f}GHz)'.format(self.cpu_freq/1000)
        cv2.putText(graph_img, txt, (20,33), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, cpu_color, )
        txt = 'DISK : {}'.format(self.bytes2str(self.disk_ave))
        cv2.putText(graph_img, txt, (20,53), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, disk_color,)
        txt = 'MEM : {:4.1f} %'.format(self.mem_ave)
        cv2.putText(graph_img, txt, (20,73), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, mem_color, )

        return graph_img

    def get_eyesImage(self, width=320, height=240, sg_left2=0, sg_top2=0, sg_width=320, sg_height=240, ):
        eyes_image = np.zeros((height,width,3), np.uint8)

        color_base = (0, 0, 0)
        all_ave = np.mean(self.cpu_data)
        if   (all_ave <= 15):
            red_lv = 0
        elif (all_ave >= 65):
            red_lv = 255
        else:
            red_lv = int(((all_ave-15)/50) * 255)
            if (red_lv > 255):
                red_lv = 255
        color_eyes = (255-red_lv, 255-red_lv, 255)
        yoko0 = int(width / 6)
        tate0 = int(height * 0.7)
        yoko1 = int(yoko0 / 5) + 2
        tate1 = int(tate0 / 5) + 2
        futosa = int(height * 0.05)

        eye1_center_x = int(width / 2) - int(width / 9)
        eye1_center_y = int(height / 2) + int(height / 20)

        eye2_center_x = int(width / 2) + int(width / 9)
        eye2_center_y = int(height / 2) + int(height / 20)

        (pos_x, pos_y) = qGUI.position()
        on_x = int((pos_x - sg_left2) / (sg_width/width))
        on_y = int((pos_y - sg_top2) / (sg_height/height))

        # ポインタ
        cv2.ellipse(eyes_image, ((on_x, on_y), (10, 10), 0), (0,0,255), thickness=-1)

        # 目ん玉１
        eye_screen_x = int((eye1_center_x) * (sg_width/width)) + sg_left2
        eye_screen_y = int((eye1_center_y) * (sg_height/height)) + sg_top2
        x = pos_x - eye_screen_x
        y = eye_screen_y - pos_y
        rd = np.arctan2(x, y)
        eye_x = int(np.sin(rd) * yoko0 / 3)
        eye_y = - int(np.cos(rd) * tate0 / 3)
        #cv2.ellipse(eyes_image, ((eye1_center_x, eye1_center_y), (yoko0, tate0), 0), color_base, thickness=-1)
        cv2.ellipse(eyes_image, ((eye1_center_x, eye1_center_y), (yoko0, tate0), 0), color_eyes, thickness=futosa)
        if  (on_x >= (eye1_center_x-abs(eye_x)-5)) and (on_x <= (eye1_center_x+abs(eye_x)+5)) \
        and (on_y >= (eye1_center_y-abs(eye_y)-5)) and (on_y <= (eye1_center_y+abs(eye_y)+5)):
            #try:
            #    eyes_image[ on_y-32:on_y+32, on_x-32:on_x+32 ] = self.img_pcam6464[ 0:64, 0:64 ]
            #    self.last_icon = 'pcam'
            #except:
            cv2.ellipse(eyes_image, ((on_x, on_y), (yoko1, tate1), 0), color_eyes, thickness=-1)
            cv2.ellipse(eyes_image, ((on_x, on_y), (yoko1, tate1), 0), (0,0,0)   , thickness= 2)
        else:
            cv2.ellipse(eyes_image, ((eye1_center_x+eye_x, eye1_center_y+eye_y), (yoko1, tate1), 0), color_eyes, thickness=-1)
            cv2.ellipse(eyes_image, ((eye1_center_x+eye_x, eye1_center_y+eye_y), (yoko1, tate1), 0), (0,0,0)   , thickness= 2)

        # 目ん玉２
        eye_screen_x = int((eye2_center_x) * (sg_width/width)) + sg_left2
        eye_screen_y = int((eye2_center_y) * (sg_height/height)) + sg_top2
        x = pos_x - eye_screen_x
        y = eye_screen_y - pos_y
        rd = np.arctan2(x, y)
        eye_x = int(np.sin(rd) * yoko0 / 3)
        eye_y = - int(np.cos(rd) * tate0 / 3)
        #cv2.ellipse(digital_eyes, ((eye2_center_x, eye2_center_y), (yoko0, tate0), 0), color_base, thickness=-1)
        cv2.ellipse(eyes_image, ((eye2_center_x, eye2_center_y), (yoko0, tate0), 0), color_eyes, thickness=futosa)
        if  (on_x >= (eye2_center_x-abs(eye_x)-5)) and (on_x <= (eye2_center_x+abs(eye_x)+5)) \
        and (on_y >= (eye2_center_y-abs(eye_y)-5)) and (on_y <= (eye2_center_y+abs(eye_y)+5)):
            #try:
            #    eyes_image[ on_y-32:on_y+32, on_x-32:on_x+32 ] = self.img_vcam6464[ 0:64, 0:64 ]
            #    self.last_icon = 'vcam'
            #except:
            cv2.ellipse(eyes_image, ((on_x, on_y), (yoko1, tate1), 0), color_eyes, thickness=-1)
            cv2.ellipse(eyes_image, ((on_x, on_y), (yoko1, tate1), 0), (0,0,0)   , thickness= 2)
        else:        
            cv2.ellipse(eyes_image, ((eye2_center_x+eye_x, eye2_center_y+eye_y), (yoko1, tate1), 0), color_eyes, thickness=-1)
            cv2.ellipse(eyes_image, ((eye2_center_x+eye_x, eye2_center_y+eye_y), (yoko1, tate1), 0), (0,0,0)   , thickness= 2)

        return eyes_image

    def get_overlayImage(self, img=None, graph_img=None, eyes_image=None, ):
        if (img is None) or (graph_img is None) or (eyes_image is None):
            return img

        # 目ん玉合成
        base = cv2.addWeighted(img, 0.7, graph_img, 1.0, 0.0)
        over = eyes_image
        # 表側でマスク作成
        gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)    
        # 表側,裏側,合成
        fg = cv2.bitwise_and(over, over, mask = mask)
        bg = cv2.bitwise_and(base, base, mask = mask_inv)
        img = cv2.add(bg, fg)

        return img



    def getImage_digital(self, dt_now, design=0, eyes=True, sg_left2=0, sg_top2=0, sg_width=320, sg_height=240, ):
        self.last_icon = None

        yy = dt_now.year
        mm = dt_now.month
        dd = dt_now.day
        h = dt_now.hour
        m = dt_now.minute
        s = dt_now.second

        width  = self.digital_width
        height = self.digital_height

        #----------
        # デジタル
        #----------
        if (self.font32_dseg7 is None):
            ymd  = '{:04d}. {:02d}. {:02d}.'.format(yy, mm, dd)
        else:
            ymd  = '{:04d}.    {:02d}.    {:02d}.'.format(yy, mm, dd)
        hhmm = '{:02d}:{:02d}'.format(int(h), int(m))
        if (hhmm != self.last_hhmm):
            self.last_hhmm = hhmm
            
            self.digital_dseg7_0 = np.zeros((height,width,3), np.uint8)
            if (self.font32_dseg7 is None):
                cv2.putText(self.digital_dseg7_0, ymd, (int(width*0.27),int(height*0.2)), cv2.FONT_HERSHEY_TRIPLEX, 2, (223,223,0))
                cv2.putText(self.digital_dseg7_0, hhmm, (int(width*0.10),int(height*0.85)), cv2.FONT_HERSHEY_TRIPLEX, 7, (255,0,255))
                self.digital_dseg7_1 = self.digital_dseg7_0.copy()
            else:
                hhmm2 = '{:02d} {:02d}'.format(int(h), int(m))

                pil_image1 = self.cv2pil(self.digital_dseg7_0)
                pil_image2 = self.cv2pil(self.digital_dseg7_0)
                text_draw1 = ImageDraw.Draw(pil_image1)
                text_draw1.text((int(width*0.56),int(height*0.08)), ymd, font=self.font32_dseg7, fill=(0,223,223))
                text_draw1.text((int(width*0.05),int(height*0.25)), hhmm, font=self.font99_dseg7, fill=self.digital_b_tcolor)
                text_draw2 = ImageDraw.Draw(pil_image2)
                text_draw2.text((int(width*0.56),int(height*0.08)), ymd, font=self.font32_dseg7, fill=(0,223,223))
                text_draw2.text((int(width*0.05),int(height*0.25)), hhmm2, font=self.font99_dseg7, fill=self.digital_b_tcolor)
                self.digital_dseg7_0 = self.pil2cv(pil_image1)
                self.digital_dseg7_1 = self.pil2cv(pil_image2)

            # 画像保存　０
            base = self.digital_base        
            over = self.digital_dseg7_0.copy()
            #over = self.digital_dseg7_1.copy()
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            self.digital_image_0 = cv2.add(bg, fg)

            # 画像保存　１
            base = self.digital_base        
            #over = self.digital_dseg7_0.copy()
            over = self.digital_dseg7_1.copy()
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            self.digital_image_1 = cv2.add(bg, fg)

        #----------
        # データ収集
        #----------
        self.update_graphData()

        #----------
        # グラフ作図
        #----------
        if (eyes == True):
            graph_img = self.get_graphImage(width=width, height=height, s=s, )

        #----------
        # 目ん玉
        #----------
        if (eyes == True):
            eyes_image = self.get_eyesImage(width=width, height=height, sg_left2=sg_left2, sg_top2=sg_top2, sg_width=sg_width, sg_height=sg_height, )

        #----------
        # 画像合成
        #----------
        if ((s % 2) == 1) or (eyes == True):
            img = self.digital_image_1.copy()
        else:
            img = self.digital_image_0.copy()

        # 目ん玉合成
        if (eyes == True):
            img =  self.get_overlayImage(img=img, graph_img=graph_img, eyes_image=eyes_image, )

        # 秒針
        w = int(width * (s/59))
        if (eyes != True):
            cv2.rectangle(img,(width-w,0),(width,5),(0,0,255),thickness=-1,)
        else:
            cv2.rectangle(img,(width-w,0),(width,5),(255,255,0),thickness=-1,)

        return img



    def getImage_analog(self, dt_now, design=0, eyes=True, sg_left2=0, sg_top2=0, sg_width=320, sg_height=240, ):
        self.last_icon = None

        yy = dt_now.year
        mm = dt_now.month
        dd = dt_now.day
        h = dt_now.hour
        m = dt_now.minute
        s = dt_now.second

        m = m + s/60
        h = h + m/60

        width  = self.analog_width
        height = self.analog_height

        #----------
        # デジタル
        #----------
        if (self.font32_dseg7 is None):
            ymd  = '{:04d}. {:02d}. {:02d}.'.format(yy, mm, dd)
        else:
            ymd  = '{:04d}.    {:02d}.    {:02d}.'.format(yy, mm, dd)
        hhmm = '{:02d}:{:02d}'.format(int(h), int(m))
        if (hhmm != self.last_hhmm):
            self.last_hhmm = hhmm
            
            width  = self.analog_width
            height = self.analog_height
            self.analog_dseg7_0 = np.zeros((height,width,3), np.uint8)
            if (self.font32_dseg7 is None):
                cv2.putText(self.analog_dseg7_0, ymd, (int(width*0.27),int(height*0.33)), cv2.FONT_HERSHEY_TRIPLEX, 2, (223,223,0))
                cv2.putText(self.analog_dseg7_0, hhmm, (int(width*0.2),int(height*0.7)), cv2.FONT_HERSHEY_TRIPLEX, 5, (255,0,255))
                self.analog_dseg7_1 = self.analog_dseg7_0.copy()
            else:
                if ((design % 2) == 0):
                    hhmm2 = '{:02d} {:02d}'.format(int(h), int(m))
                    pil_image1 = self.cv2pil(self.analog_dseg7_0)
                    pil_image2 = self.cv2pil(self.analog_dseg7_0)
                    text_draw1 = ImageDraw.Draw(pil_image1)
                    text_draw1.text((int(width*0.34),int(height*0.30)), ymd, font=self.font32_dseg7, fill=(0,223,223))
                    text_draw1.text((int(width*0.06),int(height*0.6)), hhmm, font=self.font99_dseg7, fill=self.analog_b_tcolor)
                    text_draw2 = ImageDraw.Draw(pil_image2)
                    text_draw2.text((int(width*0.34),int(height*0.30)), ymd, font=self.font32_dseg7, fill=(0,223,223))
                    text_draw2.text((int(width*0.06),int(height*0.6)), hhmm2, font=self.font99_dseg7, fill=self.analog_b_tcolor)
                    self.analog_dseg7_0 = self.pil2cv(pil_image1)
                    self.analog_dseg7_1 = self.pil2cv(pil_image2)
                else:
                    hh = '{:02d}'.format(int(h))
                    mm = '{:02d}'.format(int(m))
                    pil_image = self.cv2pil(self.analog_dseg7_0)
                    text_draw = ImageDraw.Draw(pil_image)
                    text_draw.text((int(width*0.65),int(height*0.02)), ymd, font=self.font32_dseg7, fill=(0,223,223))
                    text_draw.text((int(width*0.05),int(height*0.08)), hh, font=self.font88_dseg7, fill=self.analog_b_tcolor)
                    text_draw.text((int(width*0.35),int(height*0.53)), mm, font=self.font88_dseg7, fill=self.analog_b_tcolor)
                    self.analog_dseg7_0 = self.pil2cv(pil_image)
                    self.analog_dseg7_1 = self.analog_dseg7_0.copy()

        #----------
        # データ収集
        #----------
        self.update_graphData()

        #----------
        # グラフ作図
        #----------
        if (eyes == True):
            graph_img = self.get_graphImage(width=width, height=height, s=s, )

        #----------
        # 目ん玉
        #----------
        if (eyes == True):
            eyes_image = self.get_eyesImage(width=width, height=height, sg_left2=sg_left2, sg_top2=sg_top2, sg_width=sg_width, sg_height=sg_height, )

        # 文字 2 パターン
        # 盤 3 パターン
        # 素数 5 目盛
        # 素数 7 パイ配色
        # 素数 11 目盛文字

        #----------
        # 表示板リセット
        #----------
        if (h != self.ax_last_hh):
            plt.cla()
            plt.clf()
            plt.close()

            plt.cla()
            plt.style.use(self.analog_pltStyle)
            self.fig = plt.figure(figsize=(10,10))
            self.ax = self.fig.add_subplot(111)
            self.ax.set_xlim(-1.05,1.05)
            self.ax.set_ylim(-1.05,1.05)
            self.ax.axis('off')
            self.ax_last_hh = h

        #----------
        # パイ盤 0,1
        #----------
        if ((design % 3) == 0) \
        or ((design % 3) == 1):
            plt.cla()
            # 外周
            vals = np.array([100,])
            colors = [self.analog_b_bcolor,]
            self.ax.pie(vals,colors=colors,counterclock=False, startangle=90, radius=1, wedgeprops=dict(width=0.02), )
            # 色
            if ((design % 3) == 1) \
            or ((design % 7) == 4):
                s_colors = [self.analog_s_bcolor2, self.analog_s_bcolor1,]
                m_colors = [self.analog_m_bcolor2, self.analog_m_bcolor1,]
                h_colors = [self.analog_h_bcolor2, self.analog_h_bcolor1,]
            else:
                s_colors = [self.analog_s_bcolor1, self.analog_b_bcolor,]
                m_colors = [self.analog_m_bcolor1, self.analog_b_bcolor,]
                h_colors = [self.analog_h_bcolor1, self.analog_b_bcolor,]
            # 秒
            vals = np.array([s/60, 1-s/60,])
            self.ax.pie(vals,colors=s_colors,counterclock=False, startangle=90, radius=0.85, wedgeprops=dict(width=0.2), )
            # 分
            vals = np.array([m/60, 1-m/60,])
            self.ax.pie(vals,colors=m_colors,counterclock=False, startangle=90, radius=0.60, wedgeprops=dict(width=0.2), )
            # 時
            vals = np.array([(h % 12)/12, 1-(h % 12)/12,])
            self.ax.pie(vals,colors=h_colors,counterclock=False, startangle=90, radius=0.35, wedgeprops=dict(width=0.2), )
            # 目盛
            if ((design % 11) != 1):
                for t in range(1,13):
                    if ((t % 3)==0):
                        t_x = np.sin(np.radians((t % 12)/12*360)) * 0.75
                        t_y = np.cos(np.radians((t % 12)/12*360)) * 0.75
                        self.ax.text(t_x, t_y, str(t), color=self.analog_b_fcolor, ha='center', va='center', size=64, )
            # 画像保存
            buf = io.BytesIO()
            self.fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, )
            enc = np.frombuffer(buf.getvalue(), dtype=np.uint8)
            img_pie = cv2.imdecode(enc, 1)
            # サイズ調整
            if (img_pie.shape) != (self.analog_base.shape):
                img_pie = cv2.resize(img_pie, (self.analog_width, self.analog_height))
            #plt.show()

        #----------
        # 画像合成
        #----------
        if ((design % 3) == 1):

            if ((design % 5) == 1):
                base = img_pie.copy()
            else:
                base = img_pie
                over = self.analog_base        
                # 表側でマスク作成
                gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)    
                # 表側,裏側,合成
                fg = cv2.bitwise_and(over, over, mask = mask)
                bg = cv2.bitwise_and(base, base, mask = mask_inv)
                base = cv2.add(bg, fg)

            if ((s % 2) == 0):
                over = self.analog_dseg7_0
            else:
                over = self.analog_dseg7_1
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            img = cv2.add(bg, fg)

            # 目ん玉合成
            if (eyes == True):
                img =  self.get_overlayImage(img=img, graph_img=graph_img, eyes_image=eyes_image, )

            return img

        #----------
        # アナログ盤 0,2
        #----------
        if ((design % 3) == 0) \
        or ((design % 3) == 2):
            plt.cla()
            # 外周
            vals = np.array([100,])
            colors = [self.analog_b_bcolor,]
            self.ax.pie(vals,colors=colors,counterclock=False, startangle=90, radius=1, wedgeprops=dict(width=0.02), )
            # 目盛
            if ((design % 11) != 1):
                for t in range(1,13):
                    if ((t % 3)==0):
                        t_x = np.sin(np.radians((t % 12)/12*360)) * 0.75
                        t_y = np.cos(np.radians((t % 12)/12*360)) * 0.75
                        self.ax.text(t_x, t_y, str(t), color=self.analog_b_fcolor, ha='center', va='center', size=64, )
            # 時針
            h_x = np.sin(np.radians((h % 12)/12*360)) * 0.55
            h_y = np.cos(np.radians((h % 12)/12*360)) * 0.55
            self.ax.plot([0,h_x], [0,h_y], color=self.analog_h_fcolor, lw=32, zorder=99, )
            # 分針
            m_x = np.sin(np.radians(m/60*360)) * 0.80
            m_y = np.cos(np.radians(m/60*360)) * 0.80
            self.ax.plot([0,m_x], [0,m_y], color=self.analog_m_fcolor, lw=16, zorder=99, )
            # 秒針
            s_x = np.sin(np.radians(s/60*360)) * 0.85
            s_y = np.cos(np.radians(s/60*360)) * 0.85
            self.ax.plot([0,s_x], [0,s_y], color=self.analog_s_fcolor, lw=8, zorder=99, )
            # 画像保存
            buf = io.BytesIO()
            self.fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, )
            enc = np.frombuffer(buf.getvalue(), dtype=np.uint8)
            img_line = cv2.imdecode(enc, 1)
            # サイズ調整
            if (img_line.shape) != (self.analog_base.shape):
                img_line = cv2.resize(img_line, (self.analog_width, self.analog_height))
            #plt.show()

        #----------
        # 画像合成
        #----------
        if ((design % 3) == 2):

            if ((design % 5) == 1):
                if ((s % 2) == 0):
                    base = self.analog_dseg7_0.copy()
                else:
                    base = self.analog_dseg7_1.copy()
            else:
                base = self.analog_base
                if ((s % 2) == 0):
                    over = self.analog_dseg7_0
                else:
                    over = self.analog_dseg7_1
                # 表側でマスク作成
                gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)    
                # 表側,裏側,合成
                fg = cv2.bitwise_and(over, over, mask = mask)
                bg = cv2.bitwise_and(base, base, mask = mask_inv)
                base = cv2.add(bg, fg)

            over = img_line
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            img = cv2.add(bg, fg)

            # 目ん玉合成
            if (eyes == True):
                img =  self.get_overlayImage(img=img, graph_img=graph_img, eyes_image=eyes_image, )

            return img

        #----------
        # 画像合成
        #----------
        if True:
            base = img_pie
            if ((s % 2) == 0):
                over = self.analog_dseg7_0
            else:
                over = self.analog_dseg7_1
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            base = cv2.add(bg, fg)

            if ((design % 5) != 1):
                over = self.analog_base
                # 表側でマスク作成
                gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)    
                # 表側,裏側,合成
                fg = cv2.bitwise_and(over, over, mask = mask)
                bg = cv2.bitwise_and(base, base, mask = mask_inv)
                base = cv2.add(bg, fg)

            over = img_line
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            img = cv2.add(bg, fg)

        # 目ん玉合成
        if (eyes == True):
            img =  self.get_overlayImage(img=img, graph_img=graph_img, eyes_image=eyes_image, )

        return img



    def timeSign_info(self, h, m, ):
        result  = str(h) + '時'
        result += str(m) + '分'

        # 情報通知
        if (result != ''):
            title = '【時報】'
            txt   = result
            #print(title, txt)
            qLog.log('info', self.proc_id, title + result, )

            if (self.timeSign_sound != ''):
                if (os.path.isfile(self.timeSign_sound)):
                    self.batch_play(sounds_file = self.timeSign_sound)

            if (self.timeSign_telop != 'no') and (self.timeSign_telop != 'off'):
                if (m==0):
                    self.telopMSG(title=title, txt= 'ただ今、' + str(h) + '時をお知らせします。', )
                else:
                    self.telopMSG(title=title, txt= 'ただ今の時間、' + str(h) + '時' + str(m) + '分です。', )

            if (self.timeSign_tts != 'no') and (self.timeSign_tts != 'off'):
                if (m==0):
                    self.ttsMSG(title='ただ今、', txt= str(h) + '時をお知らせします。', )
                else:
                    self.ttsMSG(title='ただ今の時間、', txt=str(h) + '時' + str(m) + '分です。', )

        return result

    # cpuClock,saap_worker 同一ロジック
    def telopMSG(self, title='Message', txt='', ):
        if (txt == ''):
            return False
        if (self.telop_path == ''):
            return False
        if (not os.path.isdir(self.telop_path)):
            return False
        if (title.find('【') < 0):
            title = '【' + title + '】'
        txt = title + '\r\n' + txt

        now   = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d%H%M%S')
        self.file_seq += 1
        if (self.file_seq > 9999):
            self.file_seq = 1
        seq4 = '{:04}'.format(self.file_seq)

        filename = self.telop_path + stamp + '.' + seq4 + '.txt'

        res = qFunc.txtsWrite(filename, txts=[txt], mode='w', exclusive=True, )
        if (res == False):
            qLog.log('critical', self.proc_id, '★Telop書込エラー', )
            return False        

        return True        

    # cpuClock,saap_worker 同一ロジック
    def ttsMSG(self, title='Message', txt='', ):
        if (txt == ''):
            return False
        if (self.tts_path == ''):
            return False
        if (not os.path.isdir(self.tts_path)):
            return False
        txt = txt.replace('\r',' ')
        txt = txt.replace('\n',' ')
        txt = txt.replace('／','/')
        txt = txt.replace('/','スラッシュ')

        now   = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d%H%M%S')
        self.file_seq += 1
        if (self.file_seq > 9999):
            self.file_seq = 1
        seq4 = '{:04}'.format(self.file_seq)

        filename = self.tts_path + stamp + '.' + seq4 + '.txt'

        # 個人利用時のWINOSは、直接発声！
        #if  (self.runMode == 'personal') \
        #and (self.tts_header == 'ja,winos,') \
        #and (os.name == 'nt'):

        #    winosAPI = winos_api.SpeechAPI()
        #    res = winosAPI.authenticate()
        #    if (res == False):
        #        qLog.log('critical', self.proc_id, '★winosAPI(speech)認証エラー', )
        #        return False        

        #    try:
        #        filename = filename[:-4] + '.mp3'
        #        res, api = winosAPI.vocalize(outText=txt, outLang='ja', outFile=filename, )
        #        if (res != ''):

        #            sox = subprocess.Popen(['sox', filename, '-d', '-q'], )
        #            #sox.wait()
        #            #sox.terminate()
        #            #sox = None

        #    except:
        #        qLog.log('critical', self.proc_id, '★winosAPI(speech)利用エラー', )
        #        return False

        #else:
        if True:

            txt = self.tts_header + txt
            res = qFunc.txtsWrite(filename, txts=[txt], mode='w', exclusive=True, )
            if (res == False):
                qLog.log('critical', self.proc_id, '★TTS書込エラー', )
                return False        

        return True



if __name__ == '__main__':

    proc = _proc()

    proc.init(qLog_fn='', runMode='debug',  )



