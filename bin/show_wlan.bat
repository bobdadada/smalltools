@echo off

chcp 65001

:wlan
set /p i="请输入WLAN名称："
::输入WIFI名称(SSID)
netsh wlan show profiles name=%i% key=clear
pause > nul
goto wlan