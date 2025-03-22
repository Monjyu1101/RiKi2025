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
import codecs
import subprocess

import queue
import threading

# インターフェース
ext_python_init   = 'サンプル_音声字幕202311_pyinit.py'
ext_python_script = 'サンプル_音声字幕202311_python.py'
qText_ready       = '音声字幕 function ready!'
qText_start       = '音声字幕 function start!'
qText_complete    = '音声字幕 function complete!'
qIO_func2py       = 'temp/音声字幕_func2py.txt'
qIO_py2func       = 'temp/音声字幕_py2func.txt'

qTimeout_init     = 120
qTimeout_reset    = 60
qTimeout_start    = 60
qTimeout_proc     = 300



def io_text_read(filename=''):
    text = ''
    file1 = filename
    file2 = filename[:-4] + '.@@@'
    try:
        while (os.path.isfile(file2)):
            os.remove(file2)
            time.sleep(0.10)
        if (os.path.isfile(file1)):
            os.rename(file1, file2)
            time.sleep(0.10)
        if (os.path.isfile(file2)):
            r = codecs.open(file2, 'r', 'utf-8-sig')
            for t in r:
                t = t.replace('\r', '')
                text += t
            r.close
            r = None
            time.sleep(0.25)
        while (os.path.isfile(file2)):
            os.remove(file2)
            time.sleep(0.10)
    except:
        pass
    return text

def io_text_write(filename='', text='', ):
    try:
        w = codecs.open(filename, 'w', 'utf-8')
        w.write(text)
        w.close()
        w = None
        return True
    except:
        pass
    return False

