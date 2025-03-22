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
import codecs
import time

import 認証済_音声合成 as text_to_speech
tts = text_to_speech._class()

def main():
    # ファイル
    dir_path = os.path.dirname(__file__)
    filename = dir_path + '/' + 'サンプル_ナレーション再生.txt'
    encoding =  'utf-8-sig'

    # 読取
    text = ''
    r = codecs.open(filename, 'r', encoding)
    for t in r:
        t = t.replace('\r', '')
        if (t.strip() == ''):
            time.sleep(0.20)
        else:
            # 音声合成
            print(t)
            dic = {}
            dic['speech_text'] = t
            dic['language']    = 'ja'
            json_dump = json.dumps(dic, ensure_ascii=False, )
            tts.func_proc( json_dump )

        text += t
    r.close
    r = None

    return True

if __name__ == '__main__':
    res = main()
