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

import json

import queue

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import numpy as np
import cv2

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



class _gui:

    def __init__(self, ):
        self.screen         = '0'
        self.panel          = '3--'

        self.img_file       = '_icons/RiKi_cpuClock24.png'

        titlex              = os.path.basename(__file__)
        self.title          = titlex.replace('.py','')

        self.theme          = 'Dark' # 'Default1', 'Dark',
        self.alpha_channel  = 1.0
        self.icon           = None
        self.font           = ('Arial', 8)

        self.keep_on_top    = True
        self.no_titlebar    = False
        self.disable_close  = False
        self.resizable      = True
        self.no_border      = True

        self.window         = None
        self.left           = 0
        self.top            = 0
        self.width          = 320
        self.height         = 240

        # tkinter
        self.image_label        = None
        self.event_queue        = queue.Queue()
        self.tk_image           = None
        self.default_img        = None
        self.last_resize_w      = 0
        self.last_resize_h      = 0
        self.last_afc_reset     = time.time()
        self.last_afc_mouse_x   = 0
        self.last_afc_mouse_y   = 0
        self.last_afc_window_l  = 0
        self.last_afc_window_t  = 0
        self.last_afc_window_w  = 0
        self.last_afc_window_h  = 0

    def init(self, qLog_fn='', runMode='debug',
             screen='auto', panel='auto',
             title='', theme=None,
             keep_on_top='yes', alpha_channel='1', icon=None, ):

        # ログ
        self.proc_name = 'gui'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')

        # 実行モード
        self.runMode = runMode

        # スクリーン
        if (str(screen) != 'auto'):
            try:
                self.screen = int(screen)
            except Exception as e:
                print(e)

        # パネル
        if (panel != 'auto'):
            self.panel = panel
        else:
            if   (runMode == 'analog'):
                self.panel         = '36-'
                self.no_titlebar   = True
                self.disable_close = True
            elif (runMode == 'digital'):
                self.panel         = '3-'
                self.no_titlebar   = True
                self.disable_close = True
            elif (runMode == 'personal'):
                self.panel         = '3--'
            else:
                self.panel         = '3'

        qLog.log('info', self.proc_id, 'screen = ' + str(self.screen))
        qLog.log('info', self.proc_id, 'panel  = ' + str(self.panel ))

        # タイトル
        if (title != ''):
            self.title  = title
        else:
            titlex      = os.path.basename(__file__)
            titlex      = titlex.replace('.py','')
            self.title  = titlex + '[' + runMode + ']'

        # テーマ
        if (theme is not None):
            self.theme = theme
        #sg.theme(self.theme)
        # ボーダー
        if (self.no_border != True):
            self.element_padding= ((2,2),(2,2)) #((left/right),(top/bottom))
        else:
            self.element_padding= ((0,0),(0,0)) #((left/right),(top/bottom))
            #sg.set_options(element_padding=(0,0), margins=(0,0), border_width=0)

        # 最前面
        if (keep_on_top != 'no'):
            self.keep_on_top = True
        else:
            self.keep_on_top = False

        # 透過表示
        if (str(alpha_channel) != ''):
            try:
                self.alpha_channel = float(alpha_channel)
            except Exception as e:
                print(e)

        # アイコン
        if (icon is not None):
            self.icon = icon

        # 表示位置
        qGUI.checkUpdateScreenInfo(update=True, )
        self.left, self.top, self.width, self.height = qGUI.getScreenPanelPosSize(screen=self.screen, panel=self.panel, )

        # ウィンドウ設定
        if self.window is not None:
            self.terminate()
        try:
            self.window = tk.Tk()
            self.window.attributes("-alpha", 0)
            self.window.update_idletasks()
            self.window.title(self.title)

            if icon is not None and os.path.isfile(icon):
                self.window.iconbitmap(icon)

            geometry_str = f"{self.width}x{self.height}{self.left :+}{self.top :+}"
            self.window.geometry(geometry_str)
            self.window.wm_attributes("-topmost", True if keep_on_top != 'no' else False)
            self.window.resizable(self.resizable, self.resizable)
            if self.no_titlebar:
                self.window.overrideredirect(True)
            self.image_label = tk.Label(self.window)
            self.image_label.pack(fill="both", expand=True)
            self.image_label.bind("<Button-1>", self.handle_img_click)
            self.window.protocol("WM_DELETE_WINDOW", self.on_close)
            self.default_img = np.zeros((self.height, self.width, 3), np.uint8)
            cv2.rectangle(self.default_img, (0, 0), (self.width, self.height), (255, 0, 0), -1)
            self.window.geometry(geometry_str)
            self.window.attributes("-alpha", self.alpha_channel)
            self.reset()
        except Exception as e:
            print(e)
            self.window = None

        if (self.window is not None):
            return True
        else:
            return False

    def handle_img_click(self, event):
        self.event_queue.put("_output_img_")

    def on_close(self):
        self.event_queue.put("WIN_CLOSED")
        self.terminate()

    def open(self, refresh=True):
        # 更新・表示
        try:
            if self.window is not None:
                self.window.deiconify()
                if refresh:
                    self.refresh()
                return True
        except Exception as e:
            print(e)
        return False

    def read(self, timeout=20, timeout_key='-idoling-', ):
        # 読取
        try:
            start_time = time.time()
            while (time.time() - start_time) * 1000 < timeout:
                try:
                    event = self.event_queue.get_nowait()
                    return event, {}
                except queue.Empty:
                    pass
                self.window.update()
                time.sleep(0.01)
            return timeout_key, {}
        except Exception as e:
            print(e)
        return False, False

    def close(self, ):
        # 消去
        if (self.window is not None):
            try:
                self.window.withdraw()
                self.window.update()
            except Exception as e:
                print(e)
        return True

    def terminate(self, ):
        if self.window is not None:
            try:
                self.window.destroy()
            except Exception as e:
                print(e)
        self.window = None
        return True

    # GUI 画面リセット
    def reset(self):
        try:
            w = self.window.winfo_width()
            h = self.window.winfo_height()
        except:
            return False

        # 規定値(イメージ)
        self.default_img = np.zeros((240, 320, 3), np.uint8)
        cv2.rectangle(self.default_img,(0,0),(320,240),(255,0,0),-1)
        try:
            if (os.path.isfile(self.img_file)):
                self.default_img = cv2.imread(self.img_file)
        except:
            pass

        # 項目リセット
        self.setImage(self.default_img, refresh=False)
        return True

    # GUI 画面リサイズ
    def resize(self, reset=False, ):
        try:
            w = self.window.winfo_width()
            h = self.window.winfo_height()
        except:
            return False

        # リセット
        if (reset == True):
            self.last_resize_w, self.last_resize_h = 0, 0

        # 画面リサイズ？
        if (w != self.last_resize_w) or (h != self.last_resize_h):
            self.last_resize_w, self.last_resize_h = w, h

            # 項目リセット
            self.setImage(self.default_img, refresh=True)

        return True

    # GUI 画面更新
    def refresh(self):
        try:
            self.window.update_idletasks()
            return True
        except Exception as e:
            print(e)
        return False    

    # 画像セット
    def setImage(self, image=None, refresh=True, ):
        try:
            w = self.window.winfo_width()
            h = self.window.winfo_height()
        except:
            return False

        if (image is None):
            img = np.zeros((h, w, 3), np.uint8)
        else:
            img = cv2.resize(image, (w, h))

        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(img_rgb)
            self.tk_image = ImageTk.PhotoImage(im)
            self.image_label.config(image=self.tk_image)
            if refresh:
                self.refresh()
            return True
        except Exception as e:
            print(e)
        return False

    # GUI 自動フェード
    def autoFadeControl(self, reset=False, intervalSec=60, fadeSec=10, ):
        try:

            # 透過率設定時に処理
            if (self.alpha_channel < 1):

                # リセット
                if (reset == True):
                    self.window.attributes("-alpha", 1.0)
                    self.last_afc_reset = time.time()

                    # マウス位置
                    (x, y) = qGUI.position()
                    self.last_afc_mouse_x, self.last_afc_mouse_y = x, y

                    # ウィンドウ位置、大きさ
                    self.last_afc_window_l = self.window.winfo_x()
                    self.last_afc_window_t = self.window.winfo_y()
                    self.last_afc_window_w = self.window.winfo_width()
                    self.last_afc_window_h = self.window.winfo_height()

                    return True

                # マウス位置変化？
                (x, y) = qGUI.position()
                if (x != self.last_afc_mouse_x) or (y != self.last_afc_mouse_y):
                    self.last_afc_mouse_x, self.last_afc_mouse_y = x, y

                    # ウィンドウ位置、大きさ変化？
                    l = self.window.winfo_x()
                    t = self.window.winfo_y()
                    w = self.window.winfo_width()
                    h = self.window.winfo_height()
                    if (l != self.last_afc_window_l) or (t != self.last_afc_window_t) \
                    or (w != self.last_afc_window_w) or (h != self.last_afc_window_h):
                        self.last_afc_window_l, self.last_afc_window_t = l, t
                        self.last_afc_window_w, self.last_afc_window_h = w, h
                        self.window.attributes("-alpha", 1.0)
                        self.last_afc_reset = time.time()
                        return True

                    # マウスオーバーでリセット
                    if (x >= l) and (x <= (l+w)) and (y >= t) and (y <= (t+h)):
                        self.window.attributes("-alpha", 1.0)
                        self.last_afc_reset = time.time()
                        return True

                # フェード処理
                sec = (time.time() - self.last_afc_reset)
                if (sec < (intervalSec + fadeSec)):
                    v = 1 - float(self.alpha_channel)
                    p = (sec - intervalSec) / fadeSec
                    if (p <= 0):
                        self.window.attributes("-alpha", 1.0)
                    else:
                        # フェードアウト
                        if (p > 1):
                            p = 1
                        alpha = 1 - v * p
                        self.window.attributes("-alpha", alpha)

            return True
        except:
            pass
        return False



