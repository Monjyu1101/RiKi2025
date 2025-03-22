#/usr/bin/env zsh

    python -m pip freeze     > requirements.txt
    python -m pip uninstall -r requirements.txt -y

    ping localhost -W 1000 -c 5 >nul

    python -m pip  list
