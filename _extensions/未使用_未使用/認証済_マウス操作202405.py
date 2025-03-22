#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

import sys
import os
import time
import datetime
import codecs
import glob

import json

import screeninfo
import pyautogui



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "mouse_operation"
        self.func_ver  = "v0.20240518"
        self.func_auth = "4z3Fk5/iQ3bsYb5DF5vmfNuU0QWoXKNSoDg0cqGnVGs="
        self.function  = {
            "name": self.func_name,
            "description": \
"""
マウス操作を行います。
マウスポインタの位置の移動やマウスのクリック操作等が実行できます。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "runMode": {
                        "type": "string",
                        "description": "実行モード 例) assistant"
                    },
                    "position_left": {
                        "type": "string",
                        "description": "マウスポインタ位置の移動Ｘ軸 例）960"
                    },
                    "position_top": {
                        "type": "string",
                        "description": "マウスポインタ位置の移動Ｙ軸 例）540"
                    },
                    "click_action": {
                        "type": "string",
                        "description": "マウスのクリック操作 yes or no 例）no"
                    },
                },
                "required": ["runMode", "click_action"]
            }
        }

        # 初期設定
        self.runMode  = 'assistant'

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        runMode       = None
        position_left = None
        position_top  = None
        click_action  = None
        if (json_kwargs is not None):
            args_dic      = json.loads(json_kwargs)
            runMode       = args_dic.get('runMode')
            position_left = str( args_dic.get('position_left') )
            position_top  = str( args_dic.get('position_top') )
            click_action  = str( args_dic.get('click_action') )

        if (runMode is None) or (runMode == ''):
            runMode      = self.runMode
        else:
            self.runMode = runMode

        # 全スクリーンの配置
        min_left     = 0
        min_top      = 0
        max_right    = 0
        max_buttom   = 0
        for s in screeninfo.get_monitors():
            if (s.x < min_left):
                min_left = s.x
            if (s.y  < min_top):
                min_top = s.y
            if ((s.x+s.width) > max_right):
                max_right = (s.x+s.width)
            if ((s.y+s.height) > max_buttom):
                max_buttom = (s.y+s.height)

        # マウス配置
        mouse_x,mouse_y = pyautogui.position()

        # 画像切り出し
        screen = -1
        for s in screeninfo.get_monitors():
            screen += 1

            # 処理スクリーン？
            if  (mouse_x >= s.x) and (mouse_x <= (s.x+s.width)) \
            and (mouse_y >= s.y) and (mouse_y <= (s.y+s.height)):

                # マウス位置
                x , y = mouse_x,mouse_y
                move_flag = False
                if (position_left is not None):
                    if (str(position_left).isdigit()):
                        x = s.x + int(position_left)
                        move_flag = True
                if (position_top is not None):
                    if (str(position_top).isdigit()):
                        y = s.y + int(position_top)
                        move_flag = True
                if (move_flag == True):
                    pyautogui.moveTo(x, y)

            # クリック
            if (click_action.lower() == 'yes'):
                pyautogui.click()

        # 戻り
        dic = {}
        dic['result'] = 'ok'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ ' \
                      + '"position_left" : "100",' \
                      + '"position_top" : "100",' \
                      + '"click_action" : "no"' \
                      + ' }'))


