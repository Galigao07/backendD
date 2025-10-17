Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c python manage.py runserver 127.0.0.1:8000", 0

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c daphne -b 0.0.0.0 -p 8001 backendD.asgi:application", 0
Set WshShell = Nothing


' python manage.py runserver_plus --cert-file cert.pem --key-file key.pem 192.168.68.103:8000