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

from gtts import gTTS
import base64

from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory, jsonify, Response, make_response, abort
qPath_templates = '_webui/clipngpt'
qPath_static    = '_webui/clipngpt/static'

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_input  = 'temp/input/'
qPath_output = 'temp/output/'
qPath_work   = 'temp/_work/'

# 共通ルーチン
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



class _webui:

    def __init__(self, ):

        self.runMode                    = 'debug'
        self.limit_mode                 = False
        self.conf                       = None
        self.chatbot                    = None
        self.chatproc                   = None
        self.flask_base                 = ''

        self.webui_local_ip             = '0.0.0.0'
        self.webui_local_port           = 51101
        self.webui_allow_ip             = '255.255.255.255'
        self.webui_allow_mask           = self.mask_from_ip('255.255.255.255')
        self.webui_multi_session        = 5
        self.webui_ssl                  = 'no'
        self.webui_ssl_cert             = ''
        self.webui_ssl_key              = ''
        self.webui_admin_id             = 'admin'
        self.webui_admin_pw             = 'secret'
        self.webui_guest_id             = 'guest'
        self.webui_guest_pw             = 'guest'

        self.tts_seq                    = 0
        self.timeOut                    = 120

        self.gpt_ini_class              = {}
        self.gpt_ini_role               = {}
        self.gpt_ini_req                = {}
        self.gpt_stt_lang               = {}
        self.gpt_tts_lang               = {}

        self.gpt_ini_class['chat']      = 'auto'
        self.gpt_ini_role['chat']       = 'あなたは美しい日本語で楽しく話す賢いアシスタントです。'
        self.gpt_ini_req['chat']        = '以下の呼びかけに楽しい会話が続くように返答してください。'
        self.gpt_stt_lang['chat']       = 'ja'
        self.gpt_tts_lang['chat']       = 'ja'

        self.gpt_ini_class['translator']= 'chat'
        self.gpt_ini_role['translator'] = 'あなたは一流の翻訳家です。美しい日本語と英語を話します。'
        self.gpt_ini_req['translator']  = '次の文章が日本語なら英語に、英語なら日本語に翻訳してください。'
        self.gpt_stt_lang['translator'] = 'ja'
        self.gpt_tts_lang['translator'] = 'ja'

        self.gpt_ini_class['summary']   = 'chat'
        self.gpt_ini_role['summary']    = 'あなたは一流のライターです。美しい日本語を話します。'
        self.gpt_ini_req['summary']     = '英文は和訳してください。長い文章を要約してください。'
        self.gpt_stt_lang['summary']    = 'ja'
        self.gpt_tts_lang['summary']    = 'ja'

        self.gpt_ini_class['knowledge'] = 'knowledge'
        self.gpt_ini_role['knowledge']  = \
