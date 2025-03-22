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

import sys
import os
import time
import datetime
import codecs
import glob
import shutil

import queue
import threading

import subprocess

import torch
import whisper



config_path     = '_config/'
config_file     = 'RiKi_ClipnGPT_key.json'
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



class qWhisper_class:

    def __init__(self, runMode='debug', cuda=False, model='large-v3', ): 

        # 出力フォルダ用意
        if (not os.path.isdir(qPath_temp)):
            os.makedirs(qPath_temp)

        # CUDA 無効化（有効な場合、GPUメモリが大量に必要！）
        print('torch version        =', torch.__version__)
        print('torch cuda available =', torch.cuda.is_available())
        if (cuda == False) and (torch.cuda.is_available() == True):
            print('torch.cuda.無効化！')
            torch.cuda.is_available = lambda: False
            print('torch cuda available =', torch.cuda.is_available())

        if (not model in ['tiny','base','small','medium','large-v2','large-v3',]):
            model = 'small'

        # Whisper認識設定
        #print('Whisper認識設定 ' + model)
        if (not os.path.exists('_extensions/models/' + str(model) + '.pt')):
            self.whisper_model = whisper.load_model(model)
        else:
            self.whisper_model = whisper.load_model(model, download_root='_extensions/models')

    def whisper_proc(self, inp_file='input.mp4', wav_file='temp.wav', txt_file='temp.txt', srt_file='temp.srt', ):

        # ファイル確認、消去
        if (not os.path.exists(inp_file)):
            return False
        try:
            os.remove(wav_file) 
        except:
            pass
        try:
            os.remove(txt_file) 
        except:
            pass
        try:
            os.remove(srt_file) 
        except:
            pass

        # 音声分離
        #print('音声分離出力 ' + wav_file)
        ffmpeg = subprocess.Popen(['ffmpeg', '-y',
            '-i', inp_file,
            '-af', 'dynaudnorm', 
            '-ar', '16000', '-ac', '1', 
            wav_file,
            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 時限待機
        if (ffmpeg is not None):
            checkTime = time.time()
            while ((time.time() - checkTime) < 30):
                line = ffmpeg.stderr.readline()
                #if (len(line) != 0):
                #    print(line.decode())
                if (not line) and (ffmpeg.poll() is not None):
                    break
                time.sleep(0.01)
        ffmpeg.terminate()
        ffmpeg = None

        # 音声認識
        #print('Whisper音声認識')
        #try:
        result = self.whisper_model.transcribe(wav_file, verbose=True, fp16=False, )
        #except:
        #    result = None

        if (result is None):
            print('★Whisper（処理）エラー')
            return False

        if (len(result['segments']) <= 0):
            print('★Whisper（認識０件）エラー')
            return False

        # ファイルオープン
        #print('ファイル出力 ' + txt_file + ', ' + srt_file)
        txtf = codecs.open(txt_file, mode='w', encoding='utf-8', )
        srtf = codecs.open(srt_file, mode='w', encoding='utf-8', )

        # ファイル出力
        n = 0
        for r in result['segments']:
            n += 1
            st = r['start']
            st_t = datetime.timedelta(seconds=st, )
            st_str = str(st_t).replace('.', ',')
            if (st_str[1:2] == ':'):
                st_str = '0' + st_str
            if (len(st_str) == 8):
                st_str = st_str + ',000000'
            st_str = st_str[:12]
            en = r['end']
            en_t = datetime.timedelta(seconds=en, )
            en_str = str(en_t).replace('.', ',')
            if (en_str[1:2] == ':'):
                en_str = '0' + en_str
            if (len(en_str) == 8):
                en_str = en_str + ',000000'
            en_str = en_str[:12]
            txt = r['text']
            #print(str(n), st_str, '-->', en_str, txt, )

            # テキスト
            txtf.write(str(txt) + '\n')

            # 字幕
            srtf.write(str(n) + '\n')
            srtf.write(st_str + ' --> ' + en_str + '\n')
            srtf.write(str(txt) + '\n')
            srtf.write('\n')

        # ファイルクローズ
        txtf.close()
        txtf = None
        srtf.close()
        srtf = None

        return True

    def jimaku_proc(self, inp_file='input.mp4', srt_file='temp.srt', out_file='output.mp4', ):

        # ファイル確認、消去
        if (not os.path.exists(inp_file)):
            return False
        if (not os.path.exists(srt_file)):
            return False
        try:
            os.remove(out_file) 
        except:
            pass

        # 字幕合成
        #print('字幕合成出力 ' + out_file)
        ffmpeg = subprocess.Popen(['ffmpeg', '-y',
            '-i', inp_file,
            '-i', srt_file,
            '-c', 'copy', '-c:s', 'mov_text', '-metadata:s:s:0', 'language=jpn',
            out_file,
            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 時限待機
        if (ffmpeg is not None):
            checkTime = time.time()
            while ((time.time() - checkTime) < 30):
                line = ffmpeg.stderr.readline()
                #if (len(line) != 0):
                #    print(line.decode())
                if (not line) and (ffmpeg.poll() is not None):
                    break
                time.sleep(0.01)
        ffmpeg.terminate()
        ffmpeg = None

        if (not os.path.exists(out_file)):
            return False

        return True

    def proc(self, inp_file='', ):
        time.sleep(5.00)

        # 入力ファイル
        if (inp_file == ''):
            filex = qPath_input + '_whisper_input'
            if   (os.path.isfile(filex + '.mp3')):
                      inp_file = filex + '.mp3'
            elif (os.path.isfile(filex + '.mp4')):
                      inp_file = filex + '.mp4'
            elif (os.path.isfile(filex + '.m4a')):
                      inp_file = filex + '.m4a'
            elif (os.path.isfile(filex + '.m4v')):
                      inp_file = filex + '.m4v'
            else:
                print('音声字幕', 'File not found, _whisper_input.*')
                return False
        if (not os.path.isfile(inp_file)):
                print('音声字幕', 'File not found,', inp_file)
                return False

        # 出力ファイル
        inp_ext  = inp_file[-4:].lower()
        nowTime  = datetime.datetime.now()
        out_base = qPath_output + nowTime.strftime('%Y%m%d.%H%M%S')
        org_file = out_base + '.stt.input' + inp_ext
        wav_file = out_base + '.stt.output.wav'
        txt_file = out_base + '.stt.output.txt'
        srt_file = out_base + '.stt.output.srt'
        out_file = out_base + '.stt.output.mp4'

        # コピー
        shutil.copy(inp_file, org_file)

        # 音声認識
        print('音声認識', '(Whisper)')
        print('音声認識', 'input = ' + org_file)
        res = qWhisper.whisper_proc(org_file, wav_file, txt_file, srt_file, )
        #print(inp_file, res)
        print('音声認識', 'result= ' + str(res))

        if (os.path.exists(wav_file)):
            print('音声認識', 'wav   = ' + wav_file)
        if (os.path.exists(txt_file)):
            print('音声認識', 'txt   = ' + txt_file)
        if (os.path.exists(srt_file)):
            print('音声認識', 'srt   = ' + srt_file)

        # 字幕合成
        if (res == True):
            if (inp_ext == '.mp4') or (inp_ext == '.m4v'):

                print('字幕合成', '(字幕合成)')
                res = qWhisper.jimaku_proc(inp_file, srt_file, out_file, )
                #print(out_file, res)
                print('字幕合成', 'jimaku=' + str(res))

                if (os.path.exists(out_file)):
                    print('字幕合成', 'output= ' + out_file)

        return res



if __name__ == '__main__':

    # 初期設定
    #res = xx.settings()
    #if (res != True):
    #    sys.exit(0)

    # 指示受信クリア
    dummy = io_text_read(qIO_func2py)

    # 出力フォルダ用意
    try:
        os.makedirs(qPath_output)
    except:
        pass

    # 準備完了
    print(qText_ready)
    res = io_text_write(qIO_py2func, qText_ready)
    time.sleep(0.50)

    # Debug!
    #question = "Clip&GPTの概要"
    #json_kwargs= '{ "question" : "' + question + '" }'
    #res = io_text_write(qIO_func2py, json_kwargs)

    # 処理ループ
    while True:
        time.sleep(0.50)

        # 指示受信
        json_kwargs = io_text_read(qIO_func2py)
        time.sleep(0.50)

        # 処理
        if (json_kwargs.strip() != ''):

            # 開始
            print('\n' + '【開始】')
            print(qText_start)
            res = io_text_write(qIO_py2func, qText_start)
            time.sleep(0.50)

            args_dic   = json.loads(json_kwargs)
            model_name = args_dic.get('model_name')
            language   = args_dic.get('language')
            res_text   = ''

            # バッチ処理
            try:
                cuda     = False
                qWhisper = qWhisper_class(
                    cuda=cuda, model=model_name, )

                batch_proc = threading.Thread(
                    target=qWhisper.proc, args=(), daemon=True, )
                batch_proc.start()

                res_text = '音声認識(+字幕処理)をバッチ処理に投入しました。'
            except Exception as e:
                print(e)

            time.sleep(0.50)

            # 戻り
            dic = {}
            if (res_text != '') and (res_text != '!'):
                dic['result'] = res_text
            else:
                dic['error']  = 'unknown'
            json_dump = json.dumps(dic, ensure_ascii=False, )

            # 完了送信
            print(res_text + '\n' + qText_complete + '\n')
            res = io_text_write(qIO_py2func, json_dump + '\n' + qText_complete)
            time.sleep(0.50)

            # (念のため)指示受信クリア
            dummy = io_text_read(qIO_func2py)
            time.sleep(0.50)


