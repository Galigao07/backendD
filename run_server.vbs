Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c python manage.py runserver 127.0.0.1:8000", 0

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c daphne -b 0.0.0.0 -p 8001 backendD.asgi:application", 0
Set WshShell = Nothing