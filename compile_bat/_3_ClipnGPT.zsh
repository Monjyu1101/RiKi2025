#/usr/bin/env zsh

    python -m pip  install --upgrade pip
    python -m pip  install --upgrade wheel
    python -m pip  install --upgrade setuptools
    python -m pip  install --upgrade pyinstaller

    python -m pip  install --upgrade screeninfo
    python -m pip  install --upgrade pyautogui
    python -m pip  install --upgrade pywin32
    python -m pip  install --upgrade psutil
    python -m pip  install --upgrade rainbow-logging-handler
    python -m pip  install --upgrade pycryptodome
    python -m pip  install --upgrade pygame
    python -m pip  install --upgrade pynput

rem python -m pip  install --upgrade numpy
    python -m pip  install --upgrade numpy==1.26.4
rem python -m pip  install --upgrade opencv-python==4.6.0.66
rem python -m pip  install --upgrade opencv-contrib-python==4.6.0.66
    python -m pip  install --upgrade opencv-python==4.9.0.80
    python -m pip  install --upgrade opencv-contrib-python==4.9.0.80

    python -m pip  install --upgrade pysimplegui
    python -m pip  install --upgrade pillow
    python -m pip  install --upgrade flask

    python -m pip  install --upgrade httpx
    python -m pip  install --upgrade tiktoken
    python -m pip  install --upgrade openai
    python -m pip  install --upgrade anthropic
    python -m pip  install --upgrade google.generativeai
    python -m pip  install --upgrade ollama

    python -m pip  install --upgrade pyperclip
    python -m pip  install --upgrade selenium
    python -m pip  install --upgrade bs4
    python -m pip  install --upgrade pdfminer.six
    python -m pip  install --upgrade pyocr
    python -m pip  install --upgrade pygame
rem python -m pip  install --upgrade wave
rem python -m pip  install --upgrade chardet
    python -m pip  install --upgrade botocore

    python -m pip  install --upgrade pandas
    python -m pip  install --upgrade openpyxl
    python -m pip  install --upgrade pyodbc
    python -m pip  install --upgrade sqlalchemy
    python -m pip  install --upgrade matplotlib
    python -m pip  install --upgrade seaborn

    python -m pip  install --upgrade gtts
    python -m pip  uninstall -y gtts-token
    python -m pip  install --upgrade gtts-token
rem python -m pip  install --upgrade googletrans
    python -m pip  install --upgrade goslate
    python -m pip  install --upgrade ggtrans

    python -m pip  install --upgrade pyaudio
    python -m pip  install --upgrade speechrecognition



    pyinstaller RiKi_ClipnGPT.py  -F --log-level ERROR --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --icon="_icons/RiKi_ClipnGPT.ico"