runMode = 'debug'

if __name__ == '__main__':

    gui = _gui()

    # 初期設定
    if (True):

        # タイトル、icon
        titlex = os.path.basename(__file__)
        titlex = titlex.replace('.py','')
        title  = titlex + '[' + runMode + ']'
        #icon  = None
        icon   = './_icons/' + titlex + '.ico'

        # GUI 初期化
        gui.init(qLog_fn='', runMode='debug',
                 screen='auto', panel='auto',
                 title=title, theme=None,
                 keep_on_top='yes', alpha_channel='0.2', icon=icon, )


    # GUI 表示ループ
    reset_flag   = True
    refresh_flag = True
    break_flag   = False
    values       = None
    while (break_flag == False):

        # GUI リセット
        if (reset_flag == True):
            reset_flag   = False
            refresh_flag = True

            # GUI 画面リセット
            gui.reset()

            # GUI 自動フェードリセット
            gui.autoFadeControl(reset=True, )

            # GUI 画面リサイズリセット
            gui.resize(reset=True, )

        # GUI 自動フェード
        gui.autoFadeControl(reset=False, )

        # GUI 画面リサイズ
        gui.resize(reset=False, )

        # GUI 画面更新
        if (refresh_flag == True):
            refresh_flag = False
            gui.refresh()
        # GUI イベント確認                 ↓　timeout値でtime.sleep代用
        event, values = gui.read(timeout=150, timeout_key='-idoling-')

        # GUI 終了イベント処理
        if event == "WIN_CLOSED":
            gui.window = None
            break_flag = True
            break
        if event in (None, '-exit-'):
            break_flag = True
            break

        try:
            # ------------------------------
            # アイドリング時の処理
            # ------------------------------
            if (event == '-idoling-'):
                pass

            # ------------------------------
            # ボタンイベント処理
            # ------------------------------
            # リセット
            elif (event == '-reset-'):
                print(event, )
                reset_flag = True

            else:
                print(event, values, )
        except Exception as e:
            print(e)
            time.sleep(5.00)

    # 終了処理
    if (True):

        # GUI 画面消去
        try:
            gui.close()
            gui.terminate()
        except:
            pass

        # 終了
        sys.exit(0)


