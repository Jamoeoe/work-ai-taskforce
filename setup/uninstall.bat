cd %~dp0
cd ..

REM delete .env
del ".env"

REM uninstall python, delete venv
winget uninstall -e --id Python.Python.3.12
rmdir /s /q ".venv"