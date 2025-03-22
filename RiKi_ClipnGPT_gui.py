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

#import PySimpleGUI_key
#PySimpleGUI_License=PySimpleGUI_key.PySimpleGUI_License
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont

import numpy as np
import cv2

from io import BytesIO

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
        self.panel          = '5+'

        titlex              = os.path.basename(__file__)
        self.title          = titlex.replace('.py','')
        self.layout         = [
                            sg.InputText('Hallo World'),
                            sg.Button('OK', key='-OK-'),
                            ]

        self.theme          = 'Dark' # 'Default1', 'Dark',
        self.alpha_channel  = 1.0
        self.icon           = None
        self.font           = 'Arial 8'

        self.keep_on_top    = True
        self.no_titlebar    = False
        self.disable_close  = False
        self.resizable      = True
        self.no_border      = False

        self.window         = None
        self.left           = 0
        self.top            = 0
        self.width          = 320
        self.height         = 240

        self.check_box      = [self.check_icon(0), self.check_icon(1), self.check_icon(2)]



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
        sg.theme(self.theme)

        # ボーダー
        if (self.no_border != True):
            self.element_padding= ((2,2),(2,2)) #((left/right),(top/bottom))
        else:
            self.element_padding= ((0,0),(0,0)) #((left/right),(top/bottom))
            sg.set_options(element_padding=(0,0), margins=(0,0), border_width=0)

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

        # レイアウト
        self.setLayout()

        # ウィンドウ設定
        self.close()
        try:
            if (sys.platform == 'darwin'): # MacOS チャック
                self.no_titlebar = False
            if (self.no_titlebar == True):
                self.window = sg.Window(self.title, self.layout,
                            keep_on_top=self.keep_on_top,
                            font=self.font,
                            element_padding=self.element_padding,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=True,
                            disable_close=self.disable_close,
                            default_element_size=(12, 1),
                            default_button_element_size=(15, 1),
                            return_keyboard_events=False, #Danger!
                            alpha_channel=self.alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width, self.height),
                            resizable=self.resizable,
                            icon=self.icon, )
            else:
                self.window = sg.Window(self.title, self.layout,
                            keep_on_top=self.keep_on_top,
                            font=self.font,
                            element_padding=self.element_padding,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=False,
                            disable_close=self.disable_close,
                            default_element_size=(12, 1),
                            default_button_element_size=(15, 1),
                            return_keyboard_events=False, #Danger!
                            alpha_channel=self.alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width, self.height),
                            resizable=self.resizable,
                            icon=self.icon, )

        except Exception as e:
            print(e)
            self.window = None

        if (self.window is not None):
            return True
        else:
            return False

    def bind(self, ):
        self.window['_input_text_'].bind('<Double-Button-1>', ' double')
        self.window['_output_text_'].bind('<Double-Button-1>', ' double')
        self.window['_proc_text_'].bind('<Double-Button-1>', ' double')
        self.window['_history_list_'].bind('<Double-Button-1>', ' double')
        self.window['_addin_tree_'].Widget.heading("#0", text=self.addin_header[0])
        self.window['_function_tree_'].Widget.heading("#0", text=self.func_header[0])
        self.window['_sendfile_tree_'].Widget.heading("#0", text=self.send_header[0])
        return True

    def open(self, refresh=True, ):
        # 更新・表示
        try:
            if (self.window is not None):
                self.window.un_hide()
                if (refresh == True):
                    self.window.refresh()
                return True
        except Exception as e:
            print(e)
        return False

    def read(self, timeout=20, timeout_key='-timeout-', ):
        # 読取
        try:
            if (self.window is not None):
                event, values = self.window.read(timeout=timeout, timeout_key=timeout_key, )
                return event, values
        except Exception as e:
            print(e)
        return False, False

    def close(self, ):
        # 消去
        if (self.window is not None):
            try:
                self.read()
                self.window.hide()
                self.window.refresh()
            except Exception as e:
                print(e)
        return True

    def terminate(self, ):
        # 終了
        if (self.window is not None):
            try:
                self.read()
                self.window.close()
                del self.window
            except Exception as e:
                print(e)
        self.window = None
        return True

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

    def pil2guiImage(self, pil_image=None):
        try:
            gui_img = self.pil2cv(pil_image=pil_image)
            h, w, _ = gui_img.shape
            if (w > self.gpt_img_xy):
                h = int(h * (self.gpt_img_xy/w))
                w = self.gpt_img_xy
            if (h > self.gpt_img_xy):
                w = int(w * (self.gpt_img_xy/h))
                h = self.gpt_img_xy
            gui_img   = cv2.resize(gui_img, (w,h))
            png_bytes = cv2.imencode('.png', gui_img)[1].tobytes()
            self.window['_input_img_'].update(data=png_bytes)
            return True
        except:
            pass
        return False

    def hex2(self, num): # 10進数を二桁16進文字列に変換
        num2 = hex(num).replace('0x', '')
        if len(num2) == 1:
            num2 = '0' + num2
        return num2

    def rgb2hex(self, r, g, b): # r,g,b数を16進カラーコード文字列に変換
        color_code = '#' + '{}{}{}'.format(self.hex2(r), self.hex2(g), self.hex2(b))
        return color_code

    # GUI 自動フェード
    def autoFadeControl(self, reset=False, intervalSec=60, fadeSec=10, ):

        # 透過率設定時に処理
        if (self.alpha_channel < 1):

            # リセット
            if (reset == True):
                self.window.alpha_channel = 1
                self.last_afc_reset = time.time()

                # マウス位置
                (x, y) = qGUI.position()
                self.last_afc_mouse_x, self.last_afc_mouse_y = x, y

                # ウィンドウ位置、大きさ
                (l, t) = self.window.current_location()
                (w, h) = self.window.size
                self.last_afc_window_l, self.last_afc_window_t = l, t
                self.last_afc_window_w, self.last_afc_window_h = w, h

                return True

            # マウス位置変化？
            (x, y) = qGUI.position()
            if (x != self.last_afc_mouse_x) or (y != self.last_afc_mouse_y):
                self.last_afc_mouse_x, self.last_afc_mouse_y = x, y

                # ウィンドウ位置、大きさ変化？
                (l, t) = self.window.current_location()
                (w, h) = self.window.size
                if (l != self.last_afc_window_l) or (t != self.last_afc_window_t) \
                or (w != self.last_afc_window_w) or (h != self.last_afc_window_h):
                    self.last_afc_window_l, self.last_afc_window_t = l, t
                    self.last_afc_window_w, self.last_afc_window_h = w, h
                    self.window.alpha_channel = 1
                    self.last_afc_reset = time.time()
                    return True

                # マウスオーバーでリセット
                if (x >= l) and (x <= (l+w)) and (y >= t) and (y <= (t+h)):
                    self.window.alpha_channel = 1
                    self.last_afc_reset = time.time()
                    return True

            # フェード処理
            sec = (time.time() - self.last_afc_reset)
            if (sec < (intervalSec + fadeSec)):
                v = 1 - float(self.alpha_channel)
                p = (sec - intervalSec) / fadeSec
                if (p <= 0):
                    self.window.alpha_channel = 1
                else:
                    # フェードアウト
                    if (p > 1):
                        p = 1
                    alpha = 1 - v * p
                    self.window.alpha_channel = alpha

        return True

    def check_icon(self, check):
        box = (24, 24)
        background = (255, 255, 255, 0)
        rectangle = (3, 3, 21, 21)
        line = ((6, 12), (12, 18), (18, 6))
        im = Image.new('RGBA', box, background)
        draw = ImageDraw.Draw(im, 'RGBA')
        draw.rectangle(rectangle, outline='gray', width=3)
        if   (check == 1):
            draw.line(line, fill='gray', width=2, joint='curve')
        elif (check == 2):
            draw.line(line, fill='gray', width=2, joint='curve')
        with BytesIO() as output:
            im.save(output, format="PNG")
            png = output.getvalue()
        return png

    def get_sg_TreeData(self, ):
        return sg.TreeData()

    def setLayout(self, ):

        # 設定
        if (os.name == 'nt'):
            col_size = 50
            check_size = 12
            label_size = 15
        else:
            col_size = 50
            check_size = 15
            label_size = 15

        menu_def = [
                    ['&File', ['&Open', '&Save', '&Quit'], ],
                    ['&Help', ['&About...'], ],
                   ]

        # レイアウト 1
        layout1 = [

                # 内容
                [sg.Frame(layout=[
                    [sg.Checkbox('Auto from Clip', default=True, key='_check_fromClip_', enable_events=True, size=(check_size,1)),
                     sg.Checkbox('File Parser', default=True, key='_check_fileParser_', enable_events=True, size=(check_size,1)),
                     sg.Checkbox('Pdf Parser', default=True, key='_check_pdfParser_', enable_events=True, size=(check_size,1)),
                     sg.Checkbox('Html Parser', default=True, key='_check_htmlParser_', enable_events=True, size=(check_size,1)),
                     sg.Checkbox('Image OCR', default=False, key='_check_imageOCR_', enable_events=True, size=(check_size,1)),
                     sg.Button('exec Parser', key='-exec-parser-', visible=False, button_color=('white', 'blue'), )],
                    [sg.Text('Input Path', justification='right', size=(label_size,None)),
                     sg.InputText('', key='_input_path_', enable_events=True, size=(col_size,None)),
                     sg.Button('Open Path', key='-open-path-', button_color=('white', 'blue'), )],
                ], title='[ Input ]', key='_frame_input_', )],

                [sg.Frame(layout=[
                    [sg.Checkbox('Auto GPT', key='_check_toGPT_', enable_events=True, size=(check_size,1)),
                     sg.Button('exec GPT', key='-exec-toGPT-', button_color=('white', 'blue'), ),
                     sg.Checkbox('Auto STT', key='_check_fromSpeech_', visible=False, enable_events=True, size=(check_size,1)),
                     sg.Checkbox('use Functions', default=True, key='_check_useFunctions_', visible=False, enable_events=True, size=(check_size,1)),
                     sg.Button('Reset / Clear', key='-reset-', visible=False, button_color=('white', 'red'), )],
                    [sg.Text('Role', justification='right', size=(label_size,None)),
                     sg.InputText('', key='_role_text_', enable_events=True, size=(col_size,None))],
                    [sg.Text('Request', justification='right', size=(label_size,None)),
                     sg.Multiline('', key='_req_text_', enable_events=True, size=(col_size,2))],
                    [sg.Text('Input Text', justification='right', size=(label_size,None)),
                     sg.Multiline('', key='_input_text_', enable_events=True, size=(col_size,2))],
                ], title='[ GPT ]', key='_frame_gpt_', visible=True, ),
                     sg.Image(filename='', key='_input_img_', ),
                ],

                [sg.Frame(layout=[
                    [sg.Checkbox('Auto to Clip', key='_check_toClip_', enable_events=True, size=(check_size,1)),
                     sg.Button('to Clip', key='-exec-toClip-', button_color=('white', 'blue'), ),
                     sg.Checkbox('Auto TTS', key='_check_toSpeech_', visible=False, enable_events=True, size=(check_size,1)),
                     sg.Button('to Speech', key='-exec-toSpeech-', visible=False, button_color=('white', 'blue'), ), ],
                    [sg.Text('Output Text', justification='right', size=(label_size,None)),
                     sg.Multiline('output text...', key='_output_text_', enable_events=True, size=(col_size,50)), ],
                ], title='[ Output ]', key='_frame_output_', )],

        ]

        # レイアウト 2
        layout2 = [

                # 内容
                [sg.Frame(layout=[
                    [sg.Checkbox('OpenAI/Azure', key='_check_openai_', default=True, enable_events=True, size=(check_size,1)),
                     sg.Checkbox('FreeAI', key='_check_freeai_', default=True, enable_events=True, size=(check_size,1)),
                     sg.Checkbox('Ollama', key='_check_ollama_', default=True, enable_events=True, size=(check_size,1)), ],
                ], title='[ LLMs ]', key='_frame_llms_', ),
                sg.Frame(layout=[
                    [sg.Checkbox('AutoUpload', key='_check_autoUpload_', default=True, enable_events=True, size=(check_size,1)),
                     sg.Checkbox('AutoSandbox', key='_check_autoSandbox_', default=True, enable_events=True, size=(check_size,1)),
                     sg.Checkbox('Debug Mode', key='_check_debugMode_', default=False, enable_events=True, size=(check_size,1)), ],
                ], title='[ Setting ]', key='_frame_setting_', ),                
                ],
                [sg.Frame(layout=[
                    [sg.Button('Clear', key='-clear-', visible=False, button_color=('white', 'red'), ),
                     sg.Button('proc to GPT', key='-proc-toGPT-', button_color=('white', 'blue'), ),
                     sg.Button('to Clip', key='-proc-toClip-', button_color=('white', 'blue'), ),
                     sg.Button('to Speech', key='-proc-toSpeech-', visible=False, button_color=('white', 'blue'), ), ],
                    [sg.Multiline('proc text...', key='_proc_text_', enable_events=True, size=(col_size,50)), ],
                ], title='[ Proc Text ]', key='_frame_proc_', )],

        ]

        # レイアウト 拡張アドイン

        self.addin_header = ['addin_name', 'addin_ver', 'description', ]
        self.addin_tree   = sg.TreeData()

        layout3 = [

                # 内容
                [sg.Frame(layout=[
                    [sg.Tree(data=self.addin_tree,
                             headings=self.addin_header[1:],
                             key='_addin_tree_', 
                             #auto_size_columns=True,
                             auto_size_columns=False,
                             col0_width=40,
                             col_widths=[10, 150], 
                             num_rows=50,
                             row_height=32,
                             justification='left',
                             header_background_color='#cccccc',
                             header_text_color='#0000ff',
                             background_color='#cccccc',
                             text_color='#000000',
                             metadata=[],
                             show_expanded=False,
                             enable_events=True,
                             select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                            )],
                ], title='[ List ]', key='_frame_addins_', )],

        ]

        # レイアウト 拡張ファンクション

        self.func_header = ['func_name', 'func_ver', 'description', ]
        self.func_tree   = sg.TreeData()

        layout4 = [

                # 内容
                [sg.Frame(layout=[
                    [sg.Tree(data=self.func_tree,
                             headings=self.func_header[1:],
                             key='_function_tree_', 
                             #auto_size_columns=True,
                             auto_size_columns=False,
                             col0_width=40,
                             col_widths=[10, 150], 
                             num_rows=50,
                             row_height=32,
                             justification='left',
                             header_background_color='#cccccc',
                             header_text_color='#0000ff',
                             background_color='#cccccc',
                             text_color='#000000',
                             metadata=[],
                             show_expanded=False,
                             enable_events=True,
                             select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                            )],
                ], title='[ List ]', key='_frame_functions_', )],

        ]

        # レイアウト 送信ファイル

        self.send_header = ['send_file', 'time', 'image', ]
        self.send_tree   = sg.TreeData()

        layout5 = [

                # 内容
                [sg.Frame(layout=[
                    [sg.Tree(data=self.send_tree,
                             headings=self.send_header[1:],
                             key='_sendfile_tree_', 
                             #auto_size_columns=True,
                             auto_size_columns=False,
                             col0_width=50,
                             col_widths=[20, 20], 
                             num_rows=50,
                             row_height=32,
                             justification='center',
                             header_background_color='#cccccc',
                             header_text_color='#0000ff',
                             background_color='#cccccc',
                             text_color='#000000',
                             metadata=[],
                             show_expanded=False,
                             enable_events=True,
                             select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                            )],
                ], title='[ List ]', key='_frame_files_', )],

        ]

        # レイアウト 履歴

        # 表
        history_header = ['Seq', 'Time', 'Role', 'Content']
        history_list = [ [1, 1, 'system', 'hallo'], ]

        layout9 = [

                # 内容
                [sg.Frame(layout=[
                    [sg.Table(history_list,
                              headings=history_header,
                              key='_history_list_',
                              #max_col_width=200,
                              #auto_size_columns=True,
                              auto_size_columns=False,
                              col_widths=[4, 8, 20, 150], #char
                              row_height=50, #pix
                              num_rows=50,
                              justification='left',
                              header_background_color='#cccccc',
                              header_text_color='#0000ff',
                              background_color='#cccccc',
                              alternating_row_color='#ffffff',
                              text_color='#000000',
                             )],
                ], title='[ History ]', key='_frame_history_', )],

        ]

        self.layout = [
            # # メニュー・実行状況
            # [sg.Menu(menu_def, tearoff=True)],

            # ステータスバー
            [sg.Text('(queue count)', key='_status_bar_', justification='right', background_color='black', size=(col_size+12,1))],

            # タブ
            [sg.TabGroup([[sg.Tab('【 Main 】', layout1),
                           sg.Tab('【 GPT 】', layout2), 
                           sg.Tab('【 Addins 】', layout3), 
                           sg.Tab('【 Functions 】', layout4), 
                           sg.Tab('【 SendFiles 】', layout5), 
                           sg.Tab('【 History 】', layout9),
                        ]])
            ],

        ]
        return True



    # GUI 画面リセット
    def reset(self, role_text='', req_text='', web_home='', ):
        try:
            (w, h) = self.window.size #表示領域のサイズ
        except:
            return False

        # 規定値(イメージ)
        self.gpt_img_xy = 160
        img = np.zeros((self.gpt_img_xy, self.gpt_img_xy, 3), np.uint8)
        self.gpt_img_null = cv2.imencode('.png', img)[1].tobytes()
        try:
            img = cv2.imread('_icons/RiKi_ClipnGPT.png')
            img = cv2.resize(img, (self.gpt_img_xy, self.gpt_img_xy))
            self.gpt_img_null = cv2.imencode('.png', img)[1].tobytes()
        except:
            pass

        # 規定値(処理中)
        self.gpt_proc_on_bg  = 'red'
        self.gpt_proc_off_bg = 'lightgray'

        # 項目リセット
        self.window['_input_img_'].update(data=self.gpt_img_null)

        if (self.window['_input_path_'].get() == ''):
            self.window['_input_path_'].update(web_home)
        if (self.window['_role_text_'].get() == ''):
            self.window['_role_text_'].update(role_text)
        if (self.window['_req_text_'].get() == ''):
            self.window['_req_text_'].update(req_text)
        #self.window['_input_text_'].update('')
        self.window['_output_text_'].update('')

        self.window['_proc_text_'].update('')
        self.window['_history_list_'].update([])
        #null_data = sg.TreeData()
        #self.window['_addin_tree_'].update(null_data)
        #self.window['_function_tree_'].update(null_data)
        #self.window['_sendfile_tree_'].update(null_data)

        return True

    # GUI 画面リサイズ
    def resize(self, reset=False, ):
        try:
            (w, h) = self.window.size #表示領域のサイズ
        except:
            return False

        # リセット
        if (reset == True):
            self.last_resize_w, self.last_resize_h = 0, 0

        # 画面リサイズ？
        (w, h) = self.window.size
        if (w == self.last_resize_w) and (h == self.last_resize_h):
            return True

        self.last_resize_w, self.last_resize_h = w, h
            
        # 項目サイズ計算
        if (os.name == 'nt'):
            col_size  = int(w / 6) - 25
            if (col_size < 80):
                col_size = 80
            if (h <= 270):
                row_size1, row_size2, row_size3 = 1, 2, 20
            elif (h <= 540):
                row_size1, row_size2, row_size3 = 2, 3, 20
                row_size2 = 3
                row_size3 = 20
            elif (h <= 720):
                row_size1, row_size2, row_size3 = 3, 6, 30
                row_size2 = 6
                row_size3 = 30
            elif (h > 720):
                row_size1, row_size2, row_size3 = 4, 10, 40
        else:
            col_size  = int(w / 5) - 30
            if (col_size < 80):
                col_size = 80
            if (h <= 270):
                row_size1, row_size2, row_size3 = 1, 2, 20
            elif (h <= 540):
                row_size1, row_size2, row_size3 = 2, 3, 20
                row_size2 = 3
                row_size3 = 20
            elif (h <= 720):
                row_size1, row_size2, row_size3 = 3, 6, 30
                row_size2 = 6
                row_size3 = 30
            elif (h > 720):
                row_size1, row_size2, row_size3 = 4, 10, 40

        # 項目サイズ設定
        self.window['_status_bar_'].set_size((col_size+30,None))
        self.window['_input_path_'].set_size((col_size-15,None))
        self.window['_role_text_'].set_size((col_size+2-28,None))
        self.window['_req_text_'].set_size((col_size-28,row_size1))
        self.window['_input_text_'].set_size((col_size-28,row_size2))
        self.window['_output_text_'].set_size((col_size,row_size3))

        self.window['_proc_text_'].set_size((col_size+18,50))
        #self.window['_history_list_'].set_size(???)

        return True

    # GUI 画面更新
    def refresh(self, ):
        try:
            (w, h) = self.window.size #表示領域のサイズ
        except:
            return False

        # 規定値(チェックボックス)
        self.gpt_chk_on_bg  = 'lime'
        self.gpt_chk_on_tc  = 'black'
        self.gpt_chk_off_bg = 'gray'
        self.gpt_chk_off_tc = 'white'
        self.gpt_chk_on2_bg = 'yellow'
        self.gpt_chk_on2_tc = 'black'

        # 項目更新
        chk_on_bg  = self.gpt_chk_on_bg
        chk_on_tc  = self.gpt_chk_on_tc
        chk_off_bg = self.gpt_chk_off_bg
        chk_off_tc = self.gpt_chk_off_tc
        chk_on2_bg = self.gpt_chk_on2_bg
        chk_on2_tc = self.gpt_chk_on2_tc

        if (self.window['_check_fromClip_'].get() == True):
            self.window['_check_fromClip_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_fromClip_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_fileParser_'].get() == True):
            self.window['_check_fileParser_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_fileParser_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_pdfParser_'].get() == True):
            self.window['_check_pdfParser_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_pdfParser_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_htmlParser_'].get() == True):
            self.window['_check_htmlParser_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_htmlParser_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_imageOCR_'].get() == True):
            self.window['_check_imageOCR_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_imageOCR_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_toGPT_'].get() == True):
            self.window['_check_toGPT_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_toGPT_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_fromSpeech_'].get() == True):
            self.window['_check_fromSpeech_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_fromSpeech_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_useFunctions_'].get() == True):
            self.window['_check_useFunctions_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_useFunctions_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_toClip_'].get() == True):
            self.window['_check_toClip_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_toClip_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_toSpeech_'].get() == True):
            self.window['_check_toSpeech_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_toSpeech_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_openai_'].get() == True):
            self.window['_check_openai_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_openai_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_freeai_'].get() == True):
            self.window['_check_freeai_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_freeai_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_ollama_'].get() == True):
            self.window['_check_ollama_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_ollama_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_autoUpload_'].get() == True):
            self.window['_check_autoUpload_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_autoUpload_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_autoSandbox_'].get() == True):
            self.window['_check_autoSandbox_'].update(background_color=chk_on_bg, text_color=chk_on_tc, )
        else:
            self.window['_check_autoSandbox_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )
        if (self.window['_check_debugMode_'].get() == True):
            self.window['_check_debugMode_'].update(background_color=chk_on2_bg, text_color=chk_on2_tc, )
        else:
            self.window['_check_debugMode_'].update(background_color=chk_off_bg, text_color=chk_off_tc, )

        return True

    # POPUP 画面表示
    def popup_text(self, title='', text='', auto_close=False, size=(96,24), ):
        txt = text
        try:
            dic = json.loads(text)
            txt = json.dumps(dic, ensure_ascii=False, indent=4, )
        except:
            pass
        if (auto_close == False):
            res= sg.popup_scrolled(txt, title='[ ' + title + ' ] (Read only)', keep_on_top=True,
                                non_blocking=True, font='Arial 16', size=size, )
        else:            
            res= sg.popup_scrolled(txt, title='[ ' + title + ' ] (Read only)', keep_on_top=True,
                                non_blocking=True, font='Arial 16', size=size, yes_no=None, 
                                auto_close=True, auto_close_duration=float(auto_close), )
        return True



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
                 keep_on_top='yes', alpha_channel='0.5', icon=icon, )
        gui.bind()

        # ボタン有効化 (リセットは最後に)
        #gui.window['_check_imageOCR_'].update(visible=True)
        #gui.window['_check_useFunctions_'].update(visible=True)
        #gui.window['_check_fromSpeech_'].update(visible=True)
        #gui.window['_check_toSpeech_'].update(visible=True)
        #gui.window['_exec_toSpeech_'].update(visible=True)
        #gui.window['_proc_toSpeech_'].update(visible=True)
        #gui.window['-clear-'].update(visible=True)
        #gui.window['-reset-'].update(visible=True)

        # GUI 専用キュー
        gui_queue = queue.Queue()

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
            gui.reset(role_text='', req_text='', web_home='', )

            # GUI 自動フェードリセット
            gui.autoFadeControl(reset=True, )

            # GUI 画面リサイズリセット
            gui.resize(reset=True, )

        # GUI 項目更新
        while (gui_queue.qsize() >= 1):
            [res_name, res_value] = gui_queue.get()
            gui_queue.task_done()
            gui.window[res_name].update(res_value)

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
        if event == sg.WIN_CLOSED:
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

                # ステータスバー
                tm     = time.time()
                tm     = tm % 9
                r   = int(abs(np.sin((tm+0)/ 9 * np.pi * 2))*255)
                g   = int(abs(np.sin((tm+3)/ 9 * np.pi * 2))*255)
                b   = int(abs(np.sin((tm+6)/ 9 * np.pi * 2))*255)
                gui.window['_status_bar_'].update(background_color=gui.rgb2hex(r,g,b))

                # ↓ Test code
                now   = datetime.datetime.now()
                stamp = now.strftime('%Y%m%d%H%M%S')
                gui_queue.put(['_req_text_', stamp])

                w, h = gui.window.size
                wh    = str(w) + ', ' + str(h)
                gui_queue.put(['_input_text_', wh])

            # ------------------------------
            # ボタンイベント処理
            # ------------------------------
            # クリア
            elif (event == '-clear-'):
                print(event, )

            # リセット
            elif (event == '-reset-'):
                print(event, )
                reset_flag = True

            # ------------------------------
            # チェックボックス処理
            # ------------------------------
            elif (event == '_check_fromClip_') \
            or   (event == '_check_fileParser_') \
            or   (event == '_check_pdfParser_') \
            or   (event == '_check_htmlParser_') \
            or   (event == '_check_toGPT_') \
            or   (event == '_check_toClip_') \
            or   (event == '_check_openai_') \
            or   (event == '_check_freeai_') \
            or   (event == '_check_ollama_') \
            or   (event == '_check_autoUpload_') \
            or   (event == '_check_autoSandbox_') \
            or   (event == '_check_debugMode_'):
                refresh_flag = True

            elif (event == '_check_imageOCR_'):
                refresh_flag = True

            elif (event == '_check_fromSpeech_'):
                refresh_flag = True

            elif (event == '_check_useFunctions_'):
                refresh_flag = True

            elif (event == '_check_toSpeech_'):
                refresh_flag = True

            elif (event == '_addin_tree_'):
                addin_name = values['_addin_tree_'][0]
                #print(addin_name)
                if addin_name in gui.window['_addin_tree_'].metadata:
                    gui.window['_addin_tree_'].metadata.remove(addin_name)
                    gui.window['_addin_tree_'].update(key=addin_name, icon=gui.check_box[0])
                else:
                    gui.window['_addin_tree_'].metadata.append(addin_name)
                    gui.window['_addin_tree_'].update(key=addin_name, icon=gui.check_box[1])

            elif (event == '_function_tree_'):
                func_name = values['_function_tree_'][0]
                #print(func_name)
                if func_name in gui.window['_function_tree_'].metadata:
                    gui.window['_function_tree_'].metadata.remove(func_name)
                    gui.window['_function_tree_'].update(key=func_name, icon=gui.check_box[0])
                else:
                    gui.window['_function_tree_'].metadata.append(func_name)
                    gui.window['_function_tree_'].update(key=func_name, icon=gui.check_box[1])

            elif (event == '_sendfile_tree_'):
                send_file = values['_sendfile_tree_'][0]
                #print(send_file)
                if send_file in gui.window['_sendfile_tree_'].metadata:
                    gui.window['_sendfile_tree_'].metadata.remove(send_file)
                    gui.window['_sendfile_tree_'].update(key=send_file, icon=gui.check_box[0])
                else:
                    gui.window['_sendfile_tree_'].metadata.append(send_file)
                    gui.window['_sendfile_tree_'].update(key=send_file, icon=gui.check_box[1])

            # ------------------------------
            # キーボードイベント処理
            # ------------------------------
            elif (event == '_input_path_') \
            or   (event == '_role_text_') \
            or   (event == '_req_text_') \
            or   (event == '_input_text_') \
            or   (event == '_output_text_') \
            or   (event == '_proc_text_'):
                # GUI 自動フェードリセット
                gui.autoFadeControl(reset=True, )

            # ------------------------------
            # POPUP 処理
            # ------------------------------
            elif (event == '_input_text_ double'):
                gui.popup_text(title='Input Text', text=values['_input_text_'], )
            elif (event == '_output_text_ double'):
                gui.popup_text(title='Output Text', text=values['_output_text_'], )
            elif (event == '_proc_text_ double'):
                gui.popup_text(title='Proc Text', text=values['_proc_text_'], )
            #elif (event == '_history_list_ double'):
            #    gui.popup_text(title='Proc Text', text=values['_history_list_'][0], )

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


