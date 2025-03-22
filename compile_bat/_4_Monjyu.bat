@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

cd ".."

ECHO; ���[�N�폜
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



ECHO;
ECHO -------
ECHO compile
ECHO -------

set pyname=RiKi_Monjyu
    echo;
    echo %pyname%.py
       pyinstaller %pyname%.py  -F --log-level ERROR --icon="_icons/%pyname%.ico"

IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\_���L\Worker\%pyname%.exe"
    copy "%pyname%.exe"        "C:\_���L\Monjyu\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
rem del  "%pyname%.exe"



set pyname=RiKi_Monjyu_debug
    echo;
    echo %pyname%.py
       pyinstaller %pyname%.py  -F --log-level ERROR

IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
rem copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
rem copy "%pyname%.exe"        "C:\_���L\Worker\%pyname%.exe"
rem copy "%pyname%.exe"        "C:\_���L\Monjyu\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
rem del  "%pyname%.exe"



ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
IF EXIST "temp"                                RD "temp"                                /s /q
IF EXIST "_cache"                              RD "_cache"                              /s /q
IF EXIST "C:\RiKi_assistant\temp"              RD "C:\RiKi_assistant\temp"              /s /q
IF EXIST "C:\RiKi_assistant\_cache"            RD "C:\RiKi_assistant\_cache"            /s /q
IF EXIST "C:\_���L\Worker\temp"                RD "C:\_���L\Worker\temp"                /s /q
IF EXIST "C:\_���L\Worker\_cache"              RD "C:\_���L\Worker\_cache"              /s /q
PAUSE



