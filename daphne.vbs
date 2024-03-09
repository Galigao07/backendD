Set objShell = WScript.CreateObject("WScript.Shell")

' Set the current directory where the script is executed
Dim currentDirectory
currentDirectory = objShell.CurrentDirectory

' Change the path to your Django project's ASGI application
Dim asgiPath
asgiPath = currentDirectory & "\backendD\asgi.py:application"

' Run Daphne using Python interpreter
objShell.Run "cmd /c python -m daphne -b 0.0.0.0 -p 8001 backendD.asgi:application" , 1, True
