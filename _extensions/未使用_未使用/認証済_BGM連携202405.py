#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

import json
import os
import time

import subprocess



class bgm_class:
    def __init__(self, runMode='assistant', ):
        self.runMode = runMode
        self.process = None

    def start(self, ):
        # 起動
        parm = []
        parm.append('RiKi_showMeCaller')
        parm.append('auto')
        parm.append('RiKi_showMeVideo24')
        parm.append('bgmdrive')
        parm.append('auto')
        parm.append('auto')
        parm.append('C:/_共有/')
        parm.append('BGM_etc/')
        parm.append('50')
        try:
            if (os.name == 'nt'):
                self.process = subprocess.Popen(['cmd.exe', '/c'] + parm)
            else:
                self.process = subprocess.Popen(parm)
        except Exception as e:
            print(e)
        time.sleep(1.00)

        # 確認
        res_flag = False
        checkTime = time.time()
        while ((time.time() - checkTime) <= 5):
            if (self.process.poll() is None):
                res_flag = True
                break
            time.sleep(0.50)
        if (res_flag == False):
            self.process = None

        return res_flag

    def stop(self, ):
        # 停止
        #try:
        #    if (self.process is not None):
        #        self.process.terminate()
        #        self.process = None
        #except Exception as e:
        #    print(e)
        # 強制停止
        self.kill('RiKi_showMeCaller')
        self.kill('RiKi_showMeVideo24')
        self.process = None
        # ffplay停止
        self.kill('ffplay')

        return True

    def kill(self, name, ):
        if (os.name == 'nt'):
            try:
                kill = subprocess.Popen(['taskkill', '/im', name + '.exe', '/f', ], \
                       shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        else:
            try:
                kill = subprocess.Popen(['pkill', '-9', '-f', name, ], \
                       shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        return False



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "execute_BGM_control"
        self.func_ver  = "v0.20240428"
        self.func_auth = "ErS5ozUvF4BE4XDewyfJgziPUsqEstHwV1uKhD6B888="
        self.function  = {
            "name": self.func_name,
            "description": \
"""
BGM再生を開始したり、終了させたりする
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "runMode": {
                        "type": "string",
                        "description": "実行モード 例) assistant"
                    },
                    "start_or_stop": {
                        "type": "string",
                        "description": "BGM再生を開始または終了の指定 start,stop (例) start"
                    },
                },
                "required": ["runMode", "start_or_stop"]
            }
        }

        # 初期設定
        self.runMode  = 'assistant'
        self.bgm_proc = bgm_class(runMode=self.runMode, )
        self.func_reset()

    def func_reset(self, ):
        self.bgm_proc.stop()
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        runMode       = None
        start_or_stop = None
        if (json_kwargs != None):
            args_dic      = json.loads(json_kwargs)
            runMode       = args_dic.get('runMode')
            start_or_stop = args_dic.get('start_or_stop')

        if (runMode is None) or (runMode == ''):
            runMode      = self.runMode
        else:
            self.runMode = runMode

        # BGM再生開始
        if (start_or_stop == 'start'):

            # 再生停止
            res = self.bgm_proc.stop()

            # 再生開始
            res = self.bgm_proc.start()

            if (res == True):
                dic = {}
                dic['result'] = "BGM再生を開始しました" 
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump
            else:
                dic = {}
                dic['result'] = "BGM再生が開始できませんでした" 
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump

        # BGM再生終了
        if (start_or_stop == 'stop'):

            # 再生停止
            res = self.bgm_proc.stop()

            if (res == True):
                dic = {}
                dic['result'] = "BGM再生を終了しました" 
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump
            else:
                dic = {}
                dic['result'] = "BGM再生が停止できませんでした" 
                json_dump = json.dumps(dic, ensure_ascii=False, )
                #print('  --> ', json_dump)
                return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ ' \
                      + '"start_or_stop" : "start"' \
                      + ' }'))
    time.sleep(60.00)

    print(ext.func_proc('{ ' \
                      + '"start_or_stop" : "stop"' \
                      + ' }'))
    time.sleep(2.00)

