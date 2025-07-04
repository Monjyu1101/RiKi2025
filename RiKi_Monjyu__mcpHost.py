#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/monjyu1101
# Thank you for keeping the rules.
# ------------------------------------------------

# モジュール名
MODULE_NAME = 'mcpHost'

# ロガーの設定
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)-10s - %(levelname)-8s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(MODULE_NAME)


import asyncio
import datetime
import json
import os
import time
import threading
import queue
from typing import Any, Dict, List, Any, Optional, Tuple, Union

# インターフェースのパス設定
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# MCPクライアントのインポート
import _v7__mcp_host
mcp_host = _v7__mcp_host.mcp_host_class()

# MCP管理クラス
class _mcpHost_class:

    # 初期化
    def __init__(self,  runMode: str = 'debug', qLog_fn: str = '', 
                        main=None, conf=None, data=None, addin=None, botFunc=None):
        logger.debug("(Host) 初期化開始...")
        
        self.runMode = runMode
        
        # ログファイル名の生成
        if qLog_fn == '':
            nowTime = datetime.datetime.now()
            qLog_fn = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'

        # 設定パラメータの保存
        self.main       = main
        self.conf       = conf
        self.data       = data
        self.addin      = addin
        self.botFunc    = botFunc

        # キュー設定
        self.req_s = queue.Queue()
        self.res_r = queue.Queue()
        
        # MCP機能モジュール取得
        self.last_modules = None

        logger.debug("(Host) 初期化完了")

    def json_check(self, input_string: str) -> Tuple[bool, Union[Dict[str, Any], str]]:
        """
        文字列がJSON形式かチェックし、適切な形式で返却するシンプルなサブルーチン
        
        Args:
            input_string (str): チェックする文字列
        
        Returns:
            Tuple[bool, Union[Dict[str, Any], str]]: 
                - JSON型 → (True, dict)
                - list型で内容がjson → (True, {"data1": 内容, "data2": 内容, ...})
                - list型で内容が文字列 → (True, {"data1": 文字列, "data2": 文字列, ...})
                - 以外 → (False, 元の文字列)
        """
        # 空文字やNoneの場合は失敗として扱う
        if not input_string or not isinstance(input_string, str):
            return False, input_string
        
        # 文字列の前後の空白を除去
        cleaned_string = input_string.strip()
        
        try:
            # JSONとしてパース試行
            parsed_data = json.loads(cleaned_string)
            
            # 1) JSON型（辞書）の場合
            if isinstance(parsed_data, dict):
                return True, parsed_data
            
            # 2) list型の場合
            elif isinstance(parsed_data, list):
                # リストの内容を"datan"形式のdictに変換
                result_dict = {}
                for i, item in enumerate(parsed_data, 1):
                    result_dict[f"data{i}"] = item
                return True, result_dict
            
            # 3) その他の型（数値、真偽値、null等）
            else:
                return False, input_string
                
        except json.JSONDecodeError:
            # JSONパースに失敗した場合
            return False, input_string

    # MCP機能モジュール取得
    def get_mcp_modules(self):
        if self.last_modules is not None:
            return self.last_modules

        logger.debug("(Host) 機能モジュール取得開始...")
        
        modules = {}
        for name, value in mcp_host.tools_info.items():
            try:
                # parameters
                parameters = value.get('inputSchema')

                # $schema 削除
                try:
                    del parameters['$schema']
                except:
                    pass

                # additionalProperties 削除
                try:
                    if (parameters['additionalProperties'] == False):
                        del parameters['additionalProperties']
                except:
                    pass

                # 空 required 削除 #geminiエラー対策
                try:
                    if (parameters['required'] == []):
                        del parameters['required']
                except:
                    pass

                # title 削除
                if False:
                    try:
                        del parameters['title']
                    except:
                        pass
                    try:
                        properties = parameters.get('properties', {})
                        for field in properties:
                            try:
                                del properties[field]['title']
                            except:
                                pass
                    except:
                        pass

                #print(parameters)

                # function
                function = {
                        "name": name,
                        "description": value.get('description'),
                        "parameters": parameters
                        }

                server = mcp_host.servers_info[value.get('server')]
                server_name = server.get('name')
                modules[name] = { 'script': 'mcp',
                                    'module': server_name,
                                    'onoff': 'on',
                                    'class': None,
                                    'func_name': name,
                                    'func_ver': '1.0.0',
                                    'func_auth': 'ok',
                                    'function': function,
                                    'func_reset': None,
                                    'func_proc': self.execute}
            except Exception as e:
                logger.error(f"(Host) 機能モジュール取得エラー: {e}")
            
        logger.debug(f"(Host) 機能モジュール取得完了: {len(modules)}件")

        self.last_modules = modules
        return modules

    # MCPツール実行関数
    def execute(self, tool_name: str , request_json: Optional[str] = None):
        logger.info(f"(Host) ツール実行: '{tool_name}'")
        
        # 残っているレスポンスを消化
        while not self.res_r.empty():
            res = self.res_r.get()
            logger.debug(f"(Host) 残存レスポンス: {res}")

        # 実行リクエスト送信
        self.req_s.put({'cmd': 'execute', 'tool_name': tool_name, 'request_json':request_json})

        # 結果待ち（タイムアウト120秒）
        result = None
        chkTime = time.time()
        while (time.time() - chkTime) < 120:
            if not self.res_r.empty():
                result = self.res_r.get()
                break

        if not result:
            logger.error("(Host) ツール実行タイムアウト")
            result = {'error': 'time out!'}
            return json.dumps(result, ensure_ascii=False)

        try:
            logger.debug(f"(Host) ツール実行結果: {result[:100]}...")

            # チェック
            is_json, json_data = self.json_check(result)
            if is_json:
                return json.dumps(json_data, ensure_ascii=False)
            else:
                logger.debug("(Host) JSON解析失敗、文字列として返却")
                res_dic = {'result': result}
                return json.dumps(res_dic, ensure_ascii=False)

        except Exception as e:
            logger.error(f"(Host) executeエラー: {e}")
            res_dic = {'result': 'error!'}
            return json.dumps(res_dic, ensure_ascii=False)

    # MCP停止
    def terminate(self):
        logger.info("(Host) 停止: terminate")
        self.last_modules = None

        # 開始コマンド送信
        self.req_s.put({'cmd': 'terminate'})
        logger.info("(Host) 停止コマンド送信")

        # 結果待ち（タイムアウト120秒）
        result = None
        chkTime = time.time()
        while (time.time() - chkTime) < 120:
            if not self.res_r.empty():
                result = self.res_r.get()
                break

    # MCP実行
    def run(self):
        logger.info("(Host) 起動: run")
        self.last_modules = None

        # MCPプロセス実行関数
        def mcp_proc(req_s, res_r, config_json_path, mcp_servers_path):
            asyncio.run(main(req_s, res_r, config_json_path, mcp_servers_path))

        # スレッド起動
        config_json_path = '_config/claude_desktop_config.json'
        mcp_servers_path = '_extensions/mcp/'
        mcp_thread = threading.Thread(target=mcp_proc, args=(self.req_s, self.res_r, config_json_path, mcp_servers_path))
        mcp_thread.start()

        if False:

            # 残っているレスポンスを消化
            while not self.res_r.empty():
                res = self.res_r.get()
                logger.debug(f"(Host) 残存レスポンス: {res}")

            # 開始コマンド送信
            self.req_s.put({'cmd': 'start'})
            logger.info("(Host) 開始コマンド送信")

            # 結果待ち（タイムアウト120秒）
            result = None
            chkTime = time.time()
            while (time.time() - chkTime) < 120:
                if not self.res_r.empty():
                    result = self.res_r.get()
                    break