def kill_pid(pid, ):
    if (os.name == 'nt'):
        try:
            kill = subprocess.Popen(['taskkill', '/pid', str(pid), '/f', ], \
                    shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            kill.wait()
            kill.terminate()
            kill = None
            return True
        except Exception as e:
            pass
    else:
        try:
            kill = subprocess.Popen(['pkill', '-9', '-P', str(pid), ], \
                    shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            kill.wait()
            kill.terminate()
            kill = None
            return True
        except Exception as e:
            pass
    return False

def kill_name(name, ):
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
        self.func_name = "submit_transcription"
        self.func_ver  = "v0.20231112"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": 
"""
動画や音声ファイルから文字起こしを行う。動画の場合は字幕生成まで行う。
ＡＩアシスタントからこの機能で起動されます。
文字お起こしはバッチ処理（非同期）されます。
音声認識モデルは、'tiny','base','small','medium','large-v2','large-v3',
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_name": {
                        "type": "string",
                        "description": "音声認識モデル。指定のない場合は'large-v3' (例) large-v3"
                    },
                    "language": {
                        "type": "string",
                        "description": "言語記号。指定のない場合は日本語'ja' (例) ja"
                    },
                },
                "required": ["model", "language"]
            }
        }

        self.start_time = None
        self.ini_python = None
        self.ini_pid    = None
        self.ext_python = None
        self.ext_pid    = None
        self.reset_run  = False
        res = self.func_reset()
        self.start_time = time.time()

    def __del__(self, ):
        # Python 停止
        if (self.ext_python != None):
            try:
                self.ext_python.terminate()
                self.ext_python = None
                kill_pid(self.ext_pid)
                kill_name('python')
                self.ext_pid    = None
            except:
                pass
        # Python kill!

    def delay_reset(self, sec=5, ):
        time.sleep(float(sec))
        self.func_reset()

    def func_reset(self, ):
        # 初回直後のリセットは無効
        if (self.start_time != None):
            if ((time.time() - self.start_time) < qTimeout_reset):
                return False

        # 他で実行中の場合待機
        checkTime = time.time()
        while ((time.time() - checkTime) < qTimeout_reset) and (self.reset_run == True):
            time.sleep(0.50)

        self.reset_run  = True
        print(ext_python_script + ' reset')

        # Python 停止
        self.__del__()

        # 結果クリア
        dummy = io_text_read(qIO_py2func)

        # Python 初期化
        print(ext_python_init + ' loading')
        try:
            dir_path = os.path.dirname(__file__) + '/'
            self.ini_python = subprocess.Popen(['python', dir_path + ext_python_init,
            ], shell=True, )
            self.ini_pid    = self.ini_python.pid
        except Exception as e:
            print(e)
            raise RuntimeError('★Pythonの実行環境をインストールしてください！')

        # 初期化完了を待機
        wait_sec = qTimeout_init
        ready = False
        checkTime = time.time()
        while ((time.time() - checkTime) < wait_sec):

            # 状況受信
            res      = io_text_read(qIO_py2func)
            res_text = res.strip()
            if (res_text != ''): 
                print(res_text)
                if (res_text != qText_complete): # complete 待機
                    print(res_text)
                else:
                    ready = True
                    break

            time.sleep(0.50)

        if (ready == False):
            # Python 停止
            self.__del__()
            # タイムアウトエラー
            raise RuntimeError('★' + ext_python_init + 'の起動タイムアウト(' + str(wait_sec) + 's)が発生しました！')

        # 結果クリア
        dummy = io_text_read(qIO_py2func)

        # Python 起動
        print(ext_python_script + ' loading')
        try:
            dir_path = os.path.dirname(__file__) + '/'
            self.ext_python = subprocess.Popen(['python', dir_path + ext_python_script,
            ], shell=True, )
            self.ext_pid    = self.ext_python.pid
        except Exception as e:
            print(e)
            raise RuntimeError('★Pythonの実行環境をインストールしてください！')

        # 準備完了を待機
        wait_sec = qTimeout_init
        ready = False
        checkTime = time.time()
        while ((time.time() - checkTime) < wait_sec):

            # 状況受信
            res      = io_text_read(qIO_py2func)
            res_text = res.strip()
            if (res_text != ''): 
                if (res_text != qText_ready): # ready 待機
                    print(res_text)
                else:
                    ready = True
                    break

            time.sleep(0.50)

        if (ready == False):
            # Python 停止
            self.__del__()
            # タイムアウトエラー
            raise RuntimeError('★' + ext_python_script + 'の起動タイムアウト(' + str(wait_sec) + 's)が発生しました！')

        self.reset_run  = False
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 実行状況クリア
        dummy = io_text_read(qIO_py2func)

        # 実行指示送信
        res = io_text_write(qIO_func2py, json_kwargs)
        time.sleep(0.50)

        # 実行開始を待機
        start = False
        checkTime = time.time()
        while ((time.time() - checkTime) < qTimeout_start):
            time.sleep(0.50)

            # 実行状況受信
            res      = io_text_read(qIO_py2func)
            res_text = res.strip()
            if (res_text != ''): 
                if (res_text != qText_start):
                    print(res_text)
                else:
                    start = True
                    break

        # タイムアウトエラー
        if (start == False):
            # リセット実行
            if (self.reset_run == False):
                reset_proc = threading.Thread(target=self.delay_reset, args=(), daemon=True, )
                reset_proc.start()

            # エラー結果
            dic = {}
            dic['error'] = '実行開始タイムアウト(' + str(qTimeout_start) + 's)エラーが発生しました'
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump

        # 実行完了を待機
        complete = False
        res_text = ''
        checkTime = time.time()
        while ((time.time() - checkTime) < qTimeout_proc):
            time.sleep(0.50)

            # 実行状況受信
            res      = io_text_read(qIO_py2func)
            res_text = res.strip()
            if (res_text != ''): 
                if (res_text.find(qText_complete) < 0):  # complete 待機
                    print(res_text)
                else:
                    complete = True
                    res_text = res_text.replace(qText_complete, '')
                    res_text = res_text.strip()
                    break

        # 結果受信クリア
        dummy = io_text_read(qIO_py2func)
        time.sleep(0.50)

        # リセット実行
        #if (self.reset_run == False):
        #    reset_proc = threading.Thread(target=self.delay_reset, args=(), daemon=True, )
        #    reset_proc.start()

        # 実行結果
        if (complete == True):
            json_dump = res_text
            #print('  --> ', json_dump)
            return json_dump
        else:
            dic = {}
            dic['error'] = '実行タイムアウト(' + str(qTimeout_proc) + 's)エラーが発生しました'
            json_dump = json.dumps(dic, ensure_ascii=False, )
            #print('  --> ', json_dump)
            return json_dump

if __name__ == '__main__':

    _ext = _class()
    time.sleep(10)

    #model_name = "large-v3"
    model_name = "small"
    language   = "ja"
    json_kwargs= '{ "model_name": "' + model_name + '", "language": "' + language + '" }'
    res = _ext.func_proc(json_kwargs)
    print("#" + res + "#")

    time.sleep(600)


