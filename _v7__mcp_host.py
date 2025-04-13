"""
MCP サーバー管理
MCPサーバーを動的にロードして実行するMCPホストです。
複数のMCPサーバーを同時に管理できます。
"""
import asyncio
import importlib
import json
import os
import sys
import logging
from typing import Any, Dict, List, Optional
# MCP クライアント関連のインポート
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

# モジュール名定義
MODULE_NAME = 'mcp_host'

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)-16s - %(levelname)-8s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(MODULE_NAME)


class mcp_host_class:
    """MCPサーバーを起動・管理するクラス"""

    def __init__(self):
        """MCPサーバー管理インスタンスの初期化"""
        logger.debug("MCPサーバー管理を初期化")
        self.exit_stack = AsyncExitStack()
        self.servers_info: Dict[str, Dict[str, Any]] = {}
        self.tools_info: Dict[str, Dict[str, Any]] = {}
        
    def _parms_to_args(self, parms: List[str]):
        """コマンドライン引数をキーワード引数に変換"""
        args = {}
        
        try:
            if parms:
                i = 0
                logger.info(f"引数変換: 引数数={len(parms)}")
                while i < len(parms):
                    if parms[i].startswith('--'):
                        key = parms[i][2:]  # '--'を削除
                        if i + 1 < len(parms) and not parms[i+1].startswith('--'):
                            # 次の引数が値の場合
                            try:
                                # 数値変換を試みる
                                value = int(parms[i+1])
                                logger.info(f"引数変換: {key}={value} (整数)")
                            except ValueError:
                                try:
                                    # 浮動小数点変換を試みる
                                    value = float(parms[i+1])
                                    logger.info(f"引数変換: {key}={value} (浮動小数点)")
                                except ValueError:
                                    # 文字列のまま
                                    value = parms[i+1]
                                    logger.info(f"引数変換: {key}={value} (文字列)")
                            args[key] = value
                            i += 2
                        else:
                            # フラグオプション（値なし）
                            args[key] = True
                            logger.info(f"引数変換: {key}=True (フラグ)")
                            i += 1
                    else:
                        # '--'で始まらない引数はスキップ
                        logger.info(f"引数変換: スキップ '{parms[i]}'")
                        i += 1
        except Exception as e:
            logger.error(f"引数の変換中にエラーが発生しました: {e}")
            return {}
            
        return args

    async def start_module(self, module_path: str, parms: Optional[List[str]] = None, env: Optional[Dict[str, str]] = None, reset: bool = False) -> bool:
        """指定されたモジュールをインポートして実行"""
        # 既存セッションのリセット
        if reset and self.servers_info:
            logger.debug("既存セッションをリセットします")
            await self.terminate()

        # モジュール名を取得
        module_name = os.path.splitext(os.path.basename(module_path))[0]
        parms_str = " ".join(parms) if parms else ""
        logger.debug(f"モジュール名: {module_name}")
        if parms:
            logger.debug(f"引数: {parms_str}")

        # 引数変換
        args = self._parms_to_args(parms)
        logger.debug(f"変換後の引数: {args}")
       
        try:
            # モジュールロード
            logger.info(f"モジュールのロードを開始: {module_path}")
            loader = importlib.machinery.SourceFileLoader(module_name, module_path)
            if loader is None:
                logger.error(f"{module_name} が見つかりませんでした")
                return False
                
            # 環境変数設定
            process_env = os.environ.copy()
            if env:
                process_env.update(env)
                logger.debug(f"環境変数を更新: 追加数={len(env)}")

            # モジュール実行
            module = loader.load_module()
            sys.modules[module_name] = module
            logger.debug(f"モジュール {module_name} をロードしました")

            # タスク作成
            try:
                loader.exec_module(module)
                logger.debug(f"モジュール {module_name} を実行します")
                server_task = asyncio.create_task(module.main(**args))
                logger.debug(f"モジュール {module_name} のタスクを作成しました: task_id={id(server_task)}")
            except TypeError as e:
                logger.error(f"{module_name}.main の呼び出しが失敗しました: {e}")
                return False
            
            # SSE接続設定
            port = args.get("port", "8001")
            server_url = f"http://127.0.0.1:{port}/sse"
            logger.debug(f"SSEサーバーURL: {server_url}")

            # SSEストリーム開始
            streams_ctx = sse_client(url=server_url)
            streams = await streams_ctx.__aenter__()
            logger.debug("SSEストリームを開始しました")

            # セッション開始
            session_ctx = ClientSession(*streams)
            session: ClientSession = await session_ctx.__aenter__()
            logger.debug("セッションを開始しました")

            # 初期化待機
            logger.debug("接続の初期化中...")
            await asyncio.sleep(5)

            # ツール初期化
            if not await self._initialize_tools(module_name, session):
                logger.error(f"{module_name} のツール初期化に失敗しました")
                return False

            # サーバー情報記録
            server_info = {"name": module_name,
                           "type": "import", 
                           "module": module, 
                           "port": args.get('port'), 
                           "server_task": server_task, 
                           "streams_ctx": streams_ctx, 
                           "streams": streams, 
                           "session_ctx": session_ctx, 
                           "session": session, 
                           "args": args, 
                           "env": env}
            self.servers_info[module_name] = server_info
            logger.info(f"モジュールを起動しました: {module_name}")
            
            return True
        
        except Exception as e:
            logger.error(f"{module_name} の実行中にエラーが発生しました: {e}")
            return False
             
    async def start_script(self, script_path: str, parms: Optional[List[str]] = None, 
                          env: Optional[Dict[str, str]] = None, reset: bool = False) -> bool:
        """外部スクリプトとしてサーバーを起動"""
        # 既存セッションのリセット
        if reset and self.servers_info:
            logger.debug("既存セッションをリセットします")
            await self.terminate()

        # サーバー名を取得
        server_name = os.path.splitext(os.path.basename(script_path))[0]
        parms_str = " ".join(parms) if parms else ""
        logger.debug(f"スクリプト名: {server_name}")
        if parms:
            logger.debug(f"引数: {parms_str}")

        # 引数変換
        args = self._parms_to_args(parms)
        logger.debug(f"変換後の引数: {args}")

        try:
            logger.info(f"スクリプトを開始: {script_path}")
            # ファイル存在確認
            if not os.path.exists(script_path):
                logger.error(f"スクリプト '{script_path}' が見つかりません")
                return False
          
            # パラメータ作成
            process_env = os.environ.copy()
            if env:
                process_env.update(env)
                logger.debug(f"環境変数を更新: 追加数={len(env)}")

            # サーバーパラメータ設定
            server_params = StdioServerParameters(
                command=sys.executable,
                args=[script_path] + (parms or []),
                env=process_env
            )
            logger.debug(f"Stdioパラメータを作成しました")

            # タスク作成と実行
            self.servers_info[server_name] = {'server_task': None}
            server_task = asyncio.create_task(self._start_stdio(server_name, server_params, args, env))
            self.servers_info[server_name]['server_task'] = server_task
            logger.debug(f"{server_name} の起動タスクを作成しました: task_id={id(server_task)}")

            logger.info(f"スクリプトを起動しました: {server_name}")
            return True
            
        except Exception as e:
            logger.error(f"{server_name} の実行中にエラーが発生しました: {e}")
            return False

    async def _start_stdio(self, server_name, server_params, args, env):
        """Stdioベースのサーバーを起動する内部処理"""
        try:
            # ストリーム初期化
            streams_ctx = stdio_client(server_params)
            streams = await self.exit_stack.enter_async_context(streams_ctx)
            logger.debug("Stdioストリームを開始しました")

            # セッション初期化
            session_ctx = ClientSession(*streams)
            session: ClientSession = await self.exit_stack.enter_async_context(session_ctx)
            logger.debug("セッションを開始しました")

            # ツール初期化
            if not await self._initialize_tools(server_name, session):
                logger.error(f"{server_name} のツール初期化に失敗しました")
                return False
            
            # サーバー情報記録
            server_info = {"name": server_name,
                            "type": "python", 
                            "module": None, 
                            "port": None, 
                            "server_task": None, 
                            "streams_ctx": streams_ctx, 
                            "streams": streams, 
                            "session_ctx": session_ctx, 
                            "session": session, 
                            "args": args, 
                            "env": env}
            self.servers_info[server_name] = server_info
            logger.debug(f"{server_name} の情報を記録しました")
            return True

        except Exception as e:
            logger.error(f"{server_name} の起動中にエラーが発生しました: {e}")
            return False

    async def start_from_config(self, config_path: str, reset: bool = True) -> bool:
        """JSON設定ファイルからサーバーを起動"""
        try:
            logger.info(f"JSON設定ファイル '{config_path}' のロード開始...")
            
            # ファイル存在確認
            if not os.path.exists(config_path):
                logger.error(f"JSON設定ファイル '{config_path}' が見つかりません。")
                return False
            
            # 既存セッションリセット
            if reset and self.servers_info:
                logger.debug("既存セッションをリセットします")
                await self.terminate()
            
            # 設定読み込み
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.debug(f"JSON設定ファイルを読み込みました: {config_path}")
            
            # 設定内容確認
            if 'mcpServers' not in config:
                logger.error("JSON設定ファイルに 'mcpServers' セクションがありません。")
                return False
            
            # サーバー起動処理
            for server_name, server_config in config['mcpServers'].items():
                logger.info(f"サーバー '{server_name}' を起動中...")
                
                # 必須パラメータ確認
                if 'command' not in server_config or 'args' not in server_config:
                    logger.error(f"サーバー '{server_name}' の設定に 'command' または 'args' が不足しています。")
                    continue
                               
                # 環境変数設定
                env = server_config.get('env', {})
                process_env = os.environ.copy()
                if env:
                    process_env.update(env)
                    logger.debug(f"環境変数を更新: 追加数={len(env)}")

                # OS別パラメータ設定
                if sys.platform != "win32":
                    server_params = StdioServerParameters(
                        command=server_config['command'],
                        args=server_config['args'],
                        env=process_env
                    )
                    logger.debug(f"非Windows向けサーバーパラメータを作成: {server_config['command']}")
                else:
                    server_params = StdioServerParameters(
                        command='cmd',
                        args=['/c', server_config['command']] + server_config['args'],
                        env=process_env
                    )
                    logger.debug(f"Windows向けサーバーパラメータを作成: cmd /c {server_config['command']}")

                # タスク作成と実行
                self.servers_info[server_name] = {'server_task': None}
                server_task = asyncio.create_task(self._start_stdio(server_name, server_params, {}, env))
                self.servers_info[server_name]['server_task'] = server_task
                logger.info(f"サーバー '{server_name}' を起動しました: task_id={id(server_task)}")
            
            logger.info("JSON設定ファイルのロード完了")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON設定ファイル '{config_path}' の解析エラー: {e}")
            if reset:
                await self.terminate()
            return False
            
        except Exception as e:
            logger.error(f"JSONファイルからのロード中にエラーが発生しました: {e}")
            if reset:
                await self.terminate()
            return False

    async def _initialize_tools(self, server_name: str, session: ClientSession) -> bool:
        """サーバーの初期化とツール情報の登録"""
        try:
            # サーバー初期化
            result = await session.initialize()
            logger.info(f"サーバー '{server_name}' の初期化が完了しました")

            # 既存ツール情報の削除
            await self._remove_tools(server_name)
            
            # ツール情報取得と登録
            result = await session.list_tools()
            tool_count = 0
            for tool in result.tools:
                full_name = f"{server_name}-{tool.name}"
                self.tools_info[full_name] = {
                    "full_name": full_name, 
                    "session": session,
                    "server": server_name, 
                    "tool": tool.name,
                    "description": tool.description, 
                    "inputSchema": tool.inputSchema,
                }
                logger.info(f"ツール '{full_name}' を登録しました")
                tool_count += 1
            
            logger.debug(f"サーバー '{server_name}' から {tool_count} 個のツールを登録しました")
            return True
            
        except Exception as e:
            logger.error(f"サーバー '{server_name}' の初期化中にエラー: {e}")
            return False

    async def _remove_tools(self, server_name: str) -> None:
        """サーバーに関連するツール情報を削除"""
        prefix = f"{server_name}-"
        keys_to_remove = [key for key in self.tools_info.keys() if key.startswith(prefix)]
        
        for key in keys_to_remove:
            del self.tools_info[key]
            logger.debug(f"ツール '{key}' を削除しました")
        
        if keys_to_remove:
            logger.debug(f"サーバー '{server_name}' の関連ツール ({len(keys_to_remove)}個) を削除しました")

    async def execute(self, tool_name: str, request_json: Optional[str] = None) -> Any:
        """指定されたツールを実行"""
        logger.info(f"ツールの実行: {tool_name}")
        
        # 前提条件チェック
        if not self.tools_info:
            logger.error("ツール情報がありません。")
            return None
        
        if tool_name not in self.tools_info:
            logger.error(f"ツール '{tool_name}' は登録されていません")
            return None
        
        # パラメータ解析
        args = {}
        if request_json:
            try:
                args = json.loads(request_json)
                logger.debug(f"パラメータを解析しました: {args}")
            except json.JSONDecodeError as e:
                logger.error(f"パラメータJSON解析エラー: {e}")
                return None
        
        # ツール実行
        try:
            tool_info = self.tools_info[tool_name]
            session = tool_info["session"]
            tool = tool_info["tool"]
            logger.debug(f"ツール '{tool}' を実行します")
            
            call_result = await session.call_tool(tool, args)
            
            if call_result and call_result.content and call_result.content:
                result = call_result.content[0].text
                logger.info("ツールの実行が完了しました")
                return result
            else:
                logger.warning(f"ツール '{tool_name}' の実行結果が空でした")
                return None
        except Exception as e:
            logger.error(f"ツール '{tool_name}' の実行中にエラー: {e}")
            return None

    async def terminate(self):
        """全てのMCPサーバーを停止"""
        logger.info("すべてのMCPサーバーの終了を開始します")

        if not self.servers_info:
            logger.warning("終了するMCPサーバーがありません")
            return

        try:
            if hasattr(self, 'exit_stack'):
                logger.debug("exit_stackの終了処理を開始します")
                await asyncio.wait_for(self.exit_stack.aclose(), timeout=2)
                logger.debug("exit_stackの終了処理が完了しました")
        except asyncio.TimeoutError:
            logger.warning("exit_stackの終了処理がタイムアウトしました")
        except Exception as e:
            logger.error(f"exit_stack終了処理中にエラー: {e}")

        # 全タスクのクリーンアップ
        for key, server_info in list(self.servers_info.items()):
            name = server_info.get('name', key)
            server_task = server_info.get('server_task')
            session = server_info.get('session')
            session_ctx = server_info.get('session_ctx')
            streams = server_info.get('streams')
            streams_ctx = server_info.get('streams_ctx')
                          
            logger.debug(f"{name} を停止します...")

            try:
                # セッションクリーンアップ
                if session_ctx:
                    logger.debug(f"{name} のセッションをクローズします")
                    try:
                        await asyncio.wait_for(session_ctx.__aexit__(None, None, None), timeout=2)
                        logger.debug(f"{name} のセッション終了処理が完了しました")
                    except asyncio.TimeoutError:
                        logger.warning(f"{name} のセッション終了処理がタイムアウトしました")

                # ストリームクリーンアップ
                if streams_ctx:
                    logger.debug(f"{name} のストリームをクローズします")
                    try:
                        await asyncio.wait_for(streams_ctx.__aexit__(None, None, None), timeout=2)
                        logger.debug(f"{name} のストリーム終了処理が完了しました")
                    except asyncio.TimeoutError:
                        logger.warning(f"{name} のストリーム終了処理がタイムアウトしました")

                # タスクキャンセル
                if server_task:
                    try:
                        logger.debug(f"{name} のタスクをキャンセルします")
                        server_task.cancel()
                        await asyncio.wait_for(server_task, timeout=3.0)
                        logger.debug(f"{name} のタスクが正常にキャンセルされました")
                    except asyncio.TimeoutError:
                        logger.warning(f"{name} のタスクがタイムアウトしました - 強制終了します")
                    except asyncio.CancelledError:
                        logger.debug(f"{name} のタスクが正常にキャンセルされました")

            except Exception as e:
                logger.error(f"{name} の停止中にエラー: {e}")
                    
            logger.debug(f"{name} を停止しました")
        
        logger.info(f"全てのMCPサーバーが停止しました")

        # 管理情報のクリア
        self.servers_info = {}
        self.tools_info = {}

        # 終了待機
        logger.debug("プログラムを正常に終了します")
        await asyncio.sleep(2)
