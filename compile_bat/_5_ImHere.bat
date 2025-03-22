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
ECHO -----
ECHO tools
ECHO -----
rem           pip  install --upgrade pip
    python -m pip  install --upgrade pip
    python -m pip  install --upgrade wheel
    python -m pip  install --upgrade setuptools
    python -m pip  install --upgrade pyinstaller

ECHO;
ECHO -------
ECHO etc
ECHO -------
    python -m pip  install --upgrade keyboard
rem python -m pip  install --upgrade mouse �g�p�֎~
    python -m pip  install --upgrade screeninfo
    python -m pip  install --upgrade pyautogui
    python -m pip  install --upgrade pywin32
    python -m pip  install --upgrade comtypes
    python -m pip  install --upgrade psutil
    python -m pip  install --upgrade rainbow-logging-handler
    python -m pip  install --upgrade pycryptodome
rem python -m pip  install --upgrade pygame
    python -m pip  install --upgrade playsound3
rem python -m pip  install --upgrade pynput �g�p�֎~!

    python -m pip  install --upgrade numpy
rem python -m pip  install --upgrade numpy==2.2.0
rem python -m pip  install --upgrade opencv-python
rem python -m pip  install --upgrade opencv-contrib-python
rem python -m pip  install --upgrade opencv-python==4.9.0.80
rem python -m pip  install --upgrade opencv-contrib-python==4.9.0.80
    python -m pip  install --upgrade opencv-python==4.10.0.84
    python -m pip  install --upgrade opencv-contrib-python==4.10.0.84

rem python -m pip  install --upgrade pysimplegui
    python -m pip  install --upgrade pillow



ECHO;
ECHO -------
ECHO compile
ECHO -------

set pyname=RiKi_ImHere24
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR --icon="_icons/%pyname%.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\_���L\Player\%pyname%.exe"
    copy "%pyname%.exe"        "C:\_���L\Worker\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
rem del  "%pyname%.exe"



ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
IF EXIST "C:\RiKi_assistant\temp"         RD "C:\RiKi_assistant\temp"         /s /q
IF EXIST "C:\RiKi_assistant\_cache"       RD "C:\RiKi_assistant\_cache"       /s /q
IF EXIST "C:\_���L\Player\temp"           RD "C:\_���L\Player\temp"           /s /q
IF EXIST "C:\_���L\Player\_cache"         RD "C:\_���L\Player\_cache"         /s /q
IF EXIST "C:\_���L\Worker\temp"           RD "C:\_���L\Worker\temp"           /s /q
IF EXIST "C:\_���L\Worker\_cache"         RD "C:\_���L\Worker\_cache"         /s /q
PAUSE



