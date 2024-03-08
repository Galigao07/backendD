@echo off

REM Store the directory where the batch file is located
set "batch_directory=%~dp0"

echo Batch file directory: %batch_directory%

REM Activate the virtual environment
call "%batch_directory%backendEnv\Scripts\activate"


REM Print current directory
echo Current directory: %cd%

REM Run Daphne server
daphne -b 0.0.0.0 -p 8000 myproject.asgi:application

REM Deactivate the virtual environment
deactivate
