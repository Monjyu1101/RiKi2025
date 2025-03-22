#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

# ★　以下、実行環境構築法
## 　↓　2023/06/25操作不要
##   https://github.com/openai/whisper
##   gitからzipダウンロード、解凍後、以下を実行する。↓
##   cd C:\Users\admin\Documents\GitHub\py-etc\whisper\whisper-main
##   python setup.py install
## 　↑　2023/06/25操作不要
#
#    python -m pip  install --upgrade screeninfo
#    python -m pip  install --upgrade pyautogui
#    python -m pip  install --upgrade pywin32
#    python -m pip  install --upgrade psutil
#    python -m pip  install --upgrade rainbow-logging-handler
#    python -m pip  install --upgrade pycryptodome
#
#    python -m pip  install --upgrade torch
#    python -m pip  install --upgrade openai-whisper
#
#    python -m pip  install --upgrade six
#    python -m pip  install --upgrade tqdm
#    python -m pip  install --upgrade packaging
#    python -m pip  install --upgrade tokenizers

# ★　CUDA有効化
#   pip uninstall torch
#   pip install   torch  --extra-index-url https://download.pytorch.org/whl/cu116

# ★　メモ 2023/06/25時点
#   exe化可能。
#    pyinstaller %pyname%.py  -F --log-level ERROR  --copy-metadata tokenizers --copy-metadata packaging --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --collect-data whisper



# 静的インストール
import sys
import os
import time
import datetime
import codecs

qPath_temp      = 'temp/'
qPath_input     = 'temp/input/'
qPath_output    = 'temp/output/'

# インターフェース
qText_ready     = '音声字幕 function ready!'
qText_start     = '音声字幕 function start!'
qText_complete  = '音声字幕 function complete!'
qIO_func2py     = 'temp/音声字幕_func2py.txt'
qIO_py2func     = 'temp/音声字幕_py2func.txt'

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

# 動的インストール
from pip._internal import main as _main
import importlib
def pip_install(module='', ver=None):
    try:
        if ver is None:
            _main(['install', '--upgrade', module])
        else:
            _main(['install', '--upgrade', '{}=={}'.format(module, ver)])
    except:
        print("pip install error!: {}".format(module))

# 動的インストール
try:
    import whisper
except:
    print('pip install ...')
    pip_install('pip')
    pip_install('wheel')
    pip_install('setuptools')

    pip_install('torch')
    pip_install('openai-whisper')



if __name__ == '__main__':

    # 出力フォルダ用意
    if (not os.path.isdir(qPath_temp)):
        os.makedirs(qPath_temp)
    if (not os.path.isdir(qPath_input)):
        os.makedirs(qPath_input)
    if (not os.path.isdir(qPath_output)):
        os.makedirs(qPath_output)

    # 準備完了
    #print(qText_complete)
    res = io_text_write(qIO_py2func, qText_complete)
    time.sleep(0.50)

    #print('pip install ok')
    sys.exit(0)


