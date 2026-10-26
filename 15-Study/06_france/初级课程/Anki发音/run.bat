@echo off
chcp 65001 >nul
cd /d "%~dp0"
uv run --with edge-tts==7.3.1 python add_audio.py %*