"""
あなたは情報検索するボットです。
ユーザーの問い合わせに対しアップロード済のファイルから情報を検索します。
関連する情報も自動的に検索します。
検索した結果は中学生でも理解できる解りやすい日本語で返答します。
ＷＥＢや３賢者に問い合わせることは禁止です。
"""
        self.gpt_ini_req['knowledge']   = '長い情報は要約するか箇条書きにして返答してください。'
        self.gpt_stt_lang['knowledge']  = 'ja'
        self.gpt_tts_lang['knowledge']  = 'ja'

    def init(self, qLog_fn='', runMode='debug', limit_mode=False, 
             conf=None, chatbot=None, chatproc=None, 
             flask_base='', ):

        self.runMode             = runMode
        self.limit_mode          = limit_mode

        # ログ
        self.proc_name = 'webui'
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
            self.webui_local_ip         = conf.webui_local_ip
            self.webui_local_port       = int(conf.webui_local_port)
            self.webui_allow_ip         = conf.webui_allow_ip 
            self.webui_allow_mask       = self.mask_from_ip(conf.webui_allow_ip)
            self.webui_multi_session    = int(conf.webui_multi_session)
            self.webui_ssl              = conf.webui_ssl
            self.webui_ssl_cert         = conf.webui_ssl_cert
            self.webui_ssl_key          = conf.webui_ssl_key
            self.webui_admin_id         = conf.webui_admin_id
            self.webui_admin_pw         = conf.webui_admin_pw
            self.webui_guest_id         = conf.webui_guest_id
            self.webui_guest_pw         = conf.webui_guest_pw

        # チャット履歴
        self.webui_last_session = 1
        self.webui_sid          = {}
        self.webui_sno          = {}
        self.webui_user         = {}
        self.webui_histories    = {}
        self.webui_files        = {}
        self.webui_last_access  = {}
        self.gpt_histories      = {}
        self.gpt_role           = {}
        self.gpt_req            = {}
        self.gpt_result_queue   = {}
        for sno in range(1, 2 + self.webui_multi_session):
            self.webui_last_access[sno] = time.time()

            for m in self.gpt_ini_role:
                self.webui_histories[str(sno) + str(m)]  = []
                self.webui_files[str(sno) + str(m)]      = []
                self.gpt_histories[str(sno) + str(m)]    = []
                self.gpt_role[str(sno) + str(m)]         = self.gpt_ini_role[str(m)]
                self.gpt_req[str(sno) + str(m)]          = self.gpt_ini_req[str(m)]
                self.gpt_result_queue[str(sno) + str(m)] = queue.Queue()

        # Flask
        self.app = Flask(__name__,  
                         template_folder=self.flask_base + qPath_templates,
                         static_folder=self.flask_base + qPath_static,
                         )
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
        if (self.webui_allow_mask == 0):
            return True
        ip_int = int(''.join([f"{int(i):08b}" for i in ip.split('.')]), 2)        
        # Mask the allow_ip to get the actual subnet address
        subnet_ip = '.'.join([str(int(octet) & (255 if mask_bit > 0 else 0)) 
        for octet, mask_bit in zip(self.webui_allow_ip.split('.'), 
            [(self.webui_allow_mask - i * 8) if (self.webui_allow_mask - i * 8) > 0 else 0 for i in range(4)])])
        subnet_int = int(''.join([f"{int(i):08b}" for i in subnet_ip.split('.')]), 2)
        return (ip_int & (0xFFFFFFFF << (32 - self.webui_allow_mask))) == subnet_int

    def flask_start(self):
        qLog.log('info', self.proc_id, 'start')
        self.flask_thread = threading.Thread(target=self.flask_proc, daemon=True, )
        self.flask_thread.start()

    def flask_proc(self):
        if (self.webui_ssl == 'yes'):
            self.app.run(host=self.webui_local_ip, port=self.webui_local_port,
                        ssl_context=(self.webui_ssl_cert, self.webui_ssl_key),
                        debug=True, use_reloader=False)
        else:
            self.app.run(host=self.webui_local_ip, port=self.webui_local_port,
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
            return render_template('test.html')

        @self.app.route('/')
        def index():
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /")

            sid = session.get('clipngpt_sid')
            sno = None
            if (sid):
                sno = self.webui_sid.get(sid)
                if (sid != self.webui_sno[sno]):
                    return redirect(url_for('login'))
                self.webui_last_access[sno] = time.time()
            else:
                sid = None
                sno = None
            print('/_index.html sid=', sid, 'sno=', sno,)
            return render_template('_index.html', sid=sid, sno=sno, )

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /login")

            username = None
            password = None
            msg      = None

            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
  
                # Check id,pw
                user_id  = ''
                if (    (username.lower() == self.webui_admin_id.lower())  \
                    and (password == self.webui_admin_pw)):
                         user_id = self.webui_admin_id
                if (    (username.lower() == self.webui_guest_id.lower()) \
                    and (password == self.webui_guest_pw)):
                         user_id = self.webui_guest_id
                if (user_id == ''):
                        msg = 'Check Username and Password'
                        return render_template('login.html', username=username, password=password, msg=msg, )

                # Guest access ok ?
                if (user_id == self.webui_guest_id):
                    if (self.webui_multi_session < 1):
                        msg = 'Sorry, Guest use is disabled'
                        return render_template('login.html', username=username, password=password, msg=msg, )

                # login 処理
                #sid = session.get('clipngpt_sid') or str(os.urandom(24))
                sid = str(os.urandom(24))
                sno = None

                # Adminの場合
                if (user_id.lower() == self.webui_admin_id.lower()):
                    sno = 1

                # ゲストの場合、一番古いのを使う。
                if (user_id.lower() == self.webui_guest_id.lower()):
                    s = 0
                    max_time = time.time()
                    for s in range(2, 2 + self.webui_multi_session):
                        if (self.webui_last_access.get(s) is None):
                            sno = s
                            max_time = 0
                        elif (self.webui_last_access.get(s) < max_time):
                            sno = s
                            max_time = self.webui_last_access.get(s)
                    if (sno != 0):
                        self.webui_last_session = sno
                    else:
                        self.webui_last_session += 1
                        if (self.webui_last_session > self.webui_multi_session):
                            self.webui_last_session = 2
                            sno = self.webui_last_session

                # セッションsid,snoを設定
                session['clipngpt_sid'] = sid
                self.webui_sid[sid]     = sno
                self.webui_sno[sno]     = sid
                self.webui_user[sno]    = user_id
                self.webui_last_access[sno] = time.time()

                # ゲストの場合、履歴もクリア。
                for m in self.gpt_ini_role:
                    #self.webui_histories[str(sno) + str(m)]  = []
                    self.webui_files[str(sno) + str(m)]  = []
                    if (user_id == self.webui_guest_id):
                        self.webui_histories[str(sno) + str(m)]  = []
                        self.gpt_histories[str(sno) + str(m)]    = []
                        self.gpt_role[str(sno) + str(m)]         = self.gpt_ini_role[str(m)]
                        self.gpt_req[str(sno) + str(m)]          = self.gpt_ini_req[str(m)]
                        self.gpt_result_queue[str(sno) + str(m)] = None
                        self.gpt_result_queue[str(sno) + str(m)] = queue.Queue()

                return redirect(url_for('index'))

            return render_template('login.html', username=username, password=password, msg=msg, )
    
        @self.app.route('/logout', methods=['GET', 'POST'])
        def logout():
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /logout")

            sid = session.get('clipngpt_sid')
            if (not sid):
                return redirect(url_for('/'))
            sno = self.webui_sid.get(sid)
            #if (sid != self.webui_sno.get(sno)):
            #    return "このセッションは無効です。再ログインしてください。"
 
            if (sid != self.webui_sno.get(sno)) \
            or (request.method == 'POST'):

                # セッションsidを破棄
                session.pop('clipngpt_sid', None)

                return redirect(url_for('index'))

            msg = 'ログアウトしますか？'
            username = self.webui_user.get(sno)
            return render_template('logout.html', sid=sid, sno=sno, msg=msg, username=username, )

        @self.app.route('/chat', methods=['GET', 'POST'])
        def chat():
            client_ip = request.remote_addr 
            mode = request.args.get('mode')
            qLog.log('info', self.proc_id, f"{client_ip} /chat?mode={mode}")

            sid = session.get('clipngpt_sid')
            if (not sid):
                return redirect(url_for('login'))
            sno = self.webui_sid.get(sid)
            if (sid != self.webui_sno.get(sno)):
                return redirect(url_for('login'))
            self.webui_last_access[sno] = time.time()
 
            return render_template('chat.html', mode=mode, sid=sid, sno=sno, )

        @self.app.route('/chat/send_message', methods=['POST'])
        def send_message():
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /chat/send_message")

            sid = session.get('clipngpt_sid')
            if (not sid):
                #return "このセッションは無効です。再ログインしてください。"
                return jsonify([])
            sno = self.webui_sid.get(sid)
            if (sid != self.webui_sno.get(sno)):
                #return "このセッションは無効です。再ログインしてください。"
                return jsonify([])
            self.webui_last_access[sno] = time.time()

            mode = request.form['mode']
            msg  = request.form['message'].rstrip()

            downloadLink = None
            isImage = False
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            text = '!'
            path = ''
            if (self.chatbot is None) or (msg.strip() == ''):
                text = '!' + '\n'
                time.sleep(1.00)
            else:

                # バッチ投入
                gpt_history = self.gpt_histories[str(sno) + str(mode)]
                gpt_class   = self.gpt_ini_class.get(str(mode), 'auto')
                gpt_sysText = self.gpt_role.get(str(sno) + str(mode), '')
                gpt_reqText = self.gpt_req.get(str(sno) + str(mode), '')
                gpt_inpText = msg
                gpt_files   = self.webui_files[str(sno) + str(mode)]
                self.webui_files[str(sno) + str(mode)] = []

                if (sno == 1): # admin
                    interface  = 'web-admin'
                    session_id = 'admin'
                else:
                    interface = 'web-guest'
                    session_id = 'guest' + str(sno)
                    if (gpt_class != 'knowledge'):
                        gpt_class = 'chat'
                    if (gpt_class == 'knowledge'):
                        gpt_history = []

                gpt_proc = threading.Thread(target=self.chatproc.proc_gpt, args=(
                                            self.gpt_result_queue[str(sno) + str(mode)], None, {}, 
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
                    if (self.gpt_result_queue[str(sno) + str(mode)].qsize() >= 1):
                        break
                    time.sleep(0.25)

                while (self.gpt_result_queue[str(sno) + str(mode)].qsize() >= 1):
                    [res_name, res_value] = self.gpt_result_queue[str(sno) + str(mode)].get()
                    self.gpt_result_queue[str(sno) + str(mode)].task_done()
                    if (res_name=='_output_text_'):
                        text = res_value
                    if (res_name=='_input_path_'):
                        path = res_value
                    if (res_name=='[history]'):
                        self.gpt_histories[str(sno) + str(mode)] = res_value
                    time.sleep(0.25)

            # メッセージ保管
            message  = msg.replace('\n', '<br>')
            response = text.replace('\n', '<br>')
            if (path != ''):
                downloadLink = '/downloads/' + os.path.basename(path)
                isImage = path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

            try:
                self.webui_histories[str(sno) + str(mode)].append({'sender':'user', 'message': message, 'timestamp': timestamp, })
                self.webui_histories[str(sno) + str(mode)].append({'sender':'gpt' , 'message': response, 'timestamp': timestamp, 'downloadLink': downloadLink, "isImage": isImage})
            except:
                self.webui_histories[str(sno) + str(mode)] = []
                self.webui_histories[str(sno) + str(mode)].append({'sender':'user', 'message': message, 'timestamp': timestamp, })
                self.webui_histories[str(sno) + str(mode)].append({'sender':'gpt' , 'message': response, 'timestamp': timestamp, 'downloadLink': downloadLink, "isImage": isImage})

            return jsonify({
                "response": response,
                "timestamp": timestamp,
                "downloadLink": downloadLink,
                "isImage": isImage
            })

        @self.app.route('/chat/get_history', methods=['GET'])
        def get_history():
            client_ip = request.remote_addr
            mode = request.args.get('mode')
            qLog.log('info', self.proc_id, f"{client_ip} /chat/get_history?mode={mode}")

            sid = session.get('clipngpt_sid')
            if (not sid):
                return jsonify([])
            sno = self.webui_sid.get(sid)
            if (sid != self.webui_sno.get(sno)):
                return jsonify([])
            self.webui_last_access[sno] = time.time()

            return jsonify(self.webui_histories.get(str(sno) + str(mode), []))

        @self.app.route('/chat_setting', methods=['GET', 'POST'])
        def chat_setting():
            client_ip = request.remote_addr
            mode = request.args.get('mode')
            qLog.log('info', self.proc_id, f"{client_ip} /chat_setting?mode={mode}")

            sid = session.get('clipngpt_sid')
            if (not sid):
                return redirect(url_for('login'))
            sno = self.webui_sid.get(sid)
            if (sid != self.webui_sno.get(sno)):
                return redirect(url_for('login'))
            self.webui_last_access[sno] = time.time()
 
            if request.method == 'POST':
                action_type = request.form.get('action_type')
                if action_type == 'set_reset':

                    # Set
                    self.gpt_role[str(sno) + str(mode)] = request.form['role']
                    self.gpt_req[str(sno) + str(mode)]  = request.form['request']

                    # Reset
                    self.webui_histories[str(sno) + str(mode)] = []
                    self.gpt_histories[str(sno) + str(mode)]   = []

                elif action_type == 'cancel':
                    pass

                return redirect(url_for('chat', mode=mode))

            chat_class = self.gpt_ini_class.get(str(mode), '')
            role       = self.gpt_role.get(str(sno) + str(mode), '')
            req        = self.gpt_req.get(str(sno) + str(mode), '')
            return render_template('chat_setting.html', mode=mode, chat_class=chat_class, role=role, request=req, )

        @self.app.route('/upload/<mode>', methods=['POST'])
        def upload_file(mode):
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /upload")

            sid = session.get('clipngpt_sid')
            if (not sid):
                return jsonify([])
            sno = self.webui_sid.get(sid)
            if (sid != self.webui_sno.get(sno)):
                return jsonify([])
            self.webui_last_access[sno] = time.time()

            if 'file' not in request.files:
                return 'No file part'
            file = request.files['file']
            if file.filename == '':
                return 'No selected file'
            if file:
                filename = os.path.join(self.app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)

                self.webui_files[str(sno) + str(mode)].append(filename)

                # チャット履歴に追加する情報を用意
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = filename
                response = "ファイルを受信しました。"
                downloadLink = '/uploads/' + os.path.basename(filename)
                isImage = filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

                try:
                    self.webui_histories[str(sno) + str(mode)].append({'sender':'user', 'message': message, 'timestamp': timestamp, })
                    self.webui_histories[str(sno) + str(mode)].append({'sender':'gpt' , 'message': response, 'timestamp': timestamp, 'downloadLink': downloadLink, "isImage": isImage})
                except:
                    self.webui_histories[str(sno) + str(mode)] = []
                    self.webui_histories[str(sno) + str(mode)].append({'sender':'user', 'message': message, 'timestamp': timestamp, })
                    self.webui_histories[str(sno) + str(mode)].append({'sender':'gpt' , 'message': response, 'timestamp': timestamp, 'downloadLink': downloadLink, "isImage": isImage})

                # クライアントに返す情報
                return jsonify({
                    "response": response,
                    "timestamp": timestamp,
                    "downloadLink": downloadLink,
                    "isImage": isImage
                })

            return redirect(url_for('chat', **request.args))

        @self.app.route('/uploads/<filename>', methods=['GET'])
        def uploads_file(filename):
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /uploads/{filename}")

            sid = session.get('clipngpt_sid')
            if (not sid):
                return jsonify([])
            sno = self.webui_sid.get(sid)
            if (sid != self.webui_sno.get(sno)):
                return jsonify([])
            self.webui_last_access[sno] = time.time()

            return send_from_directory(self.app.config['UPLOAD_FOLDER'], filename, as_attachment=True if filename != 'dummy.png' else False)

        @self.app.route('/downloads/<filename>', methods=['GET'])
        def downloads_file(filename):
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /downloads/{filename}")

            sid = session.get('clipngpt_sid')
            if (not sid):
                return jsonify([])
            sno = self.webui_sid.get(sid)
            if (sid != self.webui_sno.get(sno)):
                return jsonify([])
            self.webui_last_access[sno] = time.time()

            return send_from_directory(self.app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True if filename != 'dummy.png' else False)

        @self.app.route('/synthesize_speech', methods=['POST'])
        def synthesize_speech():
            client_ip = request.remote_addr
            qLog.log('info', self.proc_id, f"{client_ip} /synthesize_speech")

            sid = session.get('clipngpt_sid')
            if (not sid):
                return jsonify([])
            sno = self.webui_sid.get(sid)
            if (sid != self.webui_sno.get(sno)):
                return jsonify([])
            self.webui_last_access[sno] = time.time()

            data = request.json
            text = data.get("speech_text")            
            text = text.replace('<br>', '\n')
            t    = text.split('\n')
            if (len(t) > 1):
                if (t[0][:1] == '['):
                    del t[0]
                    text = '\n'.join(t)

            # 出力ファイル
            self.tts_seq += 1
            if (self.tts_seq > 9999):
                self.tts_seq = 1
            seq4 = '{:04}'.format(self.tts_seq)
            outFile = qPath_work + 'webui_tts' + '.' + seq4 + '.mp3'

            if (os.path.isfile(outFile)):
                try:
                    os.remove(outFile)
                except Exception as e:
                    print(e)

            # gttsを使用してテキストを音声に変換
            tts = gTTS(text=text, lang='ja', slow=False)
            tts.save(outFile)

            # ファイルからデータを読み込む
            with open(outFile, 'rb') as f:
                audio_data = f.read()

            # MP3データをbase64レスポンスとして返す
            return Response(base64.b64encode(audio_data),  mimetype="text/plain")

if __name__ == '__main__':

    webui = _webui()

    base_path = os.path.dirname(sys.argv[0]) + '/'
    webui.init(qLog_fn='', runMode='debug', limit_mode=False, 
               conf=None, chatbot=None, chatproc=None,
               flask_base=base_path, )
    webui.flask_start()

    time.sleep(300)


