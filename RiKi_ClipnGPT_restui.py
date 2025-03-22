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

import queue
import threading

from flask import Flask, request, jsonify, abort, make_response
import json

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_input  = 'temp/input/'
qPath_output = 'temp/output/'
qPath_work   = 'temp/_work/'

# 共通ルーチン
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



class _restui:

    def __init__(self, ):

        self.runMode                    = 'debug'
        self.limit_mode                 = False
        self.conf                       = None
        self.chatbot                    = None
        self.chatproc                   = None
        self.flask_base                 = ''

        self.restui_local_ip            = '0.0.0.0'
        self.restui_local_port          = 61101
        self.restui_allow_ip            = '255.255.255.255'
        self.restui_allow_mask          = self.mask_from_ip('255.255.255.255')
        self.restui_ssl                 = 'no'
        self.restui_ssl_cert            = ''
        self.restui_ssl_key             = ''
        self.restui_auth_key            = 'secret'

        self.timeOut                    = 120

    def init(self, qLog_fn='', runMode='debug', limit_mode=False, 
             conf=None, chatbot=None, chatproc=None, 
             flask_base='', ):

        self.runMode             = runMode
        self.limit_mode          = limit_mode

        # ログ
        self.proc_name = 'restui'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')

        # パス
        if (not os.path.exists(qPath_work)):
            os.makedirs(qPath_work)

        self.conf                = conf
        self.chatbot             = chatbot
        self.chatproc            = chatproc
        self.flask_base          = flask_base

        if (conf is not None):
            self.restui_local_ip         = conf.restui_local_ip
            self.restui_local_port       = int(conf.restui_local_port)
            self.restui_allow_ip         = conf.restui_allow_ip 
            self.restui_allow_mask       = self.mask_from_ip(conf.restui_allow_ip)
            self.restui_ssl              = conf.restui_ssl
            self.restui_ssl_cert         = conf.restui_ssl_cert
            self.restui_ssl_key          = conf.restui_ssl_key
            self.restui_auth_key         = conf.restui_auth_key

        # Flask
        self.app = Flask(__name__, )
        self.app.config['UPLOAD_FOLDER']   = self.flask_base + qPath_input
        self.app.config['DOWNLOAD_FOLDER'] = self.flask_base + qPath_output
        self.app.config['SECRET_KEY']      = os.urandom(24)
        self.flask_routes()

    def mask_from_ip(self, ip):
        octets = ip.split('.')
        if   (int(octets[0]) == 255) and (int(octets[1]) == 255) and (int(octets[2]) == 255) and (int(octets[3]) == 255):
            return 0
        elif (int(octets[1]) == 255) and (int(octets[2]) == 255) and (int(octets[3]) == 255):
            return 8
        elif (int(octets[2]) == 255) and (int(octets[3]) == 255):
            return 16
        elif (int(octets[3]) == 255):
            return 24
        else:
            return 32

    def ip_in_subnet(self, ip):
        if (ip == '127.0.0.1'):
            return True
        if (self.restui_allow_mask == 0):
            return True
        ip_int = int(''.join([f"{int(i):08b}" for i in ip.split('.')]), 2)        
        # Mask the allow_ip to get the actual subnet address
        subnet_ip = '.'.join([str(int(octet) & (255 if mask_bit > 0 else 0)) 
        for octet, mask_bit in zip(self.restui_allow_ip.split('.'), 
            [(self.restui_allow_mask - i * 8) if (self.restui_allow_mask - i * 8) > 0 else 0 for i in range(4)])])
        subnet_int = int(''.join([f"{int(i):08b}" for i in subnet_ip.split('.')]), 2)
        return (ip_int & (0xFFFFFFFF << (32 - self.restui_allow_mask))) == subnet_int

    def flask_start(self):
        qLog.log('info', self.proc_id, 'start')
        self.flask_thread = threading.Thread(target=self.flask_proc, daemon=True, )
        self.flask_thread.start()

    def flask_proc(self):
        if (self.restui_ssl == 'yes'):
            self.app.run(host=self.restui_local_ip, port=self.restui_local_port,
                        ssl_context=(self.restui_ssl_cert, self.restui_ssl_key),
                        debug=True, use_reloader=False)
        else:
            self.app.run(host=self.restui_local_ip, port=self.restui_local_port,
                        debug=True, use_reloader=False)

    def flask_routes(self):
        @self.app.before_request
        def limit_remote_addr():
            client_ip = request.remote_addr
            if not self.ip_in_subnet(client_ip):
                qLog.log('error', self.proc_id, f"Access denied for IP = {client_ip}")
                abort(403)  # Forbidden
        
        @self.app.route('/test', methods=['GET', 'POST'])
        def test():
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /test")
            return jsonify({'result': 'ok'})

        @self.app.route('/v0/assistant', methods=['GET', 'POST'])
        def v0_assistant():
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /v0/assistant")

            # 認証確認
            if (self.restui_auth_key != ''):
                auth_header = request.headers.get('Authorization')
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    if (token != self.restui_auth_key):
                        abort(401)
                #else:
                #    abort(401)

            # パラメータ
            request_text = None
            if request.method == 'POST':
                data = request.json
                request_text = data.get('request_text')
            else:
                request_text = request.args.get('request_text')

            # 戻り値
            result_text = None

            # 処理
            text = '!'
            path = ''
            if (self.chatbot is None) or (request_text.strip() == ''):
                client_ip = request.remote_addr
                time.sleep(1.00)
            else:
                qLog.log('info', self.proc_id, 'request \n' + request_text)

                # 忙しいときは busy 回答
                if (self.chatproc.worker_queue.qsize() > 0):
                    qLog.log('info', self.proc_id, 'result busy!')
                    return jsonify({'result': 'busy'})

                # バッチ投入
                gpt_history = []
                gpt_class   = 'auto'
                gpt_sysText = ''
                gpt_reqText = ''
                gpt_inpText = request_text
                gpt_files   = []
                interface   = 'web-rest'
                session_id  = 'rest'
                res_queue   = queue.Queue()

                gpt_proc = threading.Thread(target=self.chatproc.proc_gpt, args=(
                                            res_queue, None, {}, 
                                            gpt_sysText, gpt_reqText, gpt_inpText, 
                                            gpt_files, interface, gpt_class, session_id, 
                                            gpt_history,
                                            ), daemon=True, )
                self.chatproc.worker_queue.put(gpt_proc)

                # 結果受信
                text = ''
                path = ''

                checkTime = time.time()
                while ((time.time() - checkTime) < self.timeOut):
                    if (res_queue.qsize() >= 1):
                        break
                    time.sleep(0.25)

                while (res_queue.qsize() >= 1):
                    [res_name, res_value] = res_queue.get()
                    res_queue.task_done()
                    if (res_name=='_output_text_'):
                        text = res_value
                    if (res_name=='_input_path_'):
                        path = res_value
                    if (res_name=='[history]'):
                        pass
                    time.sleep(0.25)

                if (text != '') and (text != '!'):
                    result_text = text
                    qLog.log('info', self.proc_id, 'result \n' + result_text)

            if (result_text is None):
                return jsonify({'result': 'ng'})
            else:
                response_data = {'result': 'ok', 'result_text': result_text}
                response = make_response(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
                response.headers['Content-Type'] = 'application/json; charset=utf-8'
                return response

        
if __name__ == '__main__':

    restui = _restui()

    base_path = os.path.dirname(sys.argv[0]) + '/'
    restui.init(qLog_fn='', runMode='debug', limit_mode=False, 
               conf=None, chatbot=None, chatproc=None,
               flask_base=base_path, )
    restui.flask_start()

    time.sleep(300)