# メインループ処理
async def main( req_q, res_q,
                config_json_path='_config/claude_desktop_config.json',
                mcp_servers_path='_extensions/mcp/'):
    logger.debug("(Host) メインループ開始")

    # 起動状態
    isRunning = False

    # フォルダ内容、前回値
    previous_state = None
    last_check_time = time.time()
    update_time = None

    while True:
        try:

            # フォルダ監視と再起動
            req_cmd = None
            if req_q.empty():
                await asyncio.sleep(0.25)

                # フォルダの確認は3秒間隔
                if ((time.time() - last_check_time) > 3):
                    last_check_time = time.time()

                    # フォルダ内容取得
                    current_state = {}
                    if os.path.isdir(mcp_servers_path):
                        for item in os.listdir(mcp_servers_path):
                            item_path = os.path.join(mcp_servers_path, item)
                            current_state[item] = os.path.getmtime(item_path)

                    # フォルダ変化確認
                    update_folder = False
                    if previous_state is None:
                        update_folder = True    # 初回
                        update_time = time.time()
                    else:
                        # 変更を検出
                        for item, mtime in current_state.items():
                            if item not in previous_state:
                                update_folder = True    # 新規
                            elif mtime != previous_state[item]:
                                update_folder = True    # 更新
                        # 削除されたアイテムを検出
                        for item in previous_state:
                            if item not in current_state:
                                update_folder = True    # 削除
                    # 状態を更新
                    previous_state = current_state
                    if update_folder:
                        update_time = time.time()

                    # 更新を通知（更新中を考慮、15秒遅らせる）
                    if (update_time is not None):
                        if ((time.time() - update_time) > 15):
                            logger.info("(Host) ★★★ update folder! (15s) ★★★")
                            update_time = None

                            # MCP終了
                            if isRunning:
                                logger.info("(Host) 終了処理中...")

                                mcp_host.runTerminate = True   #終了処理状況
                                result = await mcp_host.terminate()

                                # 終了処理中待機 180s
                                chkTime = time.time()
                                while ((time.time() - chkTime) < 180) and (mcp_host.runTerminate == True):
                                    await asyncio.sleep(1)

                                logger.info("(Host) 終了処理完了")
                                isRunning = False

                            req_cmd = 'start'

            # コマンド受信
            if req_cmd is None:
                if not req_q.empty():
                    req_dic = req_q.get()
                    req_cmd = req_dic.get('cmd')
                    logger.debug(f"(Host) コマンド受信: cmd='{req_cmd}' ")

            # コマンド処理
            if req_cmd is not None:
                if (req_cmd == 'start'):
                    logger.info(f"(Host) 起動処理: config_json='{config_json_path}' ")
                    await mcp_host.start_from_config(config_json_path=config_json_path, reset=True)
                    
                    #module_path = '_extensions/mcp/helloworld.py'
                    #parms = ['--port', '5001']
                    #await mcp_host.start_module(module_path=module_path, parms=parms)
                    
                    #script_path = '_extensions/mcp/helloworld.py'
                    #parms = []
                    #await mcp_host.start_script(script_path=script_path)

                    logger.info(f"(Host) 起動処理: servers_path='{mcp_servers_path}' ")
                    await mcp_host.start_from_path(mcp_servers_path=mcp_servers_path)

                    isRunning = True
                    res_q.put(True)

                elif (req_cmd == 'terminate'):
                    logger.info("(Host) 終了処理中...")

                    mcp_host.runTerminate = True   #終了処理状況
                    result = await mcp_host.terminate()

                    # 終了処理中待機 180s
                    chkTime = time.time()
                    while ((time.time() - chkTime) < 180) and (mcp_host.runTerminate == True):
                        await asyncio.sleep(1)

                    logger.info("(Host) 終了処理完了")
                    isRunning = False
                    res_q.put(result)

                elif (req_cmd == 'execute'):
                    tool_name = req_dic.get('tool_name')
                    request_json = req_dic.get('request_json')
                    logger.debug(f"(Host) ツール実行: name='{tool_name}' ")
                    result = await mcp_host.execute(tool_name=tool_name, request_json=request_json)
                    res_q.put(result)

                else:
                    logger.error(f"(Host) 予期しないコマンド: {req_dic}")

        except Exception as e:
            logger.error(f"(Host) メインループエラー: {e}")


# メイン処理
if __name__ == '__main__':
    print()
    logger.info("【テスト開始】")
    
    # インスタンス生成
    runMode = 'debug'
    mcpHost = _mcpHost_class(runMode=runMode, qLog_fn='')

    # MCP実行
    mcpHost.run()

    time.sleep(40)

    # テスト用コード

    logger.info("【モジュール一覧取得】")
    mcp_modules = mcpHost.get_mcp_modules()
    for mcp_module in mcp_modules:
        print(mcp_module)

    logger.info("【ツール実行】")
    tool_name = "filesystem-list_directory"
    request = {"path": "C:/_共有/_sandbox"}
    request_json = json.dumps(request, ensure_ascii=False)
    json_str = mcpHost.execute(tool_name=tool_name, request_json=request_json)

    parsed = json.loads(json_str)
    formatted_json = json.dumps(parsed, indent=4, ensure_ascii=False)
    print(formatted_json)

    # テスト実行待機
    time.sleep(120)
